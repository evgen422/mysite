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
    start_time = time.time()
    while True:
        #print('views id',threading.get_ident())
        if not frame_queue.empty():
            fps_counter()
            frame = frame_queue.get()
            # Encode the frame as a JPEG image
            ret, buffer = cv2.imencode('.jpg', frame)
            encoded_frame = buffer.tobytes()

            # calculate the time to sleep
            elapsed_time = time.time() - start_time
            if elapsed_time > 0.1:
                print('VIEWS spike..', elapsed_time)
            time.sleep(0.035)
            start_time = time.time()

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
    if time_gap_ms > 1000:
        print('fps ', i) #print(f'fps \r{i}', end='', flush=True) #
        i = 0
        time_start = dt.datetime.now()

