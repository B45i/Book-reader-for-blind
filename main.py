import cv2
import numpy as np
import pytesseract
from gtts import gTTS
import vlc
import os


def get_image():
    camera_port = 0
    camera = cv2.VideoCapture(camera_port)
    _, im = camera.read()
    return im


def get_string():
    img = get_image()
    img = cv2.imread('test.png')
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)
    # cv2.imshow("noise-removed", img)
    # cv2.waitKey(0)
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
    # cv2.imshow("threshold", img)
    # cv2.waitKey(0)
    return pytesseract.image_to_string(img, lang='eng')


def read_text(text):
    # tts = gTTS(text=text, lang='en')
    # tts.save('op_audio.mp3')
    p = vlc.MediaPlayer('op_audio.mp3')
    p.play()


def main():
    text = get_string()
    print text
    read_text(text)
    read_text('hello world')


if __name__ == '__main__':
    main()