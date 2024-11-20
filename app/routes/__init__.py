# app/routes/__init__.py
from app.routes.auth.auth import auth_bp
from app.routes.category import category_bp
from app.routes.orders import order_bp
from app.routes.customer import customer_bp
from app.routes.carts import cart_bp


def register_routes(app):
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(category_bp, url_prefix='/api/admin/categories')
    app.register_blueprint(order_bp, url_prefix='/api/admin/orders')
    app.register_blueprint(customer_bp, url_prefix='/api/admin/customers')
    app.register_blueprint(cart_bp, url_prefix='/api/admin/carts')
