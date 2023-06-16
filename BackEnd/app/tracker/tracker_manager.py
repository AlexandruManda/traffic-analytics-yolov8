

import cv2
from flask import g
try:
    from app.tracker.tracker_factory import TrackerFactory
    from app.db import get_db
    from ..utils.query_params_helper import QueryParamHelper
except ImportError:
    from BackEnd.app.tracker.tracker_factory import TrackerFactory
    from utils.query_params_helper import QueryParamHelper

class TrackerManager:
    def __init__(self):
        self.db = get_db()

    def create_tracker(self, task, source, line1, line2):
        """
        Creates and returns a tracker object.

        Args:
            task (str): The type of the task (e.g., "traffic", "person").
            source (str): The video source for the tracker.
            line1, line2: Additional parameters for the tracker.

        Returns:
            An instance of a tracker object.
        """
        TrackerClass = TrackerFactory.get_tracker_class(task)

        if not TrackerClass:
            return None

        if task == "traffic":
            tracker_config = self.get_config_from_db(task)
            lines_coords = []
            param_helper = QueryParamHelper()

            if line1 and line2:
                lines_coords.append(param_helper.convert_query_param_to_tuples(line1))
                lines_coords.append(param_helper.convert_query_param_to_tuples(line2))

            return TrackerClass(source=source, lines_coords=lines_coords, **tracker_config)
        else:
            tracker_config = self.get_config_from_db(task)
            return TrackerClass(source=source, **tracker_config)

    def get_config_from_db(self, task):
        """
        Retrieves the configuration for a tracker from the database.

        Args:
            task (str): The type of the task (e.g., "person").

        Returns:
            A dictionary with the configuration for the tracker.
        """
        # Retrieve configuration from MongoDB
        config = self.db.trackerConfig.find_one({"task": task})

        if not config:
            raise Exception(f"No configuration found for task {task}")

        config = self.process_config(task, config)

        # Exclude _id and task from config
        return {k: v for k, v in config.items() if k not in ["_id", "task"]}
    


    def process_config(self, task, config):
        """
        Processes the configuration for a tracker based on the task type.

        Args:
            task (str): The type of the task (e.g., "person").
            config (dict): The configuration from the database.

        Returns:
            The processed configuration.
        """
        if task == "traffic":
            # Update config keys and values based on ObjectTracker constructor
            config["model_name"] = config.get("model_name", "yolo-highway-v2.pt")
            config["line_color"] = tuple(config.get("line_color", (0, 0, 255)))
            config["text_color"] = tuple(config.get("text_color", (255, 255, 255)))
            config["line_font"] = getattr(cv2, config.get("line_font", "FONT_HERSHEY_SIMPLEX"))
            config["line_font_scale"] = config.get("line_font_scale", 1)
            config["line_thickness"] = config.get("line_thickness", 2)
            config["text_thickness"] = config.get("text_thickness", 2)
            config["box_thickness"] = config.get("box_thickness", 2)
            config["box_text_thickness"] = config.get("box_text_thickness", 1)
            config["box_text_scale"] = config.get("box_text_scale", 0.5)
            config["box_text_padding"] = config.get("box_text_padding", 2)

        elif task == "person":
            # Update config keys and values based on PersonDetectionTracker constructor
            config["model_name"] = config.get("model_name", "yolov8m.pt")
            config["box_thickness"] = config.get("box_thickness", 2)
            config["text_thickness"] = config.get("text_thickness", 1)
            config["text_scale"] = config.get("text_scale", 0.5)
            config["text_padding"] = config.get("text_padding", 2)
            config["counter_text_font"] = getattr(cv2, config.get("counter_text_font", "FONT_HERSHEY_SIMPLEX"))
            config["counter_text_scale"] = config.get("counter_text_scale", 1)
            config["counter_text_color"] = tuple(config.get("counter_text_color", (255, 255, 255)))
            config["counter_text_thickness"] = config.get("counter_text_thickness", 2)

        return config
