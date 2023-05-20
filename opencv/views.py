from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.http import StreamingHttpResponse

import time
import cv2
import datetime as dt
#from threading import Thread
import opencv.apps as apps
import multiprocessing
import redis
from PIL import Image
import io
import numpy as np
import pickle

def index(request):
    return render(request, 'opencv.html')

# Define the view that renders the HTML template and streams the video
def video_feed(request):
    print('new instance of video_feed.....')
    # Connect to Redis
    r = redis.Redis(host='localhost', port=6379, db=0)
    # Subscribe to the "output" channel
    pubsub = r.pubsub(ignore_subscribe_messages=True)
    pubsub.subscribe('BATCH')

    def stream():
        for BATCH in pubsub.listen():
            BATCH = pickle.loads(BATCH['data'])
            for frame in BATCH:
                # Convert the message data to an image
                im = Image.open(io.BytesIO(frame.getvalue()))
                # Convert the image to JPEG format
                with io.BytesIO() as output:
                    im.save(output, 'JPEG')
                    frame = output.getvalue()
                # Send the frame as the HTTP response
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                time.sleep(0.038)
                #fps_counter()

    return StreamingHttpResponse(stream(), content_type='multipart/x-mixed-replace; boundary=frame')




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
