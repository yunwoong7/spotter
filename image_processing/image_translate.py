import cv2
import imutils
from imutils.perspective import four_point_transform
from image_processing import get_type, convert_image
from image_processing.edge_detectors.hed import HED

HED_DETECTION_MODEL = HED()

def cannyScan(image, width, ksize=(5, 5), min_threshold=75, max_threshold=200):
    '''
    OpenCV Canny를 이용하여 윤곽선을 찾아 꼭지점을 이용하여 이미지를 보정
    :param image: (bytes) or (pil.image) or (numpy array) or (qimage)
    :param width: (int)
    :param ksize: (tuple)
    :param min_threshold: (int)
    :param max_threshold: (int)
    :return: (bytes) or (pil.image) or (numpy array) or (qimage)
    '''
    transform_image = image.copy()
    image_type = get_type(image)
    org_image = convert_image(image, 'cv2')
    image = imutils.resize(org_image, width=width)

    ratio = org_image.shape[1] / float(image.shape[1])

    # 이미지를 grayscale로 변환하고 blur를 적용
    # 모서리를 찾기위한 이미지 연산
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, ksize, 0)
    edged = cv2.Canny(blurred, min_threshold, max_threshold)

    findCnt = find_contours(edged)

    if findCnt is not None:
        transform_image = four_point_transform(org_image, findCnt.reshape(4, 2) * ratio)
        transform_image = convert_image(transform_image, image_type)

    return transform_image


def hedScan(image, width=500, height=500, thresh=255):
    transform_image = image.copy()
    image_type = get_type(image)
    image = convert_image(image, 'cv2')
    edge_img = HED_DETECTION_MODEL.detect_edge(image, width, height)

    findCnt = find_contours(edge_img, thresh)

    if findCnt is not None:
        transform_image = four_point_transform(image, findCnt.reshape(4, 2))
        transform_image = convert_image(transform_image, image_type)

    return transform_image


def find_contours(image, thresh=-1):
    '''
    Contours 검색
    :param image: (bytes) or (pil.image) or (numpy array) or (qimage)
    :param thresh: (int)
    :return: (numpy.ndarray)
    '''
    image = convert_image(image, 'cv2')

    # contours를 찾아 크기순으로 정렬
    if thresh > -1:
        ret, edge_img = cv2.threshold(image, thresh, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    else:
        edge_img = image.copy()

    cnts = cv2.findContours(edge_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

    findCnt = None

    # 정렬된 contours를 반복문으로 수행하며 4개의 꼭지점을 갖는 도형을 검출
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)

        # contours가 크기순으로 정렬되어 있기때문에 제일 첫번째 사각형을 윤곽선 영역으로 판단하고 break
        if len(approx) == 4:
            findCnt = approx
            break

    # 만약 추출한 윤곽이 없을 경우 오류
    if findCnt is None:
        print("Could not find receipt outline.")

    return findCnt


def draw_contours(image, contour):
    '''
    contour box를 그린 이미지를 Return
    :param image: (bytes) or (pil.image) or (numpy array) or (qimage)
    :param contour: (numpy.ndarray)
    :return: (bytes) or (pil.image) or (numpy array) or (qimage)
    '''
    image_type = get_type(image)
    output = convert_image(image, 'cv2')
    cv2.drawContours(output, [contour], -1, (0, 255, 255), 10)
    output = convert_image(output, image_type)

    return output