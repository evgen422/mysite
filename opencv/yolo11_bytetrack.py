"""
YOLOv11 Object Tracking with ByteTrack.

Detects and tracks vehicles (cars, motorcycles, buses, trucks)
from the live Ufanet CCTV stream retrieved automatically via stream_manager.
"""

import os
import sys
import time
from pathlib import Path
import threading

from datetime import datetime

import cv2
import numpy as np

# Ensure project root is in sys.path when executed directly
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# Setup Django environment if run as a standalone script
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
try:
    import django
    django.setup()
except Exception:
    pass

from ultralytics import YOLO
from opencv import stream_manager

# Vehicle classes from COCO dataset:
# 2: car, 3: motorcycle, 5: bus, 7: truck
VEHICLE_CLASSES = [2, 3, 5, 7]
DEFAULT_MODEL_PATH = "yolo11n.pt"
TRACKER_CONFIG = "bytetrack.yaml"
DEVICE = "cpu"
# Frames wider than this are downscaled before inference to keep CPU FPS usable
MAX_FRAME_WIDTH = 960

class YOLO11ByteTracker:
    """
    YOLOv11 vehicle tracker using ByteTrack algorithm running on CPU.
    """

    def __init__(
        self,
        model_name: str = DEFAULT_MODEL_PATH,
        classes: list = None,
        device: str = DEVICE,
        tracker: str = TRACKER_CONFIG,
        conf: float = 0.35,
        iou: float = 0.5,
    ):
        self.model_name = model_name
        self.classes = classes if classes is not None else VEHICLE_CLASSES
        self.device = device
        self.tracker = tracker
        self.conf = conf
        self.iou = iou

        print(f"Loading YOLOv11 model '{self.model_name}' on device '{self.device}'...")
        self.model = YOLO(self.model_name)
        print("Model loaded successfully.")

        # =====================================================================
        # PLACEHOLDER: Vehicle Counting & Line-Crossing State Initialization
        # =====================================================================
        # Re-initialize custom tracking states, direction vectors, or counters:
        # e.g.,
        # self.active_tracks = {}
        # self.prev_tracks = {}
        # self.left_counter = 0
        # self.right_counter = 0
        # self.counting_line_y = 350
        # self.db_connection = ...
        # =====================================================================

    def get_live_stream_url(self, force_refresh: bool = False) -> str:
        """
        Fetch the current live stream URL via the stream_manager architecture.
        """
        stream_info = stream_manager.refresh_stream_info(force=force_refresh)
        stream_url = stream_info.get("stream_url")
        if not stream_url:
            raise RuntimeError(
                f"Unable to retrieve stream URL from stream_manager: {stream_info.get('error')}"
            )
        return stream_url

    def prepare_frame(self, frame: np.ndarray) -> np.ndarray:
        """
        Downscale an incoming frame when it is wider than MAX_FRAME_WIDTH.

        Detection coordinates are produced on the returned frame, so the
        annotations drawn afterwards stay aligned with the resized image.
        """
        height, width = frame.shape[:2]
        if width > MAX_FRAME_WIDTH:
            scale = MAX_FRAME_WIDTH / float(width)
            frame = cv2.resize(
                frame,
                (int(width * scale), int(height * scale)),
                interpolation=cv2.INTER_AREA,
            )
        return frame

    def track_frame(self, frame: np.ndarray, persist: bool = True):
        """
        Run YOLOv11 ByteTrack tracking on a single frame.
        """
        results = self.model.track(
            source=frame,
            persist=persist,
            tracker=self.tracker,
            device=self.device,
            classes=self.classes,
            conf=self.conf,
            iou=self.iou,
            verbose=False,
        )
        return results[0]

    def process_tracks(self, frame: np.ndarray, result) -> np.ndarray:
        """
        Draw bounding boxes, IDs, class names, and handle counting logic.
        """
        annotated_frame = frame.copy()

        boxes = result.boxes
        if boxes is not None and len(boxes) > 0:
            for box in boxes:
                xyxy = box.xyxy[0].cpu().numpy().astype(int)
                xmin, ymin, xmax, ymax = xyxy

                conf = float(box.conf[0].cpu().numpy())
                class_id = int(box.cls[0].cpu().numpy())
                class_name = self.model.names.get(class_id, str(class_id))
                track_id = int(box.id[0].cpu().numpy()) if box.id is not None else None

                # =============================================================
                # PLACEHOLDER: Vehicle Counting & Line-Crossing Logic
                # =============================================================
                # Re-insert directional analysis, virtual line crossing,
                # edge-of-screen boundary triggers, or database logging here.
                #
                # Example:
                # center_x = (xmin + xmax) // 2
                # center_y = (ymin + ymax) // 2
                # if track_id in self.prev_tracks:
                #     prev_x, prev_y = self.prev_tracks[track_id]
                #     if prev_x < line_x <= center_x:
                #         self.right_counter += 1
                #         # log_to_db(...)
                # =============================================================

                # Draw bounding box (cars are in bounding boxes with id)
                box_color = (0, 255, 0)
                cv2.rectangle(annotated_frame, (xmin, ymin), (xmax, ymax), box_color, 2)

                # Draw label with ID, class name, and confidence
                label = f"ID:{track_id} {class_name} {conf:.2f}" if track_id is not None else f"{class_name} {conf:.2f}"
                (label_w, label_h), baseline = cv2.getTextSize(
                    label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1
                )
                label_ymin = max(ymin, label_h + 10)
                cv2.rectangle(
                    annotated_frame,
                    (xmin, label_ymin - label_h - 5),
                    (xmin + label_w + 5, label_ymin + baseline - 5),
                    box_color,
                    -1,
                )
                cv2.putText(
                    annotated_frame,
                    label,
                    (xmin + 2, label_ymin - 4),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 0, 0),
                    1,
                    cv2.LINE_AA,
                )

        # =====================================================================
        # PLACEHOLDER: On-Screen Counters / Statistics Overlay
        # =====================================================================
        # e.g.,
        # cv2.putText(annotated_frame, f"Left: {self.left_counter}", (20, 60), ...)
        # cv2.putText(annotated_frame, f"Right: {self.right_counter}", (20, 100), ...)
        # =====================================================================

        return annotated_frame


    def stream_generator(self, max_consecutive_failures: int = 15):
        """
        Yield processed annotated frames as a generator.
        Automatically reconnects and refreshes the token if the stream drops.
        """
        url = self.get_live_stream_url()
        print(f"Opening live stream: {url}")
        cap = cv2.VideoCapture(url)
        consecutive_failures = 0

        try:
            while True:
                ret, frame = cap.read()
                if not ret or frame is None:
                    consecutive_failures += 1
                    print(f"Warning: Stream read failure #{consecutive_failures}. Re-fetching URL...")
                    time.sleep(1)

                    if consecutive_failures >= max_consecutive_failures:
                        cap.release()
                        url = self.get_live_stream_url(force_refresh=True)
                        print(f"Reconnecting with refreshed URL: {url}")
                        cap = cv2.VideoCapture(url)
                        consecutive_failures = 0
                    continue

                consecutive_failures = 0
                track_result = self.track_frame(frame, persist=True)
                annotated_frame = self.process_tracks(frame, track_result)

                yield annotated_frame

        finally:
            cap.release()
            print("Capture released.")

    def run_live(self, display: bool = True, output_path: str = None):
        """
        Run the full tracking loop on the live CCTV stream.
        """
        url = self.get_live_stream_url()
        print(f"Connecting to live CCTV stream: {url}")

        cap = cv2.VideoCapture(url)
        if not cap.isOpened():
            print("Initial connection failed. Attempting force token refresh...")
            url = self.get_live_stream_url(force_refresh=True)
            cap = cv2.VideoCapture(url)

        writer = None
        consecutive_failures = 0

        try:
            while True:
                start_time = time.time()

                ret, frame = cap.read()
                if not ret or frame is None:
                    consecutive_failures += 1
                    print(f"Failed to read frame ({consecutive_failures}). Refreshing token...")
                    time.sleep(1)
                    if consecutive_failures > 5:
                        cap.release()
                        url = self.get_live_stream_url(force_refresh=True)
                        print(f"Reconnecting to new stream URL: {url}")
                        cap = cv2.VideoCapture(url)
                        consecutive_failures = 0
                    continue

                consecutive_failures = 0

                # Downscale the frame to keep CPU inference fast
                frame = self.prepare_frame(frame)

                # Run YOLOv11 tracking with ByteTrack on CPU
                track_result = self.track_frame(frame, persist=True)

                # Annotate frame and process tracking data
                annotated_frame = self.process_tracks(frame, track_result)

                # Compute and display FPS
                elapsed = time.time() - start_time
                fps = 1.0 / elapsed if elapsed > 0 else 0.0
                cv2.putText(
                    annotated_frame,
                    f"FPS: {fps:.2f} (CPU / YOLO11n + ByteTrack)",
                    (20, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 0, 255),
                    2,
                )

                # Optional video saving
                if output_path:
                    if writer is None:
                        h, w = annotated_frame.shape[:2]
                        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
                        writer = cv2.VideoWriter(output_path, fourcc, 25.0, (w, h))
                    writer.write(annotated_frame)

                # Interactive display window if GUI environment is present
                if display:
                    cv2.imshow("YOLOv11 + ByteTrack Live Stream", annotated_frame)
                    if cv2.waitKey(1) & 0xFF == ord("q"):
                        print("User requested quit.")
                        break

        except KeyboardInterrupt:
            print("Stopped by user (KeyboardInterrupt).")
        finally:
            cap.release()
            if writer is not None:
                writer.release()
            if display:
                cv2.destroyAllWindows()
            print("Tracking session ended and resources cleared.")


def main():
    tracker = YOLO11ByteTracker(
        model_name=DEFAULT_MODEL_PATH,
        classes=VEHICLE_CLASSES,
        device=DEVICE,
        tracker=TRACKER_CONFIG,
    )
    display = bool(os.environ.get("DISPLAY"))
    tracker.run_live(display=display)




# Singleton tracker broadcaster instance for serving web clients
_tracker_instance = None
_tracker_lock = threading.Lock()


class StreamBroadcaster:
    """
    Background worker that continuously tracks frames from live stream
    and broadcasts annotated frames to web clients.
    """

    def __init__(self, tracker: YOLO11ByteTracker = None):
        self.tracker = tracker or YOLO11ByteTracker()
        self.lock = threading.Lock()
        self.latest_jpeg = None
        self.last_frame_time = 0
        self.running = False
        self.thread = None
        self.subscribers = 0
        self.stats = {
            "fps": 0.0,
            "tracked_vehicles": 0,
            "status": "idle",
        }

    def start(self):
        with self.lock:
            self.subscribers += 1
            if self.running:
                return
            self.running = True
            self.thread = threading.Thread(
                target=self._worker_loop, daemon=True, name="YOLO11Broadcaster"
            )
            self.thread.start()

    def stop_subscriber(self):
        with self.lock:
            self.subscribers = max(0, self.subscribers - 1)

    def _worker_loop(self):
        print("Starting YOLO11 ByteTrack background worker loop...")
        cap = None
        consecutive_failures = 0

        while self.running:
            with self.lock:
                subs = self.subscribers

            if subs <= 0:
                # Nobody is watching: release the capture so returning viewers
                # never receive stale buffered frames.
                if cap is not None:
                    cap.release()
                    cap = None
                    print("No viewers left, live capture released.")
                self.stats["status"] = "standby (no viewers)"
                self.stats["fps"] = 0.0
                self.stats["tracked_vehicles"] = 0
                time.sleep(1)
                continue

            if cap is None:
                try:
                    url = self.tracker.get_live_stream_url()
                    print(f"Opening live stream: {url}")
                    cap = cv2.VideoCapture(url)
                    consecutive_failures = 0
                except Exception as e:
                    self.stats["status"] = f"connect error: {e}"
                    time.sleep(2)
                    continue

            t_start = time.time()
            ret, frame = cap.read()
            if not ret or frame is None:
                consecutive_failures += 1
                self.stats["status"] = f"read failure ({consecutive_failures})"
                time.sleep(0.5)
                if consecutive_failures > 5:
                    cap.release()
                    cap = None
                    try:
                        url = self.tracker.get_live_stream_url(force_refresh=True)
                        print(f"Reconnecting to new stream URL: {url}")
                        cap = cv2.VideoCapture(url)
                    except Exception as e:
                        print(f"Error reconnecting stream: {e}")
                    consecutive_failures = 0
                continue

            consecutive_failures = 0
            self.stats["status"] = "tracking"

            # Downscale the frame to keep CPU inference fast
            frame = self.tracker.prepare_frame(frame)

            # YOLOv11 tracking with ByteTrack on CPU
            result = self.tracker.track_frame(frame, persist=True)
            annotated_frame = self.tracker.process_tracks(frame, result)

            t_end = time.time()
            elapsed = t_end - t_start
            fps = 1.0 / elapsed if elapsed > 0 else 0.0

            # Update stats
            box_count = len(result.boxes) if result.boxes is not None else 0
            self.stats["fps"] = round(fps, 2)
            self.stats["tracked_vehicles"] = box_count

            cv2.putText(
                annotated_frame,
                f"YOLOv11 ByteTrack (CPU) | FPS: {fps:.1f} | Vehicles: {box_count}",
                (20, 35),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 255),
                2,
            )

            ret_enc, jpeg_buf = cv2.imencode(
                ".jpg", annotated_frame, [int(cv2.IMWRITE_JPEG_QUALITY), 75]
            )
            if ret_enc:
                with self.lock:
                    self.latest_jpeg = jpeg_buf.tobytes()
                    self.last_frame_time = time.time()

        if cap is not None:
            cap.release()

    def get_latest_frame_jpeg(self):
        """
        Return the most recently processed JPEG frame, or process one on demand.
        """
        self.start()
        # Wait up to 3 seconds for the first frame if just started
        for _ in range(30):
            with self.lock:
                if self.latest_jpeg is not None:
                    return self.latest_jpeg
            time.sleep(0.1)

        with self.lock:
            return self.latest_jpeg

    def mjpeg_generator(self):
        """
        Yield MJPEG stream chunks for Django StreamingHttpResponse.
        """
        self.start()
        try:
            last_sent = 0
            while True:
                with self.lock:
                    jpeg_bytes = self.latest_jpeg
                    frame_time = self.last_frame_time

                if jpeg_bytes is not None and frame_time != last_sent:
                    last_sent = frame_time
                    yield (
                        b"--frame\r\n"
                        b"Content-Type: image/jpeg\r\n\r\n"
                        + jpeg_bytes
                        + b"\r\n"
                    )
                time.sleep(0.04)
        finally:
            self.stop_subscriber()


def get_broadcaster() -> StreamBroadcaster:
    global _tracker_instance
    with _tracker_lock:
        if _tracker_instance is None:
            tracker = YOLO11ByteTracker(
                model_name=DEFAULT_MODEL_PATH,
                classes=VEHICLE_CLASSES,
                device=DEVICE,
                tracker=TRACKER_CONFIG,
            )
            _tracker_instance = StreamBroadcaster(tracker=tracker)
        return _tracker_instance

if __name__ == "__main__":
    main()


