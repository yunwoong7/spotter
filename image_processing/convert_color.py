import cv2
from image_processing import get_type, convert_image

def grayScale(image):
    '''
    회색조 이미지로 변경
    :param image: (bytes) or (pil.image) or (numpy array) or (qimage)
    :return: (bytes) or (pil.image) or (numpy array) or (qimage)
    '''
    image_type = get_type(image)
    gray = convert_image(image, 'cv2')

    if len(gray.shape) >= 3:
        gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
        gray = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)
    else:
        print("Skip grayscle (channel : {})".format(len(gray.shape)))

    gray = convert_image(gray, image_type)

    return gray