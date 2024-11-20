from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# User Model (Admin and Customer)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(120), nullable=True, default='')  # Default empty string
    last_name = db.Column(db.String(120), nullable=True, default='')  # Default empty string
    phone_number = db.Column(db.String(20), nullable=True)
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    orders = db.relationship('Order', backref='user', lazy=True)
    cart_items = db.relationship('Cart', backref='user_cart', lazy=True)
    # Address relationship with a unique backref name 'addresses'
    address_list = db.relationship('Address', backref='user_address', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone_number': self.phone_number,
            'is_admin': self.is_admin,
            'is_active': self.is_active,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


# Address Model (for Customer's Shipping Address)
class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    street = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    zip_code = db.Column(db.String(20), nullable=False)
    is_default = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Removed redundant 'user' backref definition here
    # The backref is already defined in the User model: backref='user_address'

    def __repr__(self):
        return f'<Address {self.street}, {self.city}, {self.state}>'

    def to_dict(self):
        return {
            'id': self.id,
            'street': self.street,
            'city': self.city,
            'state': self.state,
            'zip_code': self.zip_code,
            'is_default': self.is_default,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


# Product Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(500))
    stock = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship with Categories (Many-to-One)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
    category = db.relationship('Category', backref='category_products')

    # Relationship with OrderItems (Many-to-Many via OrderItems)
    order_items = db.relationship('OrderItem', backref='order_items_product', lazy=True, cascade="all, delete-orphan")

    # Relationship with Product Images
    images = db.relationship('ProductImage', backref='product_images', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Product {self.name}, Price: {self.price}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'description': self.description,
            'stock': self.stock,
            'category': self.category.name if self.category else None,
            'is_active': self.is_active,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


# ProductImage Model (for storing images of products)
class ProductImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    image_path = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship to Product
    product = db.relationship('Product', backref=db.backref('product_images', lazy=True))

    def __repr__(self):
        return f'<ProductImage {self.image_path}>'


# Category Model (for categorizing products)
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Category {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'is_active': self.is_active,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


# Cart Model (For items added to cart)
class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    user = db.relationship('User',
                           backref=db.backref('user_cart_items', lazy=True))  # Unique backref for user_cart_items
    product = db.relationship('Product', backref=db.backref('cart_items', lazy=True))

    def __repr__(self):
        return f'<Cart {self.user.username}, Product: {self.product.name}, Quantity: {self.quantity}>'

    def to_dict(self):
        return {
            'product_id': self.product.id,
            'product_name': self.product.name,
            'quantity': self.quantity,
            'price': self.product.price,
            'created_at': self.created_at
        }


# Order Model (for placing an order)
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='pending')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship with OrderItem (One-to-Many)
    order_items = db.relationship('OrderItem', backref='order_items_order', lazy=True)

    def __repr__(self):
        return f'<Order {self.id}, Total: {self.total_price}, Status: {self.status}>'

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'total_price': self.total_price,
            'status': self.status,
            'is_active': self.is_active,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


# OrderItem Model (Join Table between Orders and Products)
class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    price = db.Column(db.Float, nullable=False)

    # Relationship with Order (One-to-Many)
    order = db.relationship('Order', backref=db.backref('order_items_list', lazy=True))  # Changed backref to 'order_items_list'

    def __repr__(self):
        return f'<OrderItem {self.product.name}, Quantity: {self.quantity}>'

    def to_dict(self):
        return {
            'product_id': self.product_id,
            'product_name': self.product.name,
            'quantity': self.quantity,
            'price': self.price
        }
