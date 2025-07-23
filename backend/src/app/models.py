# models.py
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

class Person(db.Model):
    __tablename__ = 'persons'
    nconst = db.Column(db.String, primary_key=True)
    primaryName = db.Column(db.String)
    birthYear = db.Column(db.Integer)
    deathYear = db.Column(db.Integer)
    primaryProfession = db.Column(db.String)
    knownForTitles = db.Column(db.String)

class Title(db.Model):
    __tablename__ = 'titles'
    tconst = db.Column(db.String, primary_key=True)
    titleType = db.Column(db.String)
    primaryTitle = db.Column(db.String)
    originalTitle = db.Column(db.String)
    isAdult = db.Column(db.Boolean)
    startYear = db.Column(db.Integer)
    endYear = db.Column(db.Integer)
    runtimeMinutes = db.Column(db.Integer)
    genres = db.Column(db.String)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

# Marshmallow Schemas

class TitleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Title
        load_instance = True

class PersonSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Person
        load_instance = True
