import cv2
import numpy as np
import pytesseract


def get_image():
    camera_port = 0
    camera = cv2.VideoCapture(camera_port)
    retval, im = camera.read()
    return im

def get_string():
    img = get_image()
    #img = cv2.imread("cam.jpg")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)
    cv2.imwrite("noise_removed.png", img)
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
    cv2.imwrite("threshold.png", img)
    return pytesseract.image_to_string(img, lang='eng')

print get_string()