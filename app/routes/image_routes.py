# app/views/image_view.py
from flask import Blueprint
from app.controllers.image_controller import ImageController

image_routes = Blueprint('image_routes', __name__)
image_controller = ImageController()

@image_routes.route('/api/v1/process_image', methods=['POST'])
def process_image():
    return image_controller.process_image()
