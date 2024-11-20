# app/routes/admin/products.py
import os

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.models import Product, db, ProductImage
from app.utils.file_helper import save_image

product_bp = Blueprint('product_bp', __name__)


# List Products with Search Filter
@product_bp.route('/', methods=['GET'])
def list_products():
    query = request.args
    name = query.get('name')
    category_id = query.get('category_id')

    products = Product.query.filter(Product.name.contains(name)).filter_by(category_id=category_id).all()
    return jsonify([product.to_dict() for product in products])


# Admin: Add Product
@product_bp.route('/products', methods=['POST'])
@jwt_required()
def add_product():
    data = request.get_json()
    new_product = Product(name=data['name'], price=data['price'], description=data['description'], stock=data['stock'])

    # Save the product first to get the product_id
    db.session.add(new_product)
    db.session.commit()

    # Handle Image Upload
    if 'image' in request.files:
        image = request.files['image']
        image_path = save_image(image, new_product.id)
        if image_path:
            new_image = ProductImage(product_id=new_product.id, image_path=image_path)
            db.session.add(new_image)
            db.session.commit()

    return jsonify(message="Product added", product=new_product.to_dict()), 201


# Edit Product with Image
@product_bp.route('/products/<int:id>', methods=['PUT'])
@jwt_required()
def edit_product(id):
    data = request.get_json()
    product = Product.query.get(id)

    if product:
        product.name = data['name']
        product.price = data['price']
        product.description = data['description']
        product.stock = data['stock']

        # Handle Image Upload (If new image is provided)
        if 'image' in request.files:
            image = request.files['image']
            image_path = save_image(image, product.id)
            if image_path:
                # Delete previous image if exists (Optional)
                if product.images:
                    old_image = product.images[0]
                    if os.path.exists(old_image.image_path):  # Check if file exists
                        os.remove(old_image.image_path)  # Delete previous image file
                        db.session.delete(old_image)  # Remove image from the database
                new_image = ProductImage(product_id=product.id, image_path=image_path)
                db.session.add(new_image)

        db.session.commit()
        return jsonify(message="Product updated", product=product.to_dict()), 200
    return jsonify(message="Product not found"), 404


# Delete Product and Remove Images
@product_bp.route('/products/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_product(id):
    product = Product.query.get(id)
    if product:
        for image in product.images:
            if os.path.exists(image.image_path):
                os.remove(image.image_path)
            db.session.delete(image)

        db.session.delete(product)
        db.session.commit()
        return jsonify(message="Product and associated images deleted"), 200

    return jsonify(message="Product not found"), 404


# Product Details for Users
@product_bp.route('/products/<int:id>', methods=['GET'])
def product_details(id):
    product = Product.query.get(id)
    if product:
        return jsonify(product.to_dict())
    return jsonify(message="Product not found"), 404


@product_bp.route('/products', methods=['GET'])
def search_products():
    query = request.args
    name = query.get('name', '')
    category_id = query.get('category_id')
    min_price = query.get('min_price', type=float)
    max_price = query.get('max_price', type=float)

    products = Product.query.filter(Product.name.contains(name))

    if category_id:
        products = products.filter_by(category_id=category_id)
    if min_price:
        products = products.filter(Product.price >= min_price)
    if max_price:
        products = products.filter(Product.price <= max_price)

    products = products.all()
    return jsonify([product.to_dict() for product in products])


# Product Details
@product_bp.route('/products/<int:id>', methods=['GET'])
def product_details(id):
    product = Product.query.get(id)
    if product:
        return jsonify(product.to_dict())
    return jsonify(message="Product not found"), 404
