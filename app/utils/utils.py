# app/utils/utils.py
from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity

from app.models import User


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user or user.role != 'admin':
            return jsonify(message="Admin access required"), 403
        return func(*args, **kwargs)

    return wrapper
