from app import app
from flask import render_template, redirect, url_for, flash, abort, request
from flask_login import login_required, current_user
from functools import wraps
from app.db import db, User, Product, Order_item, Order, Message


def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.id != 1:
            return abort(403)
        return f(*args, **kwargs)

    return decorated_function


@app.route("/admin/create_product", methods=['GET', 'POST'])
@login_required
@admin_only
def create_product():
    if request.method == 'GET':
        products = Product.query.all()
        return render_template("admin_products.html", products=products)
    elif request.method == 'POST':
        product = Product.query.filter_by(name=request.form["name"]).first()
        if product:
            flash("This product already exists in the DB.")
            return redirect(url_for("create_product"))

        name = request.form["name"]
        category = request.form["category"]
        price = request.form["price"]
        image_name = request.form["image_name"]
        description = request.form["description"]
        stock = request.form["stock"]

        new_product = Product(name=name,
                              category=category,
                              price=price,
                              image_name=image_name,
                              description=description,
                              stock=stock)
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('create_product'))


@app.route("/admin/my_orders")
@admin_only
def my_orders():
    users = User.query.all()
    orders = Order.query.all()
    order_items = Order_item.query.all()
    return render_template("admin_orders.html", users=users, orders=orders, items=order_items)


@app.route("/admin/my_messages")
@admin_only
def my_messages():
    messages = Message.query.all()
    return render_template("admin_messages.html", messages=messages)


@app.route("/admin/delete_message/<int:id>")
@admin_only
def delete_message(id):
    message_to_delete = Message.query.get(id)
    db.session.delete(message_to_delete)
    db.session.commit()
    return redirect(url_for("my_messages"))
