import vlc
import cv2
import sys
import select

url = 'http://136.169.226.81/1554451338BMM242/tracks-v1/mono.m3u8?token='
token = 'ec4d3c68f44243129596440a7e7e728f'
player = vlc.MediaPlayer(f'{url}{token}')
player.play()

# wait for playback to begin
while True:
    state = player.get_state()
    if state == vlc.State.Playing:
        continue
        #break





# release resources
cv2.destroyAllWindows()
player.stop()
print('end')
#media.stop()
#media.release()