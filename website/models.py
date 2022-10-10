from . import db
from flask_login import UserMixin


class Program(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(10000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    time_start = db.Column(db.Integer)
    time_end = db.Column(db.Integer)
    date = db.Column(db.Integer)
    votes = db.Column(db.Integer)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    firstName = db.Column(db.String(150))
    programs = db.relationship('Program')