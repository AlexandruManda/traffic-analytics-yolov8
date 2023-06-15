import os
import cv2
import torch
import pafy
import numpy as np
import argparse
import supervision as sv
from ultralytics import YOLO

try:
    from yolo.base.base_tracker import BaseTracker
    from yolo.classes.person_count import PersonCount
    from yolo.util import process_source
except ImportError:
    from base.base_tracker import BaseTracker
    from classes.person_count import PersonCount
    from util import process_source

class PersonDetectionTracker(BaseTracker):
    def __init__(self,
                 source=0,
                 model_name="yolov8m.pt", 
                 box_thickness=2, 
                 text_thickness=1, 
                 text_scale=0.5, 
                 text_padding=2,
                 counter_text_font=cv2.FONT_HERSHEY_SIMPLEX, 
                 counter_text_scale=1, 
                 counter_text_color=(255, 255, 255), 
                 counter_text_thickness=2
                 ):
                 
        super().__init__(source=source,model_name=model_name)
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.model = self.load_model()
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print("Using Device: ", self.device)
          #? Get the class names from the model
        self.class_name_dict = self.model.model.names
        
        #% Initialize the box annotator for drawing bounding boxes and labels
        self.box_annotator = sv.BoxAnnotator(
                color=sv.ColorPalette.default(), 
                thickness=box_thickness, 
                text_thickness=text_thickness, 
                text_scale=text_scale, 
                text_padding=text_padding
            )

        self.person_counter = PersonCount(self.class_name_dict, 
                                          counter_text_font, 
                                          counter_text_scale, 
                                          counter_text_color, 
                                          counter_text_thickness)
 
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

    def process_frame(self,result):
        """
        Processes a single frame of the video stream.

        Args:
            result: The detection result from the YOLO model.

        Returns:
            ndarray: The processed frame.
        """
        frame = result.orig_img
        person_detections = self.convert_result_to_detections(result)
  
        self.person_counter.count(person_detections)
        frame = self.person_counter.draw(frame)
        frame = self.annotate_frame(frame,person_detections)
        return frame
       
    def convert_result_to_detections(self, result):
        """
        Converts the YOLO result into a Detections format.

        Args:
            result: The result from YOLO model.

        Returns:
            Detections: The converted detections which includes only the 'person' class.
        """
       
        detections = sv.Detections(
            xyxy=result.boxes.xyxy.cpu().numpy(),
            confidence=result.boxes.conf.cpu().numpy(),
            class_id=result.boxes.cls.cpu().numpy().astype(int),
            # tracker_id=result.boxes.id.cpu().numpy().astype(int)
        )
        if result.boxes.id is not None:
            detections.tracker_id = result.boxes.id.cpu().numpy().astype(int)
   

        #% Filter out only 'person' detections
        person_class_id = next((key for key, value in self.class_name_dict.items() if value == 'person'), None)
        person_detections_indices = np.where(detections.class_id == person_class_id)
    
        #? Create new Detections object for 'person' detections only
        person_detections = sv.Detections(
            xyxy=detections.xyxy[person_detections_indices],
            confidence=detections.confidence[person_detections_indices],
            class_id=detections.class_id[person_detections_indices],
        )
        if detections.tracker_id is not None:
            person_detections.tracker_id = detections.tracker_id[person_detections_indices]

        return person_detections
    
    def annotate_frame(self,frame,person_detections):
        """
        Annotates the frame with bounding boxes and labels.

        Args:
            frame (ndarray): The frame to be annotated.
            person_detections (Detections): The detections to be annotated on the frame.

        Returns:
            ndarray: The annotated frame.
        """
        self.labels = [f"#{tracker_id} {self.class_name_dict[class_id]} {confidence:.2f} "
                            for _, confidence, class_id, tracker_id in zip(person_detections.xyxy, person_detections.confidence, person_detections.class_id, person_detections.tracker_id)] if person_detections.tracker_id is not None else [f"{self.class_name_dict[class_id]} {confidence:.2f} "
                            for _, confidence, class_id in zip(person_detections.xyxy, person_detections.confidence, person_detections.class_id)]

        # Annotate and display frame
        frame = self.box_annotator.annotate(
            scene=frame, detections=person_detections, labels=self.labels)
        
        return frame
    def show(self):
        """
        Runs the tracking process and displays the processed video frames on the screen.
        The source of the video could be a local file or a YouTube URL.
        """
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
     
                frame = self.process_frame(result)
              
                
            cv2.imshow("yolov8", frame)
            if (cv2.waitKey(30) == 27):
                break
        cv2.destroyAllWindows()

    def __call__(self):
        """
        Runs the tracking process and yields each frame in byte form.
        The source of the video could be a local file or a YouTube URL.
        """
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
     
                frame = self.process_frame(result)
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(frame) + b'\r\n')



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='YOLO Object Tracker')
    parser.add_argument('--source', type=str, default=0, help='source video file path')
    parser.add_argument('--model', type=str, default='yolov8m.pt', help='model name')
    args = parser.parse_args()

    detector = PersonDetectionTracker(source=args.source, model_name=args.model)
    detector.show()