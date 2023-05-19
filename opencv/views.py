from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.http import StreamingHttpResponse

import time
#import cv2
import datetime as dt
#from threading import Thread
import opencv.apps as apps
import multiprocessing

def index(request):
    return render(request, 'opencv.html')

# Define the view that renders the HTML template and streams the video
def video_feed(request):

    # Create a new pipe for this process
    parent_conn, child_conn = multiprocessing.Pipe()

    # Add the new pipe to the queue in apps.py
    apps.PIPE_QUEUE.put(parent_conn)

    return StreamingHttpResponse(show_frame(child_conn), content_type='multipart/x-mixed-replace; boundary=frame')


def show_frame(child_conn):

    while True:
        BATCH = child_conn.recv()
        for output in BATCH:
            time.sleep(0.035)
            fps_counter()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' +  output.getvalue() + b'\r\n')




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
        print('fps views ', i) #print(f'fps \r{i}', end='', flush=True) #
        i = 0
        time_start = dt.datetime.now()

