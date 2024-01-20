from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(150), unique = True)
    password = db.Column(db.String(150))

class Note(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(150))
    createDate = db.Column(db.Date)
    content = db.Column(db.String(1000))
    userId = db.Column(db.Integer, db.ForeignKey("user.id"))

class Flashset(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(150))
    userId = db.Column(db.Integer, db.ForeignKey("user.id"))
    numOfCards = db.Column(db.Integer)

class Flashcard(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    front = db.Column(db.String(150))
    back = db.Column(db.String(150))
    flashsetId = db.Column(db.Integer, db.ForeignKey("flashset.id"))