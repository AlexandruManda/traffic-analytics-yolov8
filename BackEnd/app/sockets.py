import cv2,os
from time import time
from flask_socketio import Namespace, emit
from yolo.object_detection import ObjectDetection

class VideoNamespace(Namespace):
    def __init__(self, namespace=None, app_context=None):
        super(VideoNamespace, self).__init__(namespace)
        self.app_context = app_context
        self.detection = ObjectDetection()
    
    def start_video(self):
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        source_path = os.path.join(current_dir, 'assets', 'videos', '1.mp4')
        cap = cv2.VideoCapture(source_path)
        assert cap.isOpened()
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)
        target_fps = 1
        time_per_frame = 1.0 / target_fps  # In seconds
        while True:
            start_time = time()
            ret,frame =cap.read()
            assert ret
            detected = self.detection.gen_image(frame)
            print(detected)
            emit('processed_image',{'processed_data':detected})
            break
    
    def on_connect(self):
        print("connected")
        emit("image",{"message":"hello"})
        # self.start_video()

    def on_disconnect(self):
        print("client disconnected")

