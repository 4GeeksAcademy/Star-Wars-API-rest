# =========================
# DELETE FAVORITE
# =========================

@app.route('/favorite/planet/<int:favorite_id>', methods=['DELETE'])
def delete_planet_favorite(favorite_id):
    favorite = Favorite.query.get(favorite_id)
    if not favorite:
        return jsonify({"error": "Favorito no encontrado"}), 404
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"msg": "Favorito eliminado"}), 200
"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Favorite
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints


@app.route('/')
def sitemap():
    return generate_sitemap(app)

# =========================
# USER
# =========================


@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([users.serialize() for u in users]), 200


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "usuario no encontrado"})
    return jsonify(user.serialize()), 200


@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "usuario no encontrado"})
    if not user.favorites:
        return jsonify({"error": "este usuario aun no tiene favoritos"})
    favorites = [fav.serialize() for fav in user.favorites]
    return jsonify(favorites), 200


# =========================
# CHARACTER
# =========================

@app.route('/people', methods=['GET'])
def get_characters():
    characters = Character.query.all()
    if not characters:
        return jsonify({"error": "no hay personajes registrados"})
    return jsonify([character.serialize() for character in characters]), 200


@app.route('/people/<int:character_id>', methods=['GET'])
def get_character(character_id):
    character = Character.query.get(character_id)
    if not character:
        return jsonify({"error": "personaje no encontrado"})
    return jsonify(character.serialize()), 200


@app.route('/people', methods=['POST'])
def create_character():
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({"error": "faltan campos requeridos"}), 400
    character = Character(
        name=data.get("name"),
        age=data.get("age"),
        gender=data.get("gender"),
        affiliation=data.get("affiliation"),
        species=data.get("species"),
        origin_planet_id=data.get("origin_planet_id")
    )
    db.session.add(character)
    db.session.commit()
    return jsonify(character.serialize()), 201

# =========================
# PLANET
# =========================


@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    if not planets:
        return jsonify({"error": "no hay planetas registrados"})
    return jsonify([planet.serialize() for planet in planets]), 200


@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify({"error": "planeta no encontrado"})
    return jsonify(planet.serialize()), 200


@app.route('/planets', methods=['POST'])
def create_planet():
    data = request.get_json()
    planet = Planet(
        name=data["name"],
        localization=data["localization"],
        description=data["description"]
    )
    db.session.add(planet)
    db.session.commit()
    return jsonify(planet.serialize()), 201

# =========================
# FAVORITES
# =========================


@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_planet_favorite(planet_id):
    data = request.get_json()
    user_id = data.get('user_id')
    if not user_id:
        return jsonify({"error": "Falta el id del usuario"}), 400
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404
    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify({"error": "Planeta no encontrado"}), 404
    favorite = Favorite(user_id=user.id, planet_id=planet.id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify(favorite.serialize()), 201


@app.route('/favorite/people/<int:character_id>', methods=['POST'])
def add_people_favorite(character_id):
    data = request.get_json()
    user_id = data.get('user_id')
    if not user_id:
        return jsonify({"error": "Falta el id del usuario"}), 400
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404
    character = Character.query.get(character_id)
    if not character:
        return jsonify({"error": "Personaje no encontrado"}), 404
    favorite = Favorite(user_id=user.id, character_id=character.id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify(favorite.serialize()), 201



    # this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
