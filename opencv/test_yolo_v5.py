import torch
import cv2
import datetime as dt

# Model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
model.conf = 0.25  # NMS confidence threshold
model.classes = [0, 2, 7]

#url1 = 'http://136.169.226.81/1554451338BMM242/tracks-v1/mono.m3u8?token='
#token = 'f2a1810c9f9646c286f1ce700fa0cd1e'
#url = (f'{url1}{token}')
#print(url)
url = 'http://95.140.153.88:8080/opencv/index.m3u8'

cap = cv2.VideoCapture(url)
new_size = (720, 420)

def detect():
    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        #frame = cv2.resize(frame, new_size)

        # Inference
        results = model(frame)
        #results.show()  # or .show()

        # Convert the tensor to a numpy array
        result_img = results.render()[0][:, :, ::-1]   

        # Display the resulting image in a window using OpenCV
        cv2.imshow('results', result_img)
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