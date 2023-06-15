from flask import Response, jsonify, request, Blueprint, render_template, make_response, send_from_directory
from flask import current_app
import os
import logging
import re

try:
    from .utils.download_manager import DownloadManager
    from .tracker.tracker_manager import TrackerManager
except:
    from utils.download_manager import DownloadManager
    from tracker.tracker_manager import TrackerManager

bp = Blueprint('video', __name__, url_prefix="/api")
MIME_TYPE = 'multipart/x-mixed-replace; boundary=frame'
INVALID_TASK_MSG = 'Invalid task type'
HTTP_BAD_REQUEST = 400
HTTP_OK = 200

logging.basicConfig(level=logging.INFO)

@bp.route('/', methods=['GET'])
def index():
    """Returns the index page."""
    return render_template('index.html')

@bp.route('/save_video', methods=['POST'])
def save_video():
    """Saves a video to the server."""
    file = request.files['video']
    filename = file.filename
    save_path = os.path.join(current_app.config['UPLOAD_VIDEO_FOLDER'], filename)
    file.save(save_path)
    response_data = {'message': f'Video {filename}  saved successfully', 'filename': filename}
    response = make_response(response_data, HTTP_OK)
    return response

@bp.route('/hello')
def hello():
    """Returns a hello world message."""
    return 'Hello, World!'

@bp.route('/stream', methods=['GET'])
def video():
    """Streams a video based on the source and task provided in the query parameters."""
    source = request.args.get('source')
    line1 = request.args.get('line1')
    line2 = request.args.get('line2')
    task = request.args.get('task')
    upload_folder = current_app.config['UPLOAD_VIDEO_FOLDER']

    if source is None or task is None:
        logging.error("Required query parameters 'source' and 'task' not provided.")
        return jsonify({'error': 'Required query parameters not provided'}), HTTP_BAD_REQUEST

    source = "0" if source == "0" else (source if re.match(r'^(https?|udp)://', source) else os.path.join(upload_folder, source))

    print(source)
    tracker_manager = TrackerManager()
    tracker = tracker_manager.create_tracker(task, source, line1, line2)

    if tracker:
        return Response(tracker(), mimetype=MIME_TYPE)
    else:
        return jsonify({'error': INVALID_TASK_MSG}), HTTP_BAD_REQUEST


@bp.route('/download', methods=['GET'])
def download():
    """Downloads a YouTube video and sends it as a file response."""
    youtube_url = request.args.get('url')
    save_path = current_app.config['UPLOAD_VIDEO_FOLDER']

    if youtube_url is None:
        logging.error("Required query parameter 'url' not provided.")
        return jsonify({'error': 'Required query parameter not provided'}), HTTP_BAD_REQUEST

    filename = DownloadManager.download_youtube_video(youtube_url, save_path)

    if filename:
        file_path = os.path.join(save_path, filename)
        response = make_response(send_from_directory(save_path, filename, as_attachment=True))
        response.headers['Content-Disposition'] = f'attachment; filename="{filename}"'
        response.headers['Access-Control-Expose-Headers'] = 'Content-Disposition'
        return response
    else:
        return 'Failed to download the YouTube video'
