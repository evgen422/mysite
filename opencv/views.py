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

def show_frame():
    # Convert the encoded image to a byte string and yield it as a response
    while True:
        if not frame_queue.empty():
            fps_counter()
            frame = frame_queue.get()
            resized_frame = cv2.resize(frame, (480, 320))
            # Encode the frame as a JPEG image
            ret, buffer = cv2.imencode('.jpg', resized_frame)
            encoded_frame = buffer.tobytes()
            time.sleep(0.04)

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + encoded_frame + b'\r\n')

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
        print('fps ', i)
        i = 0
        time_start = dt.datetime.now()

'''
This code defines a class `VideoStreamWidget` that initializes a video stream and displays its frames. It uses OpenCV library to handle the video stream.

The `__init__()` method is called when an object of the class is created. It sets the URL for the video stream, gets a token using the `get_token()` method, and constructs the complete URL by concatenating the URL and token. It then calls the `init()` method to initialize the video stream.

The `init()` method initializes the video stream using the URL passed as an argument or the complete URL constructed by the `__init__()` method. It then starts a new thread to read frames from the video stream using the `update()` method.

The `update()` method continuously reads frames from the video stream and stores them in the `frame` variable. It also sets the width and height of the frames using `cv2.CAP_PROP_FRAME_WIDTH` and `cv2.CAP_PROP_FRAME_HEIGHT` to 640x480. These frames are later resized to 320x240 and encoded as JPEG images.

The `show_frame()` method is used to display the frames in the main program. It first resizes the frame to 480x320 pixels and encodes it as a JPEG image. It then yields the encoded frame as a response. The `yield` statement is used to generate a sequence of values, and each time it is called, it returns a new value.

The `get_token()` method is used to get a token that is appended to the URL to authenticate the video stream.

Overall, this code defines a simple video streaming widget that can be used to display video streams in Python programs.
'''