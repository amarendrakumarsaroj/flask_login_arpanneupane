from extensions import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(345), nullable=False, unique=True)
    password = db.Column(db.String(345), nullable=False, unique=False)
     