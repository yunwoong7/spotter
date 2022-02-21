import os
import io
import glob
import cv2
import numpy as np
import requests
import matplotlib.pyplot as plt
import PIL.Image
from PIL.JpegImagePlugin import JpegImageFile
from PIL.PngImagePlugin import PngImageFile
from PyQt5.QtGui import QImageReader, QPixmap, QImage
from PIL.ImageQt import ImageQt


def plt_imshow(img=None, title='image', figsize=(8, 5)):
    '''
    Jupyter Notebook 또는 Colab에서 이미지를 확인하기위한 Function
    :param img: (numpy) or (list - numpy)
    :param title: (str) or (list - str)
    :param figsize: (tuple)
    :return: None
    '''
    plt.figure(figsize=figsize)

    if type(img) == list:
        if type(title) == list:
            titles = title
        else:
            titles = []

            for i in range(len(img)):
                titles.append(title)

        for i in range(len(img)):
            if len(img[i].shape) <= 2:
                rgbImg = cv2.cvtColor(img[i], cv2.COLOR_GRAY2RGB)
            else:
                rgbImg = cv2.cvtColor(img[i], cv2.COLOR_BGR2RGB)

            plt.subplot(1, len(img), i + 1), plt.imshow(rgbImg)
            plt.title(titles[i])
            plt.xticks([]), plt.yticks([])

        plt.show()
    else:
        if len(img.shape) < 3:
            rgbImg = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        else:
            rgbImg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        plt.imshow(rgbImg)
        plt.title(title)
        plt.xticks([]), plt.yticks([])
        plt.show()


def load_image_file(file_path, return_type='bytes'):
    '''
    로컬 파일을 Load
    :param file_path: (str) 경로
    :param return_type: (str) 'bytes'
    :return: (pil.image) or (bytes) or (numpy)
    '''
    try:
        pil_image = PIL.Image.open(file_path)
    except IOError:
        print("Failed opening image file: {}".format(file_path))
        return

    ext = os.path.splitext(file_path)[1].lower()
    if ext in [".jpg", ".jpeg"]:
        format = "JPEG"
    else:
        format = "PNG"

    return make_result(pil_image, return_type=return_type, format=format)


def load_image_url(url, return_type='bytes'):
    '''
    URL을 이용하여 이미지를 Load
    :param url: (str)
    :param return_type: (str) 'bytes'
    :return: (pil.image) or (bytes) or (numpy)
    '''
    try:
        response = requests.get(url)
        pil_image = PIL.Image.open(io.BytesIO(response.content))
    except IOError:
        print("Failed opening image (url): {}".format(url))
        return


    return make_result(pil_image, return_type=return_type)


def make_result(pil_image, return_type='pil', format='JPEG'):
    '''
    이미지 Return Type을 변경
    :param pil_image: (pil.image)
    :param return_type: (str)
    :param format: (str)
    :return: (pil.image) or (bytes) or (numpy)
    '''

    # apply orientation to image according to exif
    pil_image = apply_exif_orientation(pil_image)

    if return_type == 'bytes':
        with io.BytesIO() as f:
            pil_image.save(f, format=format)
            f.seek(0)
            return f.read()
    elif return_type == 'pil':
        return pil_image
    elif return_type == 'cv2':
        return pil2cv(pil_image)


def apply_exif_orientation(image):
    '''
    image의 Exif(EXchangable Image File format) Tag정보를 활용하여 이미지를 회전
    :param image: (pil.image)
    :return: (pil.image)
    '''
    try:
        exif = image._getexif()
    except AttributeError:
        exif = None

    if exif is None:
        return image

    exif = {
        PIL.ExifTags.TAGS[k]: v
        for k, v in exif.items()
        if k in PIL.ExifTags.TAGS
    }

    orientation = exif.get("Orientation", None)

    if orientation == 1:
        # do nothing
        return image
    elif orientation == 2:
        # left-to-right mirror
        return PIL.ImageOps.mirror(image)
    elif orientation == 3:
        # rotate 180
        return image.transpose(PIL.Image.ROTATE_180)
    elif orientation == 4:
        # top-to-bottom mirror
        return PIL.ImageOps.flip(image)
    elif orientation == 5:
        # top-to-left mirror
        return PIL.ImageOps.mirror(image.transpose(PIL.Image.ROTATE_270))
    elif orientation == 6:
        # rotate 270
        return image.transpose(PIL.Image.ROTATE_270)
    elif orientation == 7:
        # top-to-right mirror
        return PIL.ImageOps.mirror(image.transpose(PIL.Image.ROTATE_90))
    elif orientation == 8:
        # rotate 90
        return image.transpose(PIL.Image.ROTATE_90)
    else:
        return image


def pil2bytes(pil_image):
    '''
    PIL 이미지를 bytes로 변환
    :param pil_image: (PIL.Image)
    :return: (bytes)
    '''
    byte_arr = io.BytesIO()
    pil_image.save(byte_arr, format=pil_image.format)
    image_bytes = byte_arr.getvalue()

    return image_bytes


def pil2cv(pil_image):
    '''
    PIL 이미지를 numpy 배열로 변환
    :param pil_image: (PIL.Image)
    :return: (numpy)
    '''
    numpy_image = np.array(pil_image)
    opencv_image = cv2.cvtColor(numpy_image, cv2.COLOR_RGB2BGR)

    return opencv_image


def pil2qimage(pil_image):
    '''
    PIL 이미지를 QImage로 변환
    :param pil_image: (PIL.Image)
    :return: (PyQt5.QtGui.QImage)
        '''
    if pil_image.mode == "RGB":
        r, g, b = pil_image.split()
        pil_image = PIL.Image.merge("RGB", (b, g, r))
    elif pil_image.mode == "RGBA":
        r, g, b, a = pil_image.split()
        pil_image = PIL.Image.merge("RGBA", (b, g, r, a))
    elif pil_image.mode == "L":
        pil_image = pil_image.convert("RGBA")

    pil_image_tmp = pil_image.convert("RGBA")
    data = pil_image_tmp.tobytes("raw", "RGBA")

    qimage = QImage(data, pil_image.size[0], pil_image.size[1], QImage.Format_RGBA8888)
    # pixmap = QPixmap.fromImage(qimage)

    return qimage


def cv2pil(opencv_image):
    '''
    cv2이미지(numpy배열)를 PIL이미지로 변환
    :param opencv_image: (numpy array)
    :return: (pil.image)
    '''
    color_coverted = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2RGB)
    pil_image = PIL.Image.fromarray(color_coverted)

    return pil_image


def cv2bytes(opencv_image):
    '''
    cv2이미지(numpy배열)를 bytes로 변환
    :param opencv_image: (numpy)
    :return: (bytes)
    '''
    is_success, im_buf_arr = cv2.imencode(".jpg", opencv_image)
    image_bytes = im_buf_arr.tobytes()

    return image_bytes


def cv2qimage(opencv_image):
    '''
    cv2이미지(numpy배열)를 QImage로 변환
    :param pil_image: (numpy)
    :return: (PyQt5.QtGui.QImage)
    '''
    height, width, channel = opencv_image.shape
    bytesPerLine = 3 * width
    qimage = QImage(opencv_image.data, width, height, bytesPerLine, QImage.Format_RGB888)

    return qimage


def bytes2pil(bytes):
    '''
    bytes를 Pil 이미지로 변환
    :param bytes: (bytes)
    :return: (pil.image)
    '''
    pil_image = PIL.Image.open(io.BytesIO(bytes))
    return pil_image


def bytes2cv(bytes):
    '''
    bytes를 cv2이미지(numpy배열)로 변환
    :param bytes: (bytes)
    :return: (numpy)
    '''
    encoded_img = np.frombuffer(bytes, dtype=np.uint8)
    opencv_image = cv2.imdecode(encoded_img, cv2.IMREAD_COLOR)

    return opencv_image


def bytes2qimage(bytes):
    '''
    bytes를 QImage이미지로 변환
    :param bytes:
    :return: (PyQt5.QtGui.QImage)
    '''
    qimage = QImage()
    qimage.loadFromData(bytes)

    return qimage


def convert_image(image, image_type):
    '''
    이미지변환을 쉽게 하기위한 Function
    :param image: (bytes) or (pil.image) or (numpy array)
    :param image_type: (str)
    :return: (bytes) or (pil.image) or (numpy array)
    '''
    result = image

    if type(image) == bytes:
        if image_type == 'pil':
            result = bytes2pil(image)
        elif image_type == 'cv2':
            result = bytes2cv(image)
        elif image_type == 'bytes':
            pass
        elif image_type == 'qimage':
            result = bytes2qimage(image)
    elif type(image) in [JpegImageFile, PngImageFile]:
        if image_type == 'pil':
            pass
        elif image_type == 'cv2':
            result = pil2cv(image)
        elif image_type == 'bytes':
            result = pil2bytes(image)
        elif image_type == 'qimage':
            result = pil2qimage(image)
    elif type(image) == numpy.ndarray:
        if image_type == 'pil':
            result = cv2pil(image)
        elif image_type == 'cv2':
            pass
        elif image_type == 'bytes':
            result = cv2bytes(image)
        elif image_type == 'qimage':
            result = cv2qimage(image)

    return result


def get_image_list(folder_path):
    '''
    특정 폴더의 이미지 파일 목록을 List형태로 Return
    :param folder_path: (str)
    :return: (list)
    '''
    images = []
    extensions = [".%s" % fmt.data().decode().lower() for fmt in QImageReader.supportedImageFormats()]

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(tuple(extensions)):
                relativePath = os.path.join(root, file)
                images.append(relativePath)

    images.sort(key=lambda x: x.lower())

    return images