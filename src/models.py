from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(1000), unique=True, nullable=False)
    favorites = db.relationship('Favorite', back_populates='user')

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }


class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    localization = db.Column(db.String(200), nullable=True, default='Unknown')
    description = db.Column(db.String(1000), nullable=True, default='Unknown')

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "localization": self.localization,
            "description": self.description
        }


class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    age = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.String(100), nullable=True, default='Unknown')
    affiliation = db.Column(db.String(200), default='Unknown')
    species = db.Column(db.String(100), default='Unknown')
    origin_planet_id = db.Column(
        db.Integer, db.ForeignKey('planet.id'), nullable=True)
    origin_planet = db.relationship('Planet', backref='characters')

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age if self.age else "Unknown",
            "gender": self.gender,
            "affiliation": self.affiliation,
            "species": self.species,
            "origin_planet": self.origin_planet.name if self.origin_planet else "Unknown"
        }


class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates='favorites')
    planet_id = db.Column(db.ForeignKey('planet.id'), nullable=True)
    character_id = db.Column(db.ForeignKey('character.id'), nullable=True)

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
            "character_id": self.character_id,
        }
