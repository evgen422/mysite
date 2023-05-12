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
from opencv.apps import frame_queue




# Define the view that renders the HTML template and streams the video
def video_feed(request):
    return StreamingHttpResponse(show_frame(), content_type='multipart/x-mixed-replace; boundary=frame')

def index(request):
    return render(request, 'opencv.html')
        

'''
def gen_frames():
    url1 = 'http://136.169.226.81/1554451338BMM242/tracks-v1/mono.m3u8?token='
    token = get_token()
    url = (f'{url1}{token}')
    print(url)
    capture = cv2.VideoCapture(src)
    # Start the thread to read frames from the video stream
    thread = Thread(target=self.update, args=())
    thread.daemon = True
    thread.start()

def update():
    print('update funct started...')
    # Read the next frame from the stream in a different thread
    while True:
        if self.capture.isOpened():
            capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            (self.status, self.frame) = self.capture.read()
        time.sleep(.01)
'''
def show_frame():
    # Display frames in main program
    # Resize the frame to 480x320
    #resized_frame = cv2.resize(frame, (480, 320))
     # Encode the frame as a JPEG image
    #ret, buffer = cv2.imencode('.jpg', resized_frame)
    # Convert the encoded image to a byte string and yield it as a response
    while True:
        if not frame_queue.empty():
            frame = frame_queue.get()
            resized_frame = cv2.resize(frame, (480, 320))
            # Encode the frame as a JPEG image
            ret, buffer = cv2.imencode('.jpg', resized_frame)
            encoded_frame = buffer.tobytes()
            time.sleep(0.04)

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + encoded_frame + b'\r\n')

'''
def get_token(self):  
    url = "http://maps.ufanet.ru/ufa" 
    options = Options()
    options.add_argument("--headless")
    #options.add_argument("--no-sandbox")
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
'''



    # initialize OpenCV's video stream
    
'''    video = cv2.VideoCapture(url)
    if not video.isOpened():
        print("Error opening video stream or file")

    video.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    video.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    if not video.isOpened():
        print("Error opening video stream or file")

    while True:
        success, frame = video.read()
        if not success:
            break
        else:
            # Resize the frame to 480x320
            frame = cv2.resize(frame, (480, 320))
             # Encode the frame as a JPEG image
            ret, buffer = cv2.imencode('.jpg', frame)
            # Convert the encoded image to a byte string and yield it as a response
            frame = buffer.tobytes()
            time.sleep(0.04)
            #if cv2.waitKey(50) & 0xFF == ord('q'):
            #    break
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n') '''



'''
This code defines a class `VideoStreamWidget` that initializes a video stream and displays its frames. It uses OpenCV library to handle the video stream.

The `__init__()` method is called when an object of the class is created. It sets the URL for the video stream, gets a token using the `get_token()` method, and constructs the complete URL by concatenating the URL and token. It then calls the `init()` method to initialize the video stream.

The `init()` method initializes the video stream using the URL passed as an argument or the complete URL constructed by the `__init__()` method. It then starts a new thread to read frames from the video stream using the `update()` method.

The `update()` method continuously reads frames from the video stream and stores them in the `frame` variable. It also sets the width and height of the frames using `cv2.CAP_PROP_FRAME_WIDTH` and `cv2.CAP_PROP_FRAME_HEIGHT` to 640x480. These frames are later resized to 320x240 and encoded as JPEG images.

The `show_frame()` method is used to display the frames in the main program. It first resizes the frame to 480x320 pixels and encodes it as a JPEG image. It then yields the encoded frame as a response. The `yield` statement is used to generate a sequence of values, and each time it is called, it returns a new value.

The `get_token()` method is used to get a token that is appended to the URL to authenticate the video stream.

Overall, this code defines a simple video streaming widget that can be used to display video streams in Python programs.
'''