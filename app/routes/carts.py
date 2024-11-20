# app/routes/admin/carts.py
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Cart, Product, db, Order, OrderItem

cart_bp = Blueprint('cart_bp', __name__)


# Add to Cart
@cart_bp.route('/cart', methods=['POST'])
@jwt_required()
def add_to_cart():
    data = request.get_json()
    user_id = get_jwt_identity()
    product_id = data['product_id']
    quantity = data['quantity']

    product = Product.query.get(product_id)
    if not product:
        return jsonify(message="Product not found"), 404

    # Check if product already in cart
    existing_cart_item = Cart.query.filter_by(user_id=user_id, product_id=product_id).first()

    if existing_cart_item:
        existing_cart_item.quantity += quantity
    else:
        new_cart_item = Cart(user_id=user_id, product_id=product_id, quantity=quantity)
        db.session.add(new_cart_item)

    db.session.commit()
    return jsonify(message="Product added to cart"), 200


# Update Cart
@cart_bp.route('/cart', methods=['PUT'])
@jwt_required()
def update_cart():
    data = request.get_json()
    user_id = get_jwt_identity()
    product_id = data['product_id']
    quantity = data['quantity']

    cart_item = Cart.query.filter_by(user_id=user_id, product_id=product_id).first()

    if not cart_item:
        return jsonify(message="Product not found in cart"), 404

    cart_item.quantity = quantity
    db.session.commit()
    return jsonify(message="Cart updated"), 200


# View Cart
@cart_bp.route('/cart', methods=['GET'])
@jwt_required()
def view_cart():
    user_id = get_jwt_identity()
    cart_items = Cart.query.filter_by(user_id=user_id).all()
    return jsonify([item.to_dict() for item in cart_items]), 200


# Checkout
@cart_bp.route('/checkout', methods=['POST'])
@jwt_required()
def checkout():
    user_id = get_jwt_identity()
    cart_items = Cart.query.filter_by(user_id=user_id).all()

    if not cart_items:
        return jsonify(message="Cart is empty"), 400

    total_price = sum([item.product.price * item.quantity for item in cart_items])

    # Create order (you need to implement this part)
    order = create_order(user_id, cart_items, total_price)
    db.session.commit()

    # Clear the cart
    for item in cart_items:
        db.session.delete(item)
    db.session.commit()

    return jsonify(message="Order placed successfully", order_id=order.id), 200


def create_order(user_id, cart_items, total_price):
    # Create a new order
    order = Order(
        user_id=user_id,
        total_price=total_price,
        status='pending',  # You can modify this based on your business rules (e.g., 'paid', 'processing', etc.)
        is_active=True  # The order is active initially
    )

    # Add the order to the session (but not committed yet)
    db.session.add(order)

    # Create order items from the cart items
    for item in cart_items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=item.product.price  # You could store the price at the time of order
        )
        db.session.add(order_item)

    # Commit the transaction (save the order and its items)
    db.session.commit()

    return order
