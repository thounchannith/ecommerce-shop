from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User, Address, db

profile_bp = Blueprint('profile_bp', __name__)


# Update Profile
@profile_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    data = request.get_json()
    user_id = get_jwt_identity()

    user = User.query.get(user_id)
    if not user:
        return jsonify(message="User not found"), 404

    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)
    user.phone_number = data.get('phone_number', user.phone_number)
    db.session.commit()

    return jsonify(message="Profile updated"), 200


# View Profile
@profile_bp.route('/profile', methods=['GET'])
@jwt_required()
def view_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify(message="User not found"), 404

    return jsonify(user.to_dict())


# Manage Addresses
@profile_bp.route('/addresses', methods=['POST'])
@jwt_required()
def add_address():
    data = request.get_json()
    user_id = get_jwt_identity()

    new_address = Address(user_id=user_id, street=data['street'], city=data['city'], state=data['state'],
                          zip_code=data['zip_code'])
    db.session.add(new_address)
    db.session.commit()

    return jsonify(message="Address added"), 201


# Update Address
@profile_bp.route('/addresses/<int:id>', methods=['PUT'])
@jwt_required()
def update_address(id):
    data = request.get_json()
    address = Address.query.get(id)

    if not address or address.user_id != get_jwt_identity():
        return jsonify(message="Address not found or unauthorized"), 404

    address.street = data.get('street', address.street)
    address.city = data.get('city', address.city)
    address.state = data.get('state', address.state)
    address.zip_code = data.get('zip_code', address.zip_code)
    db.session.commit()

    return jsonify(message="Address updated"), 200


# Delete Address
@profile_bp.route('/addresses/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_address(id):
    address = Address.query.get(id)

    if not address or address.user_id != get_jwt_identity():
        return jsonify(message="Address not found or unauthorized"), 404

    db.session.delete(address)
    db.session.commit()

    return jsonify(message="Address deleted"), 200
