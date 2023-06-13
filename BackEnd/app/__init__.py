import eventlet
eventlet.monkey_patch()
import os

from flask_cors import CORS
from flask import Flask




def create_app():
    app = Flask(__name__)
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    app.config['UPLOAD_VIDEO_FOLDER'] = os.path.join(current_dir, 'assets', 'video')
    app.config['UPLOAD_IMAGE_FOLDER'] = os.path.join(current_dir, 'assets', 'image')

    CORS(app, resources={r"/*": {"origins": "*"}})

    from . import routes
    app.register_blueprint(routes.bp)

    return app
