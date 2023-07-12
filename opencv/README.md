# YOLOv8 + Deep_Sort. Car counting

## Introduction

This project shows the capabilities of YOLO and Deep Sort in objects detection and tracking. First we use YOLO v8 trained on COCO dataset to detect cars and then we feed the bounding boxes to Deep Sort. Cars moving to the right are in blue boxes, to the left are green. As soon as a car touches the edge of the screen, it is counted and turns white.
Initially it was planned to stream live webcam detection and tracking results and monitor the road 24/7. The code used to get frames with OpenCV from a public webcam and transfer them to an RTMP Nginx server which converted them to HLS and streamed .m3u8 to the webpage, but lately due to limited GPU resources it was decided to just record a demo video and upload it to Youtube. 
Video can be found here http://45.95.235.237/opencv/

## Description

The code that is responsible for detection and tracking is located at [yolo8_deepsort.py] (https://github.com/evgen422/mysite/blob/main/opencv/yolo8_deepsort.py).

1) We start by capturig video from a public webcam

2) The webcam is protected by changing token once a hour, so when the token changes we call function get_token() to obtain new.

3) Using Selenium and BeautifulSoup we open the [map] (http://maps.ufanet.ru/ufa#) , locate the needed camera, navigate to it and get the new token.

4) Then we cut the region of interest

5) Using pre-trained on COCO dataset model yolov8n.pt we get detections for the given frame

6) We loop over detections and add them to a list if confidence > then threshold. Classes except car, bus and truck are filtered out.

7) Updating the tracker with the new detections. [Deep-sort-realtime] (https://pypi.org/project/deep-sort-realtime/) is used instead of original [Deep Sort] (https://github.com/nwojke/deep_sort) due to the inability of latter to work with live video. 

8) Looping over results. If track is confirmed, we get bounding boxes and calculate its direction (i.e. left to right)

9) If car reaches the edge of the screen and has appropriate direction, we count it and add to the database.

10) Saving track to a list for next iteration comparison

11) Drawing rectangles and IDs with OpenCV

12) Saving frame to output.mp4.
