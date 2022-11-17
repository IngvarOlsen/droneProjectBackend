from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

## sqlalchemy migrate_engine
## https://stackoverflow.com/questions/14032066/cant-import-sqlalchemy-migrate-engine



class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_name = db.Column(db.String(150))
    imageSet_id = db.Column(db.Integer)


class ImageSet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_id = db.Column(db.String(150), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
   

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')
    imageSets = db.relationship('ImageSet')


