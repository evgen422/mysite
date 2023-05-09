from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import cv2

url = "http://maps.ufanet.ru/ufa" 
options = Options()
#options.add_argument("--headless")
#options.add_argument("--no-sandbox")

#options.headless = True

driver = webdriver.Chrome("/usr/bin/chromedriver")#, options=options)

driver.get(url)
print(driver.title)


# Find the element with the event listener
element = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div[1]/div[2]/div[3]/img[227]')
#element = driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div[1]/div[2]/div[3]/img[227]')
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
	print(i)
	i = 0-i
	action.move_to_element_with_offset(element, 0, 0)
	action.move_to_element_with_offset(element, 0, i)

	# Click on the element
	action.click().perform()
time.sleep(2)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
div = soup.find('div', {'class': 'ModalBodyPlayer'})
print(div)
video = div.find('iframe')
link = video.attrs.get('src')
print(link)
driver.quit()

# Create a VideoCapture object and open the video stream
stream_url = link
cap = cv2.VideoCapture(stream_url)

# Check if the video stream is open
if not cap.isOpened():
    print('Could not open video stream')
else:
    # Read frames from the video stream and display them
    while True:
        ret, frame = cap.read()
        if ret:
            cv2.imshow('Stream Video', frame)
        else:
            break
        key = cv2.waitKey(10)
        if key == ord('q'):
            break

# Release the video capture object and close all windows
cap.release()
cv2.destroyAllWindows()