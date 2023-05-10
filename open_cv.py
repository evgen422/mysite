import cv2
import datetime as dt

url = 'http://136.169.226.81/1554451338BMM242/tracks-v1/mono.m3u8?token='
token = 'e32c08e6327a49929dac9c8bc3420aca'
url2 = (f'{url}{token}')
print(url2)

# initialize OpenCV's video stream
video = cv2.VideoCapture(url2)

if not video.isOpened():
    print("Error opening video stream or file")

# read frames from the video stream
time_start = dt.datetime.now()
i = 0
while True:
    i = i+1
    time_cycle = dt.datetime.now()
    time_gap = time_cycle - time_start
    time_gap_ms = time_gap.total_seconds() * 1000
    if time_gap_ms > 10000:
        print('fps ', i)
        i = 0
        time_start = dt.datetime.now()

    ret, frame = video.read()
    if ret:
        cv2.imshow('VideoStream', frame)
    else:
        break
    
    # wait for a key press, and stop the loop if any key is pressed
    if cv2.waitKey(33) & 0xFF == ord('q'):
        break

# release the video stream resources and destroy all opencv windows
video.release()
cv2.destroyAllWindows()