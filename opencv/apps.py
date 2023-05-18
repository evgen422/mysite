from django.apps import AppConfig
import threading
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.db import models
from django.http import HttpResponse
from django.template import loader
from django.http import FileResponse
from django.http import StreamingHttpResponse

import os
from PIL import Image
from django.shortcuts import get_object_or_404

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import cv2
import datetime as dt
from threading import Thread
from queue import Queue
frame_queue = Queue()  # Create a new queue to store the frames

from io import BytesIO
from PIL import Image
import numpy as np

global buffer 
global current_frame
buffer = []

def gen_frames():
    print('get frames: token called...')
    url1 = 'http://136.169.226.81/1554451338BMM242/tracks-v1/mono.m3u8?token='
    #if token == 1:
    token = get_token()
    url = (f'{url1}{token}')
    print(url)
    capture = cv2.VideoCapture(url)
    capture.set(cv2.CAP_PROP_BUFFERSIZE, 100)
    # Start the thread to read frames from the video stream
    thread = Thread(target=update, args=(capture,))
    thread.daemon = True
    thread.start()

    thread2 = Thread(target=buffer_f, args=())
    thread2.daemon = True
    thread2.start()    

def buffer_f():
    global buffer
    global current_frame
    start_time = time.time()
    while True:
        if len(buffer) > 10:
            current_frame = buffer[0]
            buffer.pop(0)
            time.sleep(0.04)
            print('len', len(buffer))

        if len(buffer) == 100:
            buffer = []

        elapsed_time = time.time() - start_time
        print('buffer_f elapsed_time..', round(elapsed_time, 3))
        start_time = time.time()



def update(capture):
    print('apps id', threading.get_ident())
    start_time = time.time()
    global buffer
    while True:
        if capture.isOpened():

            (status, frame) = capture.read()

            # Convert the frame to a PIL Image object
            im = Image.fromarray(frame)

            # Compress the image
            im = im.resize((480, 320)) # resize image if needed
            output = BytesIO()
            im.save(output, format='JPEG', quality=50)

            buffer.append(output)
            time.sleep(0.01)



            elapsed_time = time.time() - start_time
            #if elapsed_time > 0.1:
            print('update elapsed_time..', round(elapsed_time, 3))
            #time.sleep(0.01) 
            start_time = time.time()
            #fps_counter()

time_start = dt.datetime.now()
i = 0
def fps_counter():
    global i
    global time_start
    i = i+1
    time_cycle = dt.datetime.now()
    time_gap = time_cycle - time_start
    time_gap_ms = time_gap.total_seconds() * 1000
    if time_gap_ms > 1000:
        print('apps fps.. ', i) #print(f'fps \r{i}', end='', flush=True) #
        i = 0
        time_start = dt.datetime.now()


class OpencvConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'opencv'
    print('apps.py AppConfig starting...')
    def ready(self):
        t = threading.Thread(target=gen_frames)
        t.start()    

def get_token():  
    url = "http://maps.ufanet.ru/ufa" 
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.headless = True

    driver = webdriver.Chrome("/usr/bin/chromedriver", options=options)

    driver.get(url)
    print(driver.title)


    # Find the element with the event listener
    element = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div[1]/div[2]/div[3]/img[227]')
    #element = driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div[1]/div[2]/div[3]/img[227]')
    time.sleep(1)

    # Click the element to trigger the event listener
    action = ActionChains(driver)
    action.double_click(element).perform()
    time.sleep(1)

    # Get the location of the element
    location = element.location

    # Move the mouse 100 pixels up from the element
    action = ActionChains(driver)

    for i in range(100, 105):
        i = 0-i
        action.move_to_element_with_offset(element, 0, 0)
        action.move_to_element_with_offset(element, 0, i)

        # Click on the element
        action.click().perform()
    time.sleep(2)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    div = soup.find('div', {'class': 'ModalBodyPlayer'})
    video = div.find('iframe')
    link = video.attrs.get('src')
    link = link.split('token=')
    link = link[1]
    link = link.split('&mute=true')
    token = link[0]
    print(token)
    driver.quit()
    return token
