from flask import Blueprint, request
from app.controllers.image_controller import ImageController
from app.utils import formatting

image_routes = Blueprint('image_routes', __name__)
image_controller = ImageController()

@image_routes.route('/img2text', methods=['POST'])
def process_image():
    return image_controller.process_image()
  
@image_routes.route('/test-parsing', methods=["POST"])
def parsing():
    return formatting(request.json)
