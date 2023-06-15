from yolo.car_tracker import ObjectTracker
from yolo.person_count_tracker import PersonDetectionTracker

try:
    from ..utils.query_params_helper import QueryParamHelper
except ImportError:
    from utils.query_params_helper import QueryParamHelper


class TrackerFactory:
    """
    Factory class for creating tracker objects.

    This class provides static methods to create different types of tracker
    objects based on the task type, such as "traffic" and "person".

    Typical usage example:

    tracker = TrackerFactory.get_tracker("traffic", source, line1, line2)
    """
    @staticmethod
    def get_tracker_class(task):
        """
        Returns the class of the tracker based on the task type.

        Args:
            task (str): The task type. Valid options are "traffic" and "person".

        Returns:
            The class of the corresponding tracker if the task type is valid, otherwise None.
        """
        tracker_type_map = {
            "traffic": ObjectTracker,
            "person": PersonDetectionTracker,
        }

        return tracker_type_map.get(task)