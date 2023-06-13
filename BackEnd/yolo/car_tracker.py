import os
import cv2
import torch
import pafy
import argparse
import supervision as sv
from ultralytics import YOLO
from time import time

try:
    from yolo.classes.line import Line
    from yolo.classes.line import Line
    from yolo.classes.total_classes_rectangle import TotalCountRectangle
    from yolo.classes.speed import SpeedEstimation
    from yolo.base.base_tracker import BaseTracker
    from yolo.util import process_source
except ImportError:
    from classes.line import Line
    from classes.line import Line
    from classes.total_classes_rectangle import TotalCountRectangle
    from classes.speed import SpeedEstimation
    from base.base_tracker import BaseTracker
    from util import process_source


class ObjectTracker(BaseTracker):
    def __init__(self, source=0,model_name="yolo-highway-v2.pt", lines_coords=[]):
        """
        Initializes the ObjectTracker.

        Args:
            source (str or int): The path to the video source or camera index. Default is 0 (camera).
            lines_coords (list): The coordinates of the counting lines. One example is [(268,435),(592,447)],
                                 [(600,450),(950,450)].
        """
        super().__init__(source,model_name)
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.model = self.load_model()
    
        #! Check the available device (CPU or GPU)
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print("Using Device: ", self.device)

        #? Get the class names from the model
        self.class_name_dict = self.model.model.names
        
        #% Initialize the box annotator for drawing bounding boxes and labels
        self.box_annotator = sv.BoxAnnotator(
            color=sv.ColorPalette.default(), thickness=2, text_thickness=1, text_scale=0.5, text_padding=2)
   

        #% Create instances of Line, TotalCountRectangle, and SpeedEstimation classes
        self.speed_estimation = SpeedEstimation(class_name_dict=self.class_name_dict,box_annotator=self.box_annotator)
        self.lines = [Line(self.class_name_dict, line_coord=coords) for coords in lines_coords]
        self.total_counts = TotalCountRectangle(self.class_name_dict)

    def load_model(self):
        """
        Loads the YOLO model.

        Returns:
            YOLO: The loaded YOLO model.
        """
        model_path = os.path.join(
            self.current_dir, "models",self.model_name)
        model = YOLO(model=model_path)
        model.fuse()
        return model

    def convert_result_to_detections(self, result):
        """
        Converts the YOLO result into Detections format.

        Args:
            result: The result from YOLO model.

        Returns:
            Detections: The converted detections.
        """
        detections = sv.Detections(
            xyxy=result.boxes.xyxy.cpu().numpy(),
            confidence=result.boxes.conf.cpu().numpy(),
            class_id=result.boxes.cls.cpu().numpy().astype(int),
            # tracker_id=result.boxes.id.cpu().numpy().astype(int)
        )
        if result.boxes.id is not None:
            detections.tracker_id = result.boxes.id.cpu().numpy().astype(int)
        return detections
    
    def process_frame(self, result, frame_counter_for_tracker_id, speed):
        """
        Processes a single frame of the video stream.

        Args:
            result: The result of the YOLO model's track method for the current frame.
            frame_counter_for_tracker_id: A dictionary storing the frame counter for each object tracker.
            speed: The current speed value.

        Returns:
            The annotated frame with object detections and counters.
        """
        frame = result.orig_img

        detections = self.convert_result_to_detections(result)
    
        #? Count objects and update counts for each object (rectangle and lines)
        for line in self.lines:
            line.count(detections)
        self.total_counts.count(detections)

        #? Add object annotations to the frame
        frame_counter_for_tracker_id =  self.speed_estimation.update_speed_and_frame_counter(speed,
                                        detections,frame_counter_for_tracker_id)
        self.speed_estimation.update_tracked_coordinates()
        frame = self.speed_estimation.add_annotations_to_frame(frame, detections)

        #% Draw lines and total counts
        for line in self.lines:
            frame = line.draw_line(frame)
        frame = self.total_counts.draw(frame)

        return frame, frame_counter_for_tracker_id

    def show(self):
        """
        Runs the object tracking and counting process and displays the processed video frames on the screen.

        Processed frames include object detections, counting lines, total counts and speed estimations. 
        The display will stop when the 'ESC' key is pressed.
        """
        frame_counter_for_tracker_id = {}
        speed = 0
        if (self.is_youtube_url(str(self.source))):
            video = pafy.new(self.source)
            best = video.getbest(preftype="mp4")
            cap = cv2.VideoCapture(best.url)
        else:
            cap = cv2.VideoCapture(self.source)

        assert cap.isOpened()
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        while True:
            ret, frame = cap.read()
            assert ret
            for result in self.model.track(source=frame,persist=True, stream=True, agnostic_nms=True, tracker="bytetrack.yaml"):

                frame, frame_counter_for_tracker_id = self.process_frame(result, frame_counter_for_tracker_id, speed)
            cv2.imshow("yolov8", frame)
            if (cv2.waitKey(30) == 27):
                break
        cv2.destroyAllWindows()


    def __call__(self):
        """
        Runs the object tracking and counting process.
        """
        frame_counter_for_tracker_id = {}
        speed = 0
        
        if (self.is_youtube_url(str(self.source))):
            video = pafy.new(self.source)
            best = video.getbest(preftype="mp4")
            cap = cv2.VideoCapture(best.url)
        else:
            cap = cv2.VideoCapture(process_source(self.source))

        assert cap.isOpened()
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        while True:
            ret, frame = cap.read()
            assert ret
            for result in self.model.track(source=frame,persist=True, stream=True, agnostic_nms=True, tracker="bytetrack.yaml"):

                frame, frame_counter_for_tracker_id = self.process_frame(result, frame_counter_for_tracker_id, speed)
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(frame) + b'\r\n')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='YOLO Object Tracker')
    parser.add_argument('--source', type=process_source, default=0, help='source video file path')
    parser.add_argument('--model', type=str, default='yolo-highway-v2.pt', help='model name')
    args = parser.parse_args()

    tracker = ObjectTracker(source=args.source, model_name=args.model)
    tracker.show()