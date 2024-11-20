# app/routes/admin/customer.py
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.models import User, db

customer_bp = Blueprint('customer_bp', __name__)


# Admin: View All Customers
@customer_bp.route('/customers', methods=['GET'])
@jwt_required()
def list_customers():
    customers = User.query.filter_by(is_admin=False).all()
    return jsonify([customer.to_dict() for customer in customers])


# Admin: View Customer Details
@customer_bp.route('/customers/<int:id>', methods=['GET'])
@jwt_required()
def view_customer(id):
    customer = User.query.get(id)
    if customer:
        return jsonify(customer.to_dict())
    return jsonify(message="Customer not found"), 404


# Admin: Enable/Disable Customer Account
@customer_bp.route('/customers/<int:id>/status', methods=['PUT'])
@jwt_required()
def toggle_customer_status(id):
    data = request.get_json()
    customer = User.query.get(id)
    if customer:
        customer.is_active = data['is_active']
        db.session.commit()
        return jsonify(message="Customer status updated"), 200
    return jsonify(message="Customer not found"), 404
