import eventlet

from app.sockets import VideoNamespace
eventlet.monkey_patch()
import os
from flask_cors import CORS
from flask_socketio import SocketIO
from flask import Flask




def create_app():
    app = Flask(__name__)
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    app.config['UPLOAD_VIDEO_FOLDER'] = os.path.join(current_dir, 'assets', 'video')
    app.config['UPLOAD_IMAGE_FOLDER'] = os.path.join(current_dir, 'assets', 'image')

    CORS(app, resources={r"/*": {"origins": "*"}})

    socketio = SocketIO(app,  logger=True, cors_allowed_origins='*',engineio_logger=True)
    
    from . import routes
    app.register_blueprint(routes.bp)


    socketio.on_namespace(VideoNamespace('/test', app_context=app))

    return app,socketio
