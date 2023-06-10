from flask import Response, request, Blueprint, render_template, make_response
from yolo.tracker import ObjectTracker
from flask import current_app
import os
import re
import pytube

bp = Blueprint('video', __name__,url_prefix="/api" )

def convert_query_param_to_tuples(param):
    # Extract all the numbers from the string using regular expressions
    numbers = re.findall(r'[\d\.]+', param)

    # Convert the numbers to ints and group them into tuples
    tuples = [(round(float(numbers[i])), round(float(numbers[i+1]))) for i in range(0, len(numbers), 2)]

    
    return tuples

def download_youtube_video(url, output_path):
    try:
        youtube = pytube.YouTube(url)
        video = youtube.streams.get_highest_resolution()
        video.download(output_path=output_path)
      
        return video.default_filename
    except Exception as e:
        print(f"Error downloading video: {str(e)}")
    return None


@bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@bp.route('/save_video', methods=['POST'])
def save_video():
    file = request.files['video']
    filename = file.filename
    save_path = os.path.join(current_app.config['UPLOAD_VIDEO_FOLDER'], filename)

    file.save(save_path)
    response_data = {'message': f'Video {filename}  saved successfully', 'filename': f'{filename}'}
    response = make_response(response_data, 200)

    return response


@bp.route('/hello')
def hello():
    return 'Hello, World!'


@bp.route('/stream', methods=['GET'])
def video():
    global tracker

    # Get the source from the request query parameters
    filename = request.args.get('source')
    line1 = request.args.get('line1')
    line2 = request.args.get('line2')
    lines_list = []
    if line1 and line2 : 
        lines_list.append(convert_query_param_to_tuples(line1))
        lines_list.append(convert_query_param_to_tuples(line2))
        tracker = ObjectTracker(lines_coords=lines_list)
    else:
        tracker = ObjectTracker()
    upload_folder = current_app.config['UPLOAD_VIDEO_FOLDER']

   
    if re.match(r'^https?://', filename):
        # It's a URL, use it directly as the source_path
        # source_path = filename
        file_name_download = download_youtube_video(filename, upload_folder)
        source_path = os.path.join(upload_folder, file_name_download)
        print(source_path)
    else:
        # It's a filename, append it to the UPLOAD_VIDEO_FOLDER path
        source_path = os.path.join(upload_folder, filename)

    
    tracker.set_source_path(source_path)
    return Response(tracker(), mimetype='multipart/x-mixed-replace; boundary=frame')
