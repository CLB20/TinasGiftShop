from app import app
from flask import render_template, redirect, url_for, flash, request, session
from flask_login import login_required, current_user
from datetime import date
import random
from app.db import db, Product, Order_item, Order, Message
# import stripe


@app.route("/")
def home():
    all_products = Product.query.all()
    sample_products = random.sample(all_products, 3)
    if "temp_order" not in session:
        temporary_order = None
        total = 0
    else:
        temporary_order = session["temp_order"]
        total = session["temp_total"]
        print(temporary_order)
    return render_template("index.html", sample_products=sample_products, order=temporary_order, total=total)


@app.route("/about")
def about():
    if "temp_order" not in session:
        temporary_order = None
        total = 0
    else:
        temporary_order = session["temp_order"]
        total = session["temp_total"]
    return render_template("about.html", order=temporary_order, total=total)


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == 'GET':
        if "temp_order" not in session:
            temporary_order = None
            total = 0
        else:
            temporary_order = session["temp_order"]
            total = session["temp_total"]
        return render_template("contact.html", order=temporary_order, total=total)
    elif request.method == 'POST':
        name = request.form["name"]
        email = request.form["email"]
        subject = request.form["subject"]
        message = request.form["message"]
        message_date = date.today()
        new_message = Message(name=name,
                              email=email,
                              subject=subject,
                              message=message,
                              date=message_date)
        db.session.add(new_message)
        db.session.commit()
        flash("Thank you! Your message has been sent.")
        return redirect(url_for("contact"))


@app.route("/details")
@login_required
def prof_details():
    return render_template("profile-details.html")


@app.route("/shop/<category>")
def shop(category):
    products = Product.query.filter_by(category=category)
    if "temp_order" not in session:
        temporary_order = None
        total = 0
    else:
        temporary_order = session["temp_order"]
        total = session["temp_total"]
    return render_template("shop.html", products=products, order=temporary_order, total=total)


@app.route("/product/<p_id>", methods=['GET', 'POST'])
def single_product(p_id):
    product = Product.query.get(p_id)
    if request.method == 'GET':
        if "temp_order" not in session:
            temporary_order = None
            total = 0
        else:
            temporary_order = session["temp_order"]
            total = session["temp_total"]
        all_products = Product.query.all()
        sample_products = random.sample(all_products, 3)
        return render_template("product-single.html", product=product, order=temporary_order, total=total, sample_products=sample_products)
    elif request.method == 'POST':
        text_color = request.form["text_color"]
        text = request.form["text"]
        if not text:
            text = "No text"
        if product.category == "balloons":
            balloons_color = f"{request.form['balloons_color1']}, {request.form['balloons_color2']}"
        else:
            balloons_color = "N/A"
        quantity = request.form["product-quantity"]
        order = {"product_id": product.id,
                 "image_name": product.image_name,
                 "product_name": product.name,
                 "price": product.price,
                 "text_color": text_color,
                 "text": text,
                 "balloons_color": balloons_color,
                 "quantity": quantity}
        if "temp_order" not in session:
            order_list = [order]
            session["temp_order"] = order_list
            session["temp_total"] = order["price"]
        else:
            order_list = session["temp_order"] + [order]
            session["temp_order"] = order_list
            total = 0
            for item in session["temp_order"]:
                total += (item["price"] * int(item["quantity"]))
            session["temp_total"] = total
        return redirect(url_for("cart"))


@app.route("/cart")
def cart():
    if "temp_order" not in session:
        temporary_order = None
        total = 0
    else:
        temporary_order = session["temp_order"]
        total = session["temp_total"]
    return render_template("cart.html", order=temporary_order, total=total)


@app.route("/remove_item/<item>")
def remove_item(item):
    if "temp_order" in session:
        item_to_remove = session["temp_order"][int(item)]
        print(item_to_remove)
        order_list = session["temp_order"]
        order_list.remove(item_to_remove)
        session["temp_order"] = order_list
        print(session["temp_order"])
        total = 0
        for item in session["temp_order"]:
            total += (item["price"] * int(item["quantity"]))
        session["temp_total"] = total
    return redirect(url_for("cart"))


@app.route("/checkout")
def checkout():
    if current_user.is_authenticated:
        if "temp_order" not in session:
            temporary_order = None
            total = 0
        else:
            temporary_order = session["temp_order"]
            total = session["temp_total"]
        gst = total * 0.05
        if request.method == "GET":
            return render_template("checkout.html", order=temporary_order, total=total, gst=gst)
    else:
        flash("Sign in to check out faster!")
        return redirect(url_for("login"))


@app.route("/pay_confirmation")
def pay_confirmation():
    print(session["order_id"])
    if session["order_id"]:
        order = Order.query.get(session["order_id"])
        order.status = "Paid"
        db.session.commit()
    session.pop("temp_order", None)
    session.pop("order_id", None)
    return render_template("confirmation.html")


@app.route('/create_checkout_session', methods=['POST'])
def create_checkout_session():
    if "temp_order" not in session:
        temporary_order = None
        total = 0
    else:
        temporary_order = session["temp_order"]
        total = session["temp_total"]
    user_id = current_user.id
    street_address = request.form["address"]
    postal_code = request.form["postal_code"]
    city = request.form["city"]
    address = f"{street_address}/{city}/{postal_code}"
    pickup_date = date.today()
    status = "Payment pending"
    new_order = Order(user_id=user_id,
                      address=address,
                      pickup_date=pickup_date,
                      status=status,
                      total=total)
    db.session.add(new_order)
    db.session.commit()
    db.session.flush()
    order_id = new_order.id
    for item in temporary_order:
        order_item = Order_item(order_id=order_id,
                                item_num=temporary_order.index(item),
                                product_id=item["product_id"],
                                quantity=item["quantity"],
                                text=item["text"],
                                text_color=item["text_color"],
                                balloons_color=item["balloons_color"])
        db.session.add(order_item)
    db.session.commit()
    session["order_id"] = order_id
    print(session["order_id"])
    # try:
    #     checkout_session = stripe.checkout.Session.create(
    #         line_items=[
    #             {
    #                 'price': 'price_1Kz0WYJkVDjhXN66qaHtaQHs',
    #                 'quantity': 1,
    #             },
    #         ],
    #         mode='payment',
    #         success_url=url_for("pay_confirmation", _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
    #         cancel_url=url_for("home", _external=True),
    #     )
    # except Exception as e:
    #     print(str(e))
    #     return render_template("404.html"), 404
    # return redirect(checkout_session.url, code=303)
    return redirect(url_for('home'))
