# app/config.py
import os


class Config:
    # Database configuration
    USERNAME = 'postgres'
    PASSWORD = '123'
    HOST = 'localhost'
    DB_NAME = 'ecommerce_shop'

    SQLALCHEMY_DATABASE_URI = f"postgresql://{USERNAME}:{PASSWORD}@{HOST}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Turn off modification tracking to save resources

    # JWT Configuration
    JWT_SECRET_KEY = 'd9f9b18d0c4f6ebc8a4f85e22f7383c9'
    # JWT_SECRET_KEY = os.urandom(24).hex()  # You can use this for a more secure key

    # File upload configuration
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static', 'uploads')  # Absolute path to ensure reliability
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
