# app/routes/admin/orders.py
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Order, db

order_bp = Blueprint('order_bp', __name__)


# Place Order
@order_bp.route('/orders', methods=['POST'])
@jwt_required()
def place_order():
    user_id = get_jwt_identity()
    data = request.get_json()
    address = data['address']

    # Create the order (you need to implement this part)
    order = Order(user_id=user_id, address=address)
    db.session.add(order)
    db.session.commit()

    return jsonify(message="Order placed successfully", order_id=order.id), 200


# View Order History
@order_bp.route('/orders', methods=['GET'])
@jwt_required()
def order_history():
    user_id = get_jwt_identity()
    orders = Order.query.filter_by(user_id=user_id).all()
    return jsonify([order.to_dict() for order in orders])


# Cancel Order
@order_bp.route('/orders/cancel', methods=['POST'])
@jwt_required()
def cancel_order():
    data = request.get_json()
    order_id = data['order_id']

    order = Order.query.get(order_id)
    if not order or order.user_id != get_jwt_identity():
        return jsonify(message="Order not found or unauthorized"), 404

    # Implement cancellation logic here
    order.status = 'cancelled'
    db.session.commit()

    return jsonify(message="Order cancelled"), 200
