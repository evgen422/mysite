from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.http import StreamingHttpResponse

import time
import cv2
import datetime as dt

import opencv.apps as apps
import multiprocessing
import redis
from PIL import Image
import io
import numpy as np
import pickle
buffer = []
from threading import Thread
import threading


def index(request):
    return render(request, 'opencv.html')

# Define the view that renders the HTML template and streams the video
def video_feed(request):
    print('new instance of video_feed.....')

    def stream():
        while True:
            while len(buffer) > 0:
                frame = buffer[0]               
                buffer.pop(0)
                print('len', len(buffer))
                fps_counter()
                # Send the frame as the HTTP response
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')#used to be frame
                time.sleep(0.035)


    

    def consume_redis():
        # Connect to Redis
        r = redis.Redis(host='localhost', port=6379, db=0)

        # Subscribe to the "output" channel
        pubsub = r.pubsub(ignore_subscribe_messages=True)
        pubsub.subscribe('BATCH')
        start_time = time.time()
        for BATCH in pubsub.listen():
                elapsed_time = time.time() - start_time
                #print('LISTEN elapsed_time 1 sec..', round(elapsed_time, 3))
                start_time = time.time()
                BATCH = pickle.loads(BATCH['data'])
                #c = c + 30
                #print('total out: ', c)
                for frame in BATCH:
                    buffer.append(frame)
    redis_thread = threading.Thread(target=consume_redis)
    redis_thread.start()

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
    if time_gap_ms > 10000:
        print('fps views ', int(round((i/10), 0))) #print(f'fps \r{i}', end='', flush=True) #
        i = 0
        time_start = dt.datetime.now()
