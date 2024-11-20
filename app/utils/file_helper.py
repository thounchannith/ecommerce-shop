# app/utils/file_helper.py
import os
from flask import current_app
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}


def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_image(file, product_id):
    """Save uploaded image for a given product."""
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Use product_id to create a directory if it doesn't exist
        image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], str(product_id), filename)

        # Ensure the product folder exists
        os.makedirs(os.path.dirname(image_path), exist_ok=True)

        # Save the image to the folder
        file.save(image_path)
        return image_path

    return None
