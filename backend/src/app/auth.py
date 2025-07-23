from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models import db, User
from passlib.hash import bcrypt
from datetime import timedelta

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()
    if user and bcrypt.verify(password, user.password_hash):
        token = create_access_token(identity=username, expires_delta=timedelta(hours=1))
        return jsonify(access_token=token), 200

    return jsonify({"msg": "Invalid username or password"}), 401
