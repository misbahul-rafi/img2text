from flask import Flask
from app.config import Config
from app.routes.image_routes import image_routes
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    app.register_blueprint(image_routes)

    return app
