# app/routes/admin/category.py
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.models import Category, db

category_bp = Blueprint('category_bp', __name__)


# Admin: Add Category
@category_bp.route('/categories', methods=['POST'])
@jwt_required()
def add_category():
    data = request.get_json()
    new_category = Category(name=data['name'])
    db.session.add(new_category)
    db.session.commit()
    return jsonify(message="Category added"), 201


# Admin: Edit Category
@category_bp.route('/categories/<int:id>', methods=['PUT'])
@jwt_required()
def edit_category(id):
    category = Category.query.get(id)
    if category:
        data = request.get_json()
        category.name = data['name']
        db.session.commit()
        return jsonify(message="Category updated"), 200
    return jsonify(message="Category not found"), 404


# Admin: Delete Category
@category_bp.route('/categories/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_category(id):
    category = Category.query.get(id)
    if category:
        db.session.delete(category)
        db.session.commit()
        return jsonify(message="Category deleted"), 200
    return jsonify(message="Category not found"), 404
