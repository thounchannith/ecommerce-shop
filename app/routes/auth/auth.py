# app/routes/auth/auth.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_refresh_token
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User, db

auth_bp = Blueprint('auth_bp', __name__)


# Register Route
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    is_admin = data.get('is_admin', False)

    if not username:
        return jsonify(message="Username is required"), 400
    if not email:
        return jsonify(message="Email is required"), 400
    if not password:
        return jsonify(message="Password is required"), 400

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify(message="Username already exists"), 409

    existing_email = User.query.filter_by(email=email).first()
    if existing_email:
        return jsonify(message="Email already exists"), 409

    hashed_password = generate_password_hash(password)

    new_user = User(first_name=first_name, last_name=last_name, username=username, email=email,
                    password=hashed_password, is_admin=is_admin)
    db.session.add(new_user)
    db.session.commit()

    return jsonify(message="User registered successfully"), 201


# Login Route
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify(message="Missing required fields"), 400

    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):

        access_token = create_refresh_token(identity=user.id)
        return jsonify(access_token=access_token), 200

    return jsonify(message="Invalid credentials"), 401
