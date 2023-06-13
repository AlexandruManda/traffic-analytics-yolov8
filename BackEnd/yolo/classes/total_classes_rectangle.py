import os
import cv2
import cvzone

try:
    from yolo.base.base_counter import BaseCounter
except ImportError:  
    from base.base_counter import BaseCounter

class TotalCountRectangle(BaseCounter):
    def __init__(self,class_names_dict):
        """
        Initializes the TotalCountRectangle class.

        Args:
            class_names_dict (dict): A dictionary mapping class IDs to class names.
        """
        self.total_objects_count = 0
        self.total_classes_counted = set()
        self.total_class_object_counts = {
            'car': 0, 
            'motorcycle': 0, 
            'bus': 0, 
            'truck': 0
            }
        self.class_names_dict=class_names_dict
        self.current_dir = os.path.join(os.path.dirname(os.path.dirname((os.path.abspath(__file__)))))
        self.img_path = os.path.join(self.current_dir, "assets", "Images", "counter.png")
        self.boxes_image = cv2.imread(self.img_path, cv2.IMREAD_UNCHANGED)

    def draw(self, frame):
        """
        Draws the class boxes on the frame.

        Args:
            frame (ndarray): The frame to draw the total class count on.

        Returns:
            ndarray: The frame with the total class PNG image overlay over frame.
        """
        _, frame_width = frame.shape[:2]
        boxes_image_height, boxes_image_width = self.boxes_image.shape[:2]

        pos_x = int((frame_width - boxes_image_width) / 2)
        pos_y = 0
        pos = [pos_x, pos_y]

        frame = cvzone.overlayPNG(frame, self.boxes_image, pos)
        cv2.putText(frame, f"{self.total_class_object_counts['car']}", (pos_x+20, pos_y+15 + int(boxes_image_height/2)),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(frame, f"{self.total_class_object_counts['motorcycle']}", (pos_x+170, pos_y+15 + int(boxes_image_height/2)),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(frame, f"{self.total_class_object_counts['bus']}", (pos_x+320, pos_y+15 + int(boxes_image_height/2)),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(frame, f"{self.total_class_object_counts['truck']}", (pos_x+465, pos_y+15 + int(boxes_image_height/2)),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        return frame
    
    def count(self, detections):  
        """
        Counts all the objects that are passing over in the frame
        Needs to be called after detections are coming from the model each frame
        Args:
          
            detections (Detections): The detections of objects.
        """
        if len(detections) >0:
            for _, _, class_id, tracker_id in detections:
                class_name = self.class_names_dict[class_id]
                if tracker_id not in self.total_classes_counted.copy():
                    self.total_objects_count +=1
                    self.total_class_object_counts[class_name] +=1
                    self.total_classes_counted.add(tracker_id)

    