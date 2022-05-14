from app import app
from flask import render_template, redirect, url_for, flash, request, session
from flask_login import login_user, LoginManager, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.db import db, User

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template("signin.html")
    elif request.method == 'POST':
        user = User.query.filter_by(email=request.form["email"]).first()
        if user:
            flash("This email is already registered. Log in instead.")
            return redirect(url_for("login"))

        name = request.form["name"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"], method="pbkdf2:sha256", salt_length=8)

        new_user = User(email, name, password)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        if "temp_order" not in session:
            return redirect(url_for('prof_details'))
        else:
            return redirect(url_for("checkout"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    elif request.method == 'POST':
        user = User.query.filter_by(email=request.form["email"]).first()
        if not user:
            flash("The email doesn't exist. Please try again.")
            redirect(url_for("login"))
        elif not check_password_hash(user.password, request.form["password"]):
            flash("Incorrect password. Please try again")
            redirect(url_for("login"))
        else:
            login_user(user)
            if "temp_order" not in session:
                return redirect(url_for("home"))
            else:
                return redirect(url_for("checkout"))

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))
