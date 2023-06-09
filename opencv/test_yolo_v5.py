import torch
import cv2
import datetime as dt
from sort.sort import Sort
import numpy as np

# Model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
model.conf = 0.25  # NMS confidence threshold
model.classes = [0, 2, 7]

url1 = 'http://136.169.226.81/1554451338BMM242/tracks-v1/mono.m3u8?token='
token = 'e534fa570e7e4f56ba4621b6bd8dad57'
url = (f'{url1}{token}')
#print(url)
#url = 'http://95.140.153.88:8080/opencv/index.m3u8'

cap = cv2.VideoCapture(url)
new_size = (720, 420)

def detect():
    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        #frame = cv2.resize(frame, new_size)

        # Define the rectangle coordinates
        x, y, w, h = 960, 300, 640, 460

        # Draw the rectangle on the image
        #cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Extract the region of interest
        frame = cv2.getRectSubPix(frame, (w, h), (x+w/2, y+h/2))

        # Inference
        results = model(frame)

        print(results.pandas().xyxy[0])

        # Convert the YOLO detections to the format expected by SORT
        detections = []

        for i, row in results.pandas().xyxy[0].iterrows():
            x, y, x2, y2 = row[['xmin', 'ymin', 'xmax', 'ymax']]
            confidence = row['confidence']
            detections.append([x, y, x2, y2, confidence])

        sort_detections = np.array(detections)

        print(sort_detections)


        # Initialize the SORT tracker
        max_age = 30
        min_hits = 10
        iou_threshold = 0.1
        sort_tracker = Sort(max_age=max_age, min_hits=min_hits, iou_threshold=iou_threshold)

            
        # Update the tracker with the current frame and the converted detections
        track_bbs_ids = sort_tracker.update(sort_detections)
        
        # Loop over the tracks and draw the bounding boxes and IDs on the frame
        for track_bb_id in track_bbs_ids:
            x1, y1, x2, y2, track_id = map(int, track_bb_id)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
            cv2.putText(frame, str(track_id), (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        
        # Convert the tensor to a numpy array
        #result_img = results.render()[0][:, :, ::-1]   #CHANGES>>>>>>>>>>>>>????????????????????????????????????

        # Display the resulting image in a window using OpenCV
        cv2.imshow('results', frame)
        fps_counter()

        # Exit on 'q' keypress
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
'''
https://docs.ultralytics.com/yolov5/tutorials/pytorch_hub_model_loading/#inference-settings

model.conf = 0.25  # NMS confidence threshold
      iou = 0.45  # NMS IoU threshold
      agnostic = False  # NMS class-agnostic
      multi_label = False  # NMS multiple labels per box
      classes = None  # (optional list) filter by class, i.e. = [0, 15, 16] for COCO persons, cats and dogs
      max_det = 1000  # maximum number of detections per image
      amp = False  # Automatic Mixed Precision (AMP) inference

results = model(im, size=320)  # custom inference size

'''
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

detect()




#https://docs.ultralytics.com/yolov5/tutorials/pytorch_hub_model_loading/#detailed-example
#https://github.com/abewley/sort
#https://github.com/nwojke/deep_sort

 # def update(self, dets=np.empty((0, 5))):

#    Params:
 #     dets - a numpy array of detections in the format [[x1,y1,x2,y2,score],[x1,y1,x2,y2,score],...]