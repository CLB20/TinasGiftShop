from flask import Flask
import os
from flask_bootstrap import Bootstrap
import stripe

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
Bootstrap(app)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['STRIPE_PUBLIC_KEY'] = os.environ.get("STRIPE_PUBLIC_KEY")
app.config['STRIPE_SECRET_KEY'] = os.environ.get("STRIPE_SECRET_KEY")

stripe.api_key = app.config['STRIPE_SECRET_KEY']


from app import views
from app import admin_views
from app import authorization