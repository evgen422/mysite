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

import redis
import pickle
import concurrent.futures

def gen_frames():
    # Start the thread to read frames from the video stream
    thread = Thread(target=update, args=())
    thread.daemon = True
    thread.start()

def process_frame(frame):
        # Convert the frame to a PIL Image object
    im = Image.fromarray(frame)

    # Compress the image
    im = im.resize((480, 320)) # resize image if needed
    output = BytesIO()
    im.save(output, format='JPEG', quality=50) # reduce the quality
    return output

def update():
    url1 = 'http://136.169.226.81/1554451338BMM242/tracks-v1/mono.m3u8?token='
    token = '73cec74146a54369943538779e7dfddd'
    url = (f'{url1}{token}')
    print(url)
    capture = cv2.VideoCapture(url)
    capture.set(cv2.CAP_PROP_BUFFERSIZE, 100)

    r = redis.Redis(host='localhost', port=6379, db=0)
    
    start_time = time.time()
    BATCH = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        while True:
            if capture.isOpened():

                (status, frame) = capture.read()

                # Process the frame asynchronously
                future = executor.submit(process_frame, frame)

                BATCH.append(future)

                if len(BATCH) == 50:
                    # Wait for all the futures to complete
                    results = [b.result() for b in BATCH]
                    # Convert the list to bytes
                    batch_bytes = pickle.dumps(results)
                    r.publish('BATCH', batch_bytes)
                    BATCH = []
                        
                #time.sleep(0.01)
                elapsed_time = time.time() - start_time
                #if elapsed_time > 0.1:
                #print('update elapsed_time..', round(elapsed_time, 3))
                time.sleep(0.02) 
                start_time = time.time()
                fps_counter()
            else:
                print('else')
                token = get_token()
                url = (f'{url1}{token}')
                print(url)
                capture = cv2.VideoCapture(url)
                capture.set(cv2.CAP_PROP_BUFFERSIZE, 100)

time_start = dt.datetime.now()
i = 0
def fps_counter():
    global i
    global time_start
    i = i+1
    time_cycle = dt.datetime.now()
    time_gap = time_cycle - time_start
    time_gap_ms = time_gap.total_seconds() * 1000
    if time_gap_ms > 10000:
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
