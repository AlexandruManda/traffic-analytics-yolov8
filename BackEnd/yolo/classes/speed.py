try:
    from yolo.util import estimated_speed
except ImportError:
    from util import estimated_speed
    
class SpeedEstimation:
    def __init__(self,class_name_dict,box_annotator,frame_interval_for_speed=20):
        """
        Initialize the SpeedEstimation class.

        Args:
            class_name_dict (dict): A dictionary mapping class IDs to class names.
            box_annotator (BoxAnnotator): An instance of the BoxAnnotator class for adding annotations to frames.
        """
        self.coordinatesDict = {}
        self.updated_trackers_speed = {}
        self.class_name_dict=class_name_dict
        self.box_annotator=box_annotator
        self.frame_interval_for_speed=frame_interval_for_speed

    def update_speed_and_frame_counter(self, speed, detections, frame_counter_for_tracker_id):
        """
        Calculates the speed of objects based on their detections.

        Args:
            speed (int): The initial speed value.
            detections (Detections): The detections of objects.
            frame_counter_for_tracker_id (dict): The frame counter for each object tracker.

        Returns:
            dict: The updated frame counter for each object tracker.
        """
        self.updated_trackers_speed = {}
        if len(detections) > 0:
            for detection in detections:
                tracker_id = detection[-1]
                current_location = detection[:4]

                if tracker_id in self.coordinatesDict:
                    if tracker_id not in frame_counter_for_tracker_id:
                        frame_counter_for_tracker_id[tracker_id] = 0
                    prev_location = self.coordinatesDict[tracker_id][0]
                    if frame_counter_for_tracker_id[tracker_id] == self.frame_interval_for_speed:
                        #? Calculate the speed based on the previous and current location
                        speed = estimated_speed(prev_location, current_location)
                        #% Store the updated speed and current location in the dictionary
                        self.updated_trackers_speed[tracker_id] = [current_location, speed]
                        self.coordinatesDict[tracker_id] = self.updated_trackers_speed[tracker_id]
                        frame_counter_for_tracker_id[tracker_id] = 0
                    frame_counter_for_tracker_id[tracker_id] += 1
                else:
                    # * If it's a new tracker, store the initial speed and current location
                    self.updated_trackers_speed[tracker_id] = [current_location, speed]
                    self.coordinatesDict[tracker_id] = [current_location, speed]

        return frame_counter_for_tracker_id
    
    def update_tracked_coordinates(self):
        """
        Updates the coordinates dictionary by removing expired trackers.
        """
        for key in self.updated_trackers_speed.keys():
            if key not in self.coordinatesDict:
                self.coordinatesDict.pop(key, None)
    
    def add_annotations_to_frame(self, frame, detections):
        self.labels = [f"#{tracker_id} {self.class_name_dict[class_id]} {self.coordinatesDict[tracker_id][1]} km/h"
                       for _, confidence, class_id, tracker_id in detections]
        return self.box_annotator.annotate(scene=frame, detections=detections, labels=self.labels)