from datetime import datetime
from ultralytics import YOLO
import cv2
from deep_sort_realtime.deepsort_tracker import DeepSort
import mysql.connector

def run():
    conn = mysql.connector.connect(
        host="localhost",
        user="evgeny",
        password="253321",
        database="AVITO_DB"
    )
    cursor = conn.cursor()


    CONFIDENCE_THRESHOLD = 0.6
    #color in BGR
    GREEN = (0, 255, 0) #nice color like lerua (154, 255, 157)
    WHITE = (255, 255, 255)
    BLUE = (255, 0, 0)

    url1 = 'http://136.169.226.81/1554451338BMM242/tracks-v1/mono.m3u8?token='
    token = '36c038625b9a4ea6adbb479d3d91a04c'
    url = (f'{url1}{token}')
    #url = 'http://136.169.226.35/001-999-097/tracks-v1/mono.m3u8?token=7beb585c7b0d4f37bdf864a535cc5723'

    # initialize the video capture object
    video_cap = cv2.VideoCapture(url)#"download.mp4")
    # initialize the video writer object
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    fps = 25
    output_file = "output.mp4"
    # Create a VideoWriter object
    out = cv2.VideoWriter(output_file, fourcc, fps, (640, 460))

    # load the pre-trained YOLOv8n model
    model = YOLO("yolov8n.pt")
    tracker = DeepSort(max_age=25, n_init=7, max_iou_distance=0.7, nn_budget=0, max_cosine_distance=0.2, nms_max_overlap=1.0)#TEEEEEEEEEEEEEEEEEEEEEEEESEEEEEEEEEEEEEETTTTTTTTTTTTTTT
    # Define the rectangle coordinates
    x, y, w, h = 960, 300, 640, 460
    frame_id = 0

    active_tracks = {}
    prev_tracks = {}
    right_counter = 0
    left_counter = 0

    while True:
        start = datetime.now()

        ret, frame = video_cap.read()

        if not ret:
            token = get_token()
            url = (f'{url1}{token}')
            print("url changed", url)
            video_cap = cv2.VideoCapture(url)
            continue

        # Extract the region of interest
        frame = cv2.getRectSubPix(frame, (w, h), (x+w/2, y+h/2))
        # run the YOLO model on the frame
        detections = model(frame)[0]

        # initialize the list of bounding boxes and confidences
        results = []

        ######################################
        # DETECTION
        ######################################

        # loop over the detections
        for data in detections.boxes.data.tolist():
            # extract the confidence (i.e., probability) associated with the prediction
            confidence = data[4]

            # filter out weak detections by ensuring the 
            # confidence is greater than the minimum confidence
            if float(confidence) < CONFIDENCE_THRESHOLD:
                continue

            # if the confidence is greater than the minimum confidence,
            # get the bounding box and the class id
            xmin, ymin, xmax, ymax = int(data[0]), int(data[1]), int(data[2]), int(data[3])
            class_id = int(data[5])
            # add the bounding box (x, y, w, h), confidence and class id to the results list
            print('class_id', class_id)
            #only cars and trucks and busses
            if class_id == 2 or class_id == 7 or class_id == 5:
                results.append([[xmin, ymin, xmax - xmin, ymax - ymin], confidence, class_id])

        ######################################
        # TRACKING
        ######################################

        # update the tracker with the new detections
        tracks = tracker.update_tracks(results, frame=frame)
        # loop over the tracks
        #print(trac)
        for track in tracks:
            done = 0
            dir = 0
            # if the track is not confirmed, ignore it
            if not track.is_confirmed():
                continue

            # get the track id and the bounding box
            track_id = track.track_id
            ltrb = track.to_ltrb()

            xmin, ymin, xmax, ymax = int(ltrb[0]), int(
                ltrb[1]), int(ltrb[2]), int(ltrb[3])

            #detecting direction of car
            if track_id in prev_tracks:
                #print(xmin, xmax, 'prev', prev_tracks[track_id][0])
                if (xmin+xmax) > (prev_tracks[track_id][0] + prev_tracks[track_id][1]):
                    dir = 1
                else:
                    dir = -1

            #count car if it reaches edge of screen
            #To the RIGHT
            if xmax > 630 and dir == 1 and prev_tracks[track_id][3] == 0:
                right_counter += 1
                done = 1
                #save to DB
                current_time = datetime.now()
                integer_time = int(current_time.strftime("%Y%m%d%H%M%S"))
                id = str(track_id) + str(integer_time)
                date = str(integer_time)
                cursor.execute('''INSERT INTO nagaevo_counter (id, date, direction)
                VALUES (%s, %s, %s)''', (id, date, dir))
                conn.commit()

            #To the LEFT
            if xmin < 10 and dir == -1 and prev_tracks[track_id][3] == 0:
                left_counter += 1
                done = 1
                #save to DB
                current_time = datetime.now()
                integer_time = int(current_time.strftime("%Y%m%d%H%M%S"))
                id = str(track_id) + str(integer_time)
                date = str(integer_time)
                cursor.execute('''INSERT INTO nagaevo_counter (id, date, direction)
                VALUES (%s, %s, %s)''', (id, date, dir))
                conn.commit()

            #if car has been counted in previous frame it is marked as done to prevent been counted again
            if len(prev_tracks) > 0:
                if track_id in prev_tracks:
                    if prev_tracks[track_id][3] == 1:
                        done = 1

            #saving car for next iteratin comparison
            active_tracks[track_id] = [xmin, xmax, dir, done]

            #choosing color (left/right/done)
            COLOR = GREEN#WHITE
            if dir == 1:
                COLOR = BLUE
            if dir == -1:
                COLOR = GREEN
            if done == 1:
                COLOR = WHITE                            

            # draw the bounding box and the track id
            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), COLOR, 2)
            cv2.rectangle(frame, (xmin, ymin - 20), (xmin + 40, ymin), COLOR, -1)
            cv2.putText(frame, str(track_id), (xmin + 5, ymin - 8),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, WHITE, 2)
            cv2.putText(frame, str(dir), (xmin + 25, ymin - 8),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, WHITE, 2)
            cv2.putText(frame, str(done), (xmin + 45, ymin - 8),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, WHITE, 2)

        prev_tracks = active_tracks
        active_tracks = {}


        # end time to compute the fps
        end = datetime.now()
        # show the time it took to process 1 frame
        print(f"Time to process 1 frame: {(end - start).total_seconds() * 1000:.0f} milliseconds")
        # calculate the frame per second and draw it on the frame
        fps = f"FPS: {1 / (end - start).total_seconds():.2f}"
        cv2.putText(frame, fps, (50, 400),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 8)

        #show car counters #color in BGR
        cv2.rectangle(frame, (150, 0), (350, 35), BLUE, -1)
        cv2.putText(frame, f"left: {left_counter}", (150, 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, GREEN, 4)
        cv2.rectangle(frame, (400, 0), (600, 35), GREEN, -1)
        cv2.putText(frame, f"right: {right_counter}", (400, 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, BLUE, 4)

        # show the frame to our screen
        cv2.imshow("Frame", frame)
        out.write(frame)
        if cv2.waitKey(1) == ord("q"):
            break

    video_cap.release()
    out.release()
    print('RELEASED>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    cv2.destroyAllWindows()
    conn.close()

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
def get_token():  
    url = "http://maps.ufanet.ru/ufa" 
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.headless = True

    driver = webdriver.Chrome("/usr/bin/chromedriver", options=options)

    driver.get(url)
    print(driver.title)


    # Find the element with the event listener
    element = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div[1]/div[2]/div[3]/img[225]')

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

run()