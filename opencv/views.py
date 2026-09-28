from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.http import StreamingHttpResponse

from . import stream_manager

# Ensure background token refresher is started
stream_manager.start_token_background_worker()


def index(request):
    return render(request, 'opencv.html')

car_counting = index


def live_stream(request):
    """Render the live CCTV camera stream page."""
    stream_info = stream_manager.refresh_stream_info()
    return render(request, 'live_stream.html', {'stream_info': stream_info})


def live_stream_status(request):
    """API endpoint to get current stream URL or force token refresh."""
    force = request.GET.get('force', 'false').lower() == 'true'
    stream_info = stream_manager.refresh_stream_info(force=force)
    return JsonResponse(stream_info)



'''
# Define the view that renders the HTML template and streams the video
def video_feed(request, user_id):
    if user_id not in user_pings:
        user_pings[user_id] = []
        user_pings[user_id].append('ping')
        # start consuming Redis messages
        redis_thread = threading.Thread(target=consume_redis, args=(user_buffers[user_id], user_id))
        redis_thread.daemon = True
        redis_thread.start()

    print('user_id video_feed', user_id)
    def stream(redis_thread):
        buffer = user_buffers[user_id]
        while True:
            #print('cheeeck user_pings...', user_pings[user_id])
            if not redis_thread.is_alive():
                print('dead')
                break

            if len(buffer) > 0:
                frame = buffer[0]               
                buffer.pop(0)
                #print('len', len(buffer))
                fps_counter()
                # Send the frame as the HTTP response
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')#used to be frame
                time.sleep(0.037) # 20/37 for laptop

    return StreamingHttpResponse(stream(redis_thread), content_type='multipart/x-mixed-replace; boundary=frame')
'''    
'''
def consume_redis(buffer, user_id):
    # Connect to Redis
    r = redis.Redis(host='localhost', port=6379, db=0)

    # Subscribe to the "output" channel
    pubsub = r.pubsub(ignore_subscribe_messages=True)
    pubsub.subscribe('BATCH')
    start_time = time.time()
    for BATCH in pubsub.listen():
        elapsed_time = time.time() - start_time
        #print('LISTEN elapsed_time 10 sec..', round(elapsed_time, 3))
        #check if client disconnected
        if elapsed_time > 9:
            if len(user_pings[user_id]) == 0:
                # Unsubscribe from the channel and clean up the connection
                pubsub.unsubscribe('BATCH')
                r.connection_pool.disconnect()
                print('breaking...')
                break
            else:
                user_pings[user_id] = []
                start_time = time.time()


        BATCH = pickle.loads(BATCH['data'])

        for frame in BATCH:
            buffer.append(frame)

            if len(buffer) > 500:
                print('ALERT 500')
                buffer = []
'''             



'''
def ping(request):
    user_id = request.POST.get('user_id')
    if user_id not in user_buffers:
        user_buffers[user_id] = []
        user_pings[user_id] = []
    user_id = request.POST.get("user_id")
    ping = request.POST.get("ping")
    user_pings[user_id].append(ping)
    print('len', len(user_buffers[user_id]))

    return HttpResponse('OK')

'''






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

'''