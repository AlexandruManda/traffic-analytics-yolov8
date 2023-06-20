
import cv2 

try:
    from yolo.util import compute_center
except ImportError:
    from util import compute_center


                                       # -? ------------------------
                                       # -?         |    |    |    |
                                       # -?         v    v    v    v
                                       # -%         x1   y1   x2   y2
class Line:
    def __init__(self,
                 class_names_dict,
                 line_coord=[(268,435),(592,447)],
                 line_color=(0, 0, 255),
                 text_color=(255, 255, 255),
                 line_font=cv2.FONT_HERSHEY_SIMPLEX,
                 line_font_scale=1,
                 line_thickness=2,
                 text_thickness=2):
        
        self.total_objects_count = 0
        self.counted_objects = set()
        self.line_limits=line_coord
        self.class_names_dict=class_names_dict
        self.class_object_counts={'car':0,'motorcycle':0,'bus':0,'truck':0}
        self.line_coord = line_coord


        self.line_color = line_color
        self.text_color = text_color
        self.line_font = line_font
        self.line_font_scale = line_font_scale
        self.line_thickness = line_thickness
        self.text_thickness = text_thickness

                                     
    def draw(self, frame):
        """
        Draws a line on the given frame.

        Args:
            frame (ndarray): The frame on which to draw the line.
            color (tuple): The color of the line in BGR format. Default is (0, 0, 255).
            font_scale (float): The scale of the font text for counter. Default is 1.
            thickness (int): The thickness of the line. Default is 2.
        Returns:
            ndarray: The frame with the counter text.
        """
        start_point = self.line_coord[0]
        end_point = self.line_coord[1]
        cv2.line(frame, start_point, end_point, self.line_color, self.line_thickness)
        self.draw_counter_on_line(frame)
        return frame


    def draw_counter_on_line(self,frame):
        """
        Draws the counter text on the frame.

        Args:
            frame (ndarray): The frame on which to draw the counter text.
            font_scale (float): The scale of the font. Default is 1.
            thickness (int): The thickness of the text. Default is 2.

        Returns:
            ndarray: The frame with the counter text.
        """
        x1 = self.line_limits[0][0]
        y1 = self.line_limits[0][1] - 10  # Move text a bit above the line
        counter_text = f"{self.total_objects_count}"

        cv2.putText(frame, counter_text, (x1, y1), self.line_font, self.line_font_scale, self.text_color, self.text_thickness)
        return frame
    
    def count(self, detections):  
        """
        Counts the objects crossing the given line.
        Needs to be called after detections are coming from the model each frame

        Args:
          
            detections (Detections): The detections of objects.
        """
        for xyxy, _, class_id, tracker_id in detections:
            x1,y1,x2,y2=xyxy
            cx,cy = compute_center(x1,y1,x2,y2)
            class_name = self.class_names_dict[class_id]
            if self.line_limits[0][1] -15 < cy < self.line_limits[1][1] +15  and self.line_limits[0][0] < cx < self.line_limits[1][0] :
                if tracker_id not in self.counted_objects.copy():
                    self.total_objects_count +=1
                    self.class_object_counts[class_name] +=1
                    self.counted_objects.add(tracker_id)
    