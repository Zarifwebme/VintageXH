from .extensions import db
from flask_login import UserMixin

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    classification = db.Column(db.String(100), nullable=False)
    picture = db.Column(db.LargeBinary, nullable=True)  # Store picture as binary data
    mimetype = db.Column(db.String(50), nullable=True)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    phonenumber = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(100), nullable=False)


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
