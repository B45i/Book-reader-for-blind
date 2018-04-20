
# -*- coding: utf-8 -*-
import cv2
import requests
import pyttsx
from config import subscription_key
import RPi.GPIO as GPIO

def speek(text):
    
    speech_rate = 75
    engine = pyttsx.init()
    engine.setProperty('rate', speech_rate)
    print text
    engine.say(text)
    engine.runAndWait()


def get_text():

    image_path = 'capture.jpg'
    camera_port = 1

    vision_base_url = \
        'https://westcentralus.api.cognitive.microsoft.com/vision/v1.0/'
    vision_analyze_url = vision_base_url + 'ocr'

    # print 'Capturing image......'
    # camera = cv2.VideoCapture(camera_port)
    # _, img = camera.read()
    # cv2.imwrite(image_path, img)

    image_data = open(image_path, 'rb').read()

    headers = {'Ocp-Apim-Subscription-Key': subscription_key,
               'Content-Type': 'application/octet-stream'}
    params = {'language': 'en', 'detectOrientation ': 'true'}
    
    print 'Sending request......'
    
    response = requests.post(vision_analyze_url, headers=headers,
                             params=params, data=image_data)

    response.raise_for_status()

    print 'Responce received......'
    analysis = response.json()
    line_infos = [region['lines'] for region in analysis['regions']]
    words = []
    for line in line_infos:
        for word_metadata in line:
            for word_info in word_metadata['words']:
                words.append(word_info['text'])

    print 'Speking......'
    speek(' '.join(words))



GPIO.setmode(GPIO.BCM)

GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)#Button to GPIO23
GPIO.setup(24, GPIO.OUT)  #LED to GPIO24

try:
    while True:
         button_state = GPIO.input(23)
         if button_state == False:
             GPIO.output(24, True)
             get_text()
             GPIO.output(24, False)
except:
    GPIO.cleanup()
