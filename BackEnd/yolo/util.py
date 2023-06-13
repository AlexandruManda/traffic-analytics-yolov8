import cv2
import numpy as np
import base64
import math

def decode_base64to_mat(image_url: str):
    """
    Decode a Base64 image string and create an OpenCV Mat image.

    Args:
        image_url (str): The URL that holds the Base64 encoded image.

    Returns:
        np.ndarray: The decoded image as an OpenCV Mat.
    """

    image_base64 = image_url.split(",")[1]
    image_bytes = base64.b64decode(image_base64)
    image_nparray = np.asarray(bytearray(image_bytes), dtype="uint8")
    image_cvmat = cv2.imdecode(image_nparray, cv2.IMREAD_COLOR)
    return image_cvmat


def encode_mat_base64(cvmat):
    """
    Encode an OpenCV Mat image to Base64.

    Args:
        cvmat (np.ndarray): The image as an OpenCV Mat.

    Returns:
        str: The Base64 encoded image URL.
    """
   
    ret, buffer = cv2.imencode('.jpg', cvmat)
    encoded = base64.b64encode(buffer).decode("utf-8")

    return "data:image/jpg;base64," + encoded

def resize_image(image, width=None, height=None):
    """
    Resize the image to the specified width and height.

    Args:
        image (np.ndarray): The image to resize.
        width (int, optional): The desired width. If not provided, the original width is used.
        height (int, optional): The desired height. If not provided, the original height is used.

    Returns:
        np.ndarray: The resized image.
    """

    dimensions = image.shape
    width = width if width else dimensions[1]
    height = height if height else dimensions[0]

    return cv2.resize(image, (width, height))

def compress_image(image, quality=90):
    """
    Compress the image using JPEG compression.

    Args:
        image (np.ndarray): The image to compress.
        quality (int, optional): The compression quality. Default is 90.

    Returns:
        np.ndarray: The compressed image.
    """

    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
    result, encimg = cv2.imencode('.jpg', image, encode_param)
    decimg = cv2.imdecode(encimg, 1)
    return decimg

def get_class_color(cls):
    """
    Get the color associated with a specific class.

    Args:
        cls (str): The class name.

    Returns:
        tuple: The RGB color value as a tuple.
    """

    if cls == 'car':
        color = (204, 51, 0)
    elif cls == 'truck':
        color = (22,82,17)
    elif cls == 'motorcycle':
        color = (255, 0, 85)
    else:
        color = [int((p * (2 ** 2 - 14 + 1)) % 255) for p in palette]
    return tuple(color)

def compute_center(x1,y1,x2,y2):
    """
    Compute the center coordinates of a bounding box.

    Args:
        x1 (int): The x-coordinate of the top-left corner.
        y1 (int): The y-coordinate of the top-left corner.
        x2 (int): The x-coordinate of the bottom-right corner.
        y2 (int): The y-coordinate of the bottom-right corner.

    Returns:
        list: The [x, y] coordinates of the center point.
    """
    w  = x2-x1
    h = y2-y1
    cx, cy = x1+w//2, y1+h//2
    return [cx,cy]

def estimated_speed(location1, location2):
    """
    Estimate the speed between two locations based on Euclidean distance.

    Args:
        location1 (list): The first location coordinates [x1, y1, x2, y2].
        location2 (list): The second location coordinates [x1, y1, x2, y2].

    Returns:
        int: The estimated speed in km/h.
    """
    #Euclidean distance formula
    x1_l1,y1_l1,x2_l1,y2_l1 = location1[0]
    x1_l2,y1_l2,x2_l2,y2_l2 = location2[0]
    location_1 = compute_center(x1_l1,y1_l1,x2_l1,y2_l1)
    location_2 = compute_center(x1_l2,y1_l2,x2_l2,y2_l2) 
    d_pixel = math.sqrt(math.pow(location_2[0]-location_1[0], 2) + math.pow(location_2[1]-location_1[1], 2))

    ppm = 2 # This value could me made dynamic depending on how close the object is from the camera
    d_meters = d_pixel/ppm
    
    time_constant = 15*3.6

    speed = (d_meters * time_constant)/100
    return int(speed)


def process_source(source):
    """Convert source to integer if possible."""
    try:
        return int(source)
    except ValueError:
        return source

