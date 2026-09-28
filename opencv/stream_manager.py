import re
import ssl
import threading
import time
import urllib.request

STREAM_CACHE = {
    'token': None,
    'server': None,
    'stream_url': None,
    'camera_name': 'г. Уфа, с. Нагаево, Советская, 13 Камера 2',
    'camera_id': '1554451338BMM242',
    'last_updated': 0,
    'status': 'initializing',
    'error': None,
}

_lock = threading.Lock()
_bg_thread_started = False
CACHE_TTL = 300  # refresh every 5 minutes (tokens usually expire around 1 hour)


def _fetch_token_from_ufanet(cam_id='1554451338BMM242'):
    """Extract live token, server and name directly from maps.ufanet.ru using standard library urllib."""
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    req = urllib.request.Request(
        'https://maps.ufanet.ru/ufa',
        headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    )

    with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
        html = resp.read().decode('utf-8', errors='ignore')

    idx = html.find(cam_id)
    if idx == -1:
        raise ValueError(f"Camera ID {cam_id} not found in map data")

    block = html[max(0, idx - 200):min(len(html), idx + 350)]
    token_m = re.search(r'marker\.token\s*=\s*[\'"]([a-f0-9]+)[\'"]', block)
    server_m = re.search(r'marker\.server\s*=\s*[\'"]([^\'"]+)[\'"]', block)
    name_m = re.search(r'marker\.name\s*=\s*[\'"]([^\'"]+)[\'"]', block)

    if not (token_m and server_m):
        raise ValueError("Could not extract token or server from camera data block")

    token = token_m.group(1)
    server = server_m.group(1)
    cam_name = name_m.group(1) if name_m else STREAM_CACHE['camera_name']
    stream_url = f"http://{server}/{cam_id}/tracks-v1/mono.m3u8?token={token}"

    return {
        'token': token,
        'server': server,
        'camera_name': cam_name,
        'camera_id': cam_id,
        'stream_url': stream_url,
    }


def refresh_stream_info(force=False):
    """Retrieve new stream info if cache expired or force=True."""
    global STREAM_CACHE
    now = time.time()
    with _lock:
        if not force and STREAM_CACHE['stream_url'] and (now - STREAM_CACHE['last_updated'] < CACHE_TTL):
            return STREAM_CACHE.copy()

    try:
        new_data = _fetch_token_from_ufanet(STREAM_CACHE['camera_id'])
        with _lock:
            STREAM_CACHE.update(new_data)
            STREAM_CACHE['last_updated'] = time.time()
            STREAM_CACHE['status'] = 'active'
            STREAM_CACHE['error'] = None
            return STREAM_CACHE.copy()
    except Exception as e:
        with _lock:
            STREAM_CACHE['status'] = 'error'
            STREAM_CACHE['error'] = str(e)
            return STREAM_CACHE.copy()


def _token_refresh_worker():
    """Background cycle that refreshes token periodically."""
    while True:
        try:
            refresh_stream_info(force=True)
        except Exception:
            pass
        time.sleep(CACHE_TTL)


def start_token_background_worker():
    """Start background refresh thread once."""
    global _bg_thread_started
    with _lock:
        if _bg_thread_started:
            return
        _bg_thread_started = True

    t = threading.Thread(target=_token_refresh_worker, daemon=True, name="UfanetTokenRefresher")
    t.start()
