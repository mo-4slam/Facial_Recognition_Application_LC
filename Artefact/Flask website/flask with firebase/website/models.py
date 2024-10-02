from unicodedata import name

from sqlalchemy import ForeignKey
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# defines the user with the following info, i.e their id, email, password and name


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150),)
    name = db.Column(db.String(150),)
