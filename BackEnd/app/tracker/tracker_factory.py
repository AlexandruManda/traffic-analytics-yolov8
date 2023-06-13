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
    def get_tracker(task, source, line1=None, line2=None):
        """
        Returns a tracker object based on the task type.

        Args:
            task (str): The task type. Valid options are "traffic" and "person".
            source (str): The video source for the tracker.
            line1 (str or None): The first line for the traffic tracker, if applicable.
            line2 (str or None): The second line for the traffic tracker, if applicable.

        Returns:
            An instance of a tracker object if the task type is valid, otherwise None.
        """
        tracker_type_map = {
            "traffic": TrackerFactory.create_traffic_tracker,
            "person": TrackerFactory.create_person_tracker,
        }

        create_func = tracker_type_map.get(task)
        if create_func:
            return create_func(source, line1, line2)

        return None

    @staticmethod
    def create_traffic_tracker(source, line1, line2):
        """
        Returns a traffic tracker object.

        Args:
            source (str): The video source for the tracker.
            line1 (str or None): The first line for the tracker.
            line2 (str or None): The second line for the tracker.

        Returns:
            An instance of ObjectTracker.
        """
        lines_list = []
        param_helper = QueryParamHelper()
        if line1 and line2:
            lines_list.append(param_helper.convert_query_param_to_tuples(line1))
            lines_list.append(param_helper.convert_query_param_to_tuples(line2))

      
        return ObjectTracker(source=source, lines_coords=lines_list)



    @staticmethod
    def create_person_tracker(source, line1, line2):
        """
        Returns a person tracker object.

        Args:
            source (str): The video source for the tracker.
            line1 (str or None): Unused.
            line2 (str or None): Unused.

        Returns:
            An instance of PersonDetectionTracker.
        """
        return PersonDetectionTracker(source=source)