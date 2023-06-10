import cv2
import numpy as np
import base64
import math

def decode_base64to_mat(image_url: str):
    '''
    decode_base64to_mat creates an OpenCV Mat image type from a Base64 URL image string

    :image_url: URL which holds the base64 encoded image in string format
    :return: cv::Mat of the decoded image
    '''

    image_base64 = image_url.split(",")[1]
    image_bytes = base64.b64decode(image_base64)
    image_nparray = np.asarray(bytearray(image_bytes), dtype="uint8")
    image_cvmat = cv2.imdecode(image_nparray, cv2.IMREAD_COLOR)
    return image_cvmat


def encode_mat_base64(cvmat):
    '''
    encode_mat_base64 creates a base64 encoded URL from cv::Mat type

    :cvmat: cv::Mat type image to be encoded
    :return: str containing base64 encoded image URL
    '''
    ret, buffer = cv2.imencode('.jpg', cvmat)
    encoded = base64.b64encode(buffer).decode("utf-8")

    return "data:image/jpg;base64," + encoded

def resize_image(image, width=None, height=None):
    dimensions = image.shape
    width = width if width else dimensions[1]
    height = height if height else dimensions[0]

    return cv2.resize(image, (width, height))

def compress_image(image, quality=90):
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
    result, encimg = cv2.imencode('.jpg', image, encode_param)
    decimg = cv2.imdecode(encimg, 1)
    return decimg

def get_class_color(cls):
    """
    Simple function that adds fixed color depending on the class
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
    w  = x2-x1
    h = y2-y1
    cx, cy = x1+w//2, y1+h//2
    return [cx,cy]

def estimated_speed(location1, location2):
    #Euclidean distance formula
    x1_l1,y1_l1,x2_l1,y2_l1 = location1[0]
    x1_l2,y1_l2,x2_l2,y2_l2 = location2[0]
    location_1 = compute_center(x1_l1,y1_l1,x2_l1,y2_l1)
    location_2 = compute_center(x1_l2,y1_l2,x2_l2,y2_l2) 
    d_pixel = math.sqrt(math.pow(location_2[0]-location_1[0], 2) + math.pow(location_2[1]-location_1[1], 2))

    ppm = 2 # This value could me made dynamic depending on how close the object is from the camera
    d_meters = d_pixel/ppm
    time_constant = 30*3.6

    speed = (d_meters * time_constant)/100
    return int(speed)

def estimatedSpeed(location1, location2):
    #Euclidean distance formula
    d_pixel = math.sqrt(math.pow(location2[0] - location1[0], 2) + math.pow(location2[1] - location1[1], 2))
    # setting the pixels per meter 
    ppm = 2 # This value could me made dynamic depending on how close the object is from the camera
    d_meters = d_pixel/ppm
    time_constant = 15*3.6

    speed = (d_meters * time_constant)/100
    return int(speed)