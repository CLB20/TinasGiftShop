from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from app import app

db = SQLAlchemy(app)


# Configure tables

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    orders = db.relationship("Order", backref="owner")

    def __init__(self, email, name, password):
        self.email = email
        self.name = name
        self.password = password


class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    image_name = db.Column(db.String(100), nullable=True)
    description = db.Column(db.String(250), nullable=True)
    stock = db.Column(db.Integer, nullable=False)


class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    order_items = db.relationship("Order_item", backref="owner")
    address = db.Column(db.String(100), nullable=False)
    pickup_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    total = db.Column(db.Integer, nullable=False)


class Order_item(db.Model):
    __tablename__ = "order_items"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"))
    item_num = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"))
    quantity = db.Column(db.Integer, nullable=False)
    text = db.Column(db.String(100), nullable=False)
    text_color = db.Column(db.String(100), nullable=True)
    balloons_color = db.Column(db.String(100), nullable=True)


class Message(db.Model):
    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(100), nullable=True)
    message = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(100), nullable=False)


db.create_all()
