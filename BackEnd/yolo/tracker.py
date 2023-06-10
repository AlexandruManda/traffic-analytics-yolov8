import sys
import os
from ultralytics import YOLO
import cv2
import supervision as sv
import torch
from queue import Queue
from threading import Thread
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from util import estimated_speed,compute_center


class ObjectTracker:
    def __init__(self, source_path=0,lines_coords=[[(268,435),(592,447)],[(600,450),(950,450)]]):
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.model = self.load_model()
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print("Using Device: ", self.device)
        self.class_name_dict = self.model.model.names
        self.box_annotator = sv.BoxAnnotator(
            color=sv.ColorPalette.default(), thickness=2, text_thickness=1, text_scale=0.5, text_padding=2)
        self.source_path = source_path
        self.coordinatesDict = {}
        self.updated_trackers_speed = {}
        self.total_objects_count1 = 0
        self.counted_objects1 = set()
        self.total_objects_count2 = 0
        self.counted_objects2 = set()
        self.class_object_counts={'car':0,'motorcycle':0,'bus':0,'truck':0}
        self.line_limits1=lines_coords[0]
        self.line_limits2=lines_coords[1]

    def set_source_path(self, source_path):
        self.source_path = source_path

    def load_model(self):
        model_path = os.path.join(
            self.current_dir, 'runs', 'detect', 'train-v2', 'weights', 'best.pt')
        model = YOLO(model=model_path)
        model.fuse()
        return model

                                
                                        # -? ------------------------------------------
                                        # -?          |    |                |    |
                                        # -?          v    v                v    v
                                        # -%          x1   y1               x2   y2
    def draw_line_on_frame(self, frame, start_point=(650, 450), end_point=(1000, 450), color=(0, 0, 255), thickness=2):
        cv2.line(frame, start_point, end_point, color, thickness)

    def get_detections(self,result):
        detections = sv.Detections(
                xyxy=result.boxes.xyxy.cpu().numpy(),
                confidence=result.boxes.conf.cpu().numpy(),
                class_id=result.boxes.cls.cpu().numpy().astype(int),
                # tracker_id=result.boxes.id.cpu().numpy().astype(int)
            )
        if result.boxes.id is not None:
                detections.tracker_id = result.boxes.id.cpu().numpy().astype(int)
        return detections
    
    def calculate_speed(self,speed,detections,frame_counter):
        self.updated_trackers_speed = {}
        if len(detections) > 0:
            for detection in detections:
                tracker_id = detection[-1]
                current_location = detection[:4]
                if tracker_id in self.coordinatesDict:
                    if tracker_id not in frame_counter:
                        frame_counter[tracker_id] = 0
                    prev_location = self.coordinatesDict[tracker_id][0]
                    if frame_counter[tracker_id] == 2:
                        speed = estimated_speed(prev_location, current_location)
                        self.updated_trackers_speed[tracker_id] = [current_location, speed]
                        self.coordinatesDict[tracker_id] = self.updated_trackers_speed[tracker_id]
                        frame_counter[tracker_id] = 0
                    frame_counter[tracker_id] += 1
                else:
                    self.updated_trackers_speed[tracker_id] = [current_location, speed]
                    self.coordinatesDict[tracker_id] = [current_location, speed]
                    
        return frame_counter
    
    def update_coordinates_dict(self):
        for key in self.updated_trackers_speed.keys():
            if key not in self.coordinatesDict:
                self.coordinatesDict.pop(key, None)

    def annotate_frame(self,frame,detections):
        self.labels = [f"#{tracker_id} {self.class_name_dict[class_id]} {self.coordinatesDict[tracker_id][1]} km/h"
                           for _, confidence, class_id, tracker_id
                           in detections]
        return self.box_annotator.annotate(
                scene=frame, detections=detections, labels=self.labels)
    
    def draw_counter_text(self,frame, line_limits, counter_text, font_scale=1, thickness=2):
        x1 = line_limits[0][0]
        y1 = line_limits[0][1] - 10  # Move text a bit above the line
        cv2.putText(frame, counter_text, (x1, y1),
                    cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), thickness)
        return frame
    def count_class_objects_line(self, line_limits, detections, counted_objects, total_objects_count):  
        for xyxy, _, class_id, tracker_id in detections:
            x1,y1,x2,y2=xyxy
            cx,cy = compute_center(x1,y1,x2,y2)
            class_name = self.class_name_dict[class_id]
            if line_limits[0][1] -15 < cy < line_limits[1][1] +15  and line_limits[0][0] < cx < line_limits[1][0] :
                if tracker_id not in counted_objects.copy():
                    total_objects_count +=1
                    self.class_object_counts[class_name] +=1
                    counted_objects.add(tracker_id)
        return total_objects_count, counted_objects
    
    def __call__(self):
        frame_counter = {}
        speed = 0
        for result in self.model.track(source=self.source_path, stream=True, agnostic_nms=True, tracker="bytetrack.yaml"):
            frame = result.orig_img
            self.line_limits1
            self.draw_line_on_frame(frame,start_point = self.line_limits1[0],end_point=self.line_limits1[1])
            self.draw_line_on_frame(frame,start_point = self.line_limits2[0],end_point=self.line_limits2[1])
            detections = self.get_detections(result)

            self.total_objects_count1, self.counted_objects1 = self.count_class_objects_line(
                self.line_limits1, detections, self.counted_objects1, self.total_objects_count1)

            self.total_objects_count2, self.counted_objects2 = self.count_class_objects_line(
                self.line_limits2, detections, self.counted_objects2, self.total_objects_count2)

            frame = self.draw_counter_text(frame, self.line_limits1, str(self.total_objects_count1))
            frame = self.draw_counter_text(frame, self.line_limits2, str(self.total_objects_count2)) # text for second line

            frame_counter = self.calculate_speed(speed,detections,frame_counter)
            self.update_coordinates_dict()


            frame = self.annotate_frame(frame,detections)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(frame) + b'\r\n')
            
        #     cv2.imshow("yolov8", frame)
        #     if (cv2.waitKey(30) == 27):
        #         break

        # cv2.destroyAllWindows()


if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    source_path = os.path.join(current_dir, 'assets', 'videos', '1.mp4')
    # source_path="https://www.youtube.com/watch?v=lPjevDc5G8E"
    # source_path="https://www.youtube.com/watch?v=MNn9qKG2UFI&list=PLcQZGj9lFR7y5WikozDSrdk6UCtAnM9mB"
    tracker = ObjectTracker(source_path=source_path)
    tracker()
