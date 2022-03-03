from math import sqrt
import numpy as np
import cv2
import matplotlib.pyplot as plt
from image_processing import convert_image

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
            cv_img = convert_image(img[i], image_type='cv2')
            if len(cv_img.shape) <= 2:
                rgbImg = cv2.cvtColor(cv_img, cv2.COLOR_GRAY2RGB)
            else:
                rgbImg = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)

            plt.subplot(1, len(img), i + 1), plt.imshow(rgbImg)
            plt.title(titles[i])
            plt.xticks([]), plt.yticks([])

        plt.show()
    else:
        cv_img = convert_image(img, image_type='cv2')

        if len(cv_img.shape) < 3:
            rgbImg = cv2.cvtColor(cv_img, cv2.COLOR_GRAY2RGB)
        else:
            rgbImg = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)

        plt.imshow(rgbImg)
        plt.title(title)
        plt.xticks([]), plt.yticks([])
        plt.show()


def distance(p):
    return sqrt(p.x() * p.x() + p.y() * p.y())

def distancetoline(point, line):
    p1, p2 = line
    p1 = np.array([p1.x(), p1.y()])
    p2 = np.array([p2.x(), p2.y()])
    p3 = np.array([point.x(), point.y()])
    if np.dot((p3 - p1), (p2 - p1)) < 0:
        return np.linalg.norm(p3 - p1)
    if np.dot((p3 - p2), (p1 - p2)) < 0:
        return np.linalg.norm(p3 - p2)
    return np.linalg.norm(np.cross(p2 - p1, p1 - p3)) / np.linalg.norm(p2 - p1)
