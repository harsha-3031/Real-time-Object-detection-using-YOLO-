import cv2
from ultralytics import YOLO
from collections import defaultdict
import subprocess
import os


class ObjectTracker:

    def __init__(self, model_path):
        self.model = YOLO(model_path)
        self.class_names = self.model.names

    def process_video(self, source_path, output_path):

        cap = cv2.VideoCapture(source_path)

        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        fps = cap.get(cv2.CAP_PROP_FPS)

        # 🔥 IMPORTANT FIX
        if fps is None or fps == 0:
            fps = 20  # safe default for browser

        # Use browser-friendly codec
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')

        out = cv2.VideoWriter(
            output_path,
            fourcc,
            fps,
            (width, height)
        )

        id_frame_count = defaultdict(int)
        class_counts = defaultdict(int)

        frame_count = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame_count += 1

            # Skip alternate frames for speed
            if frame_count % 2 != 0:
                continue

            results = self.model.track(
                frame,
                persist=True,
                tracker="bytetrack.yaml",
                conf=0.5,
                imgsz=320
            )

            annotated = results[0].plot()
            boxes = results[0].boxes

            if boxes.id is not None:
                for box, obj_id in zip(boxes, boxes.id):

                    cls_id = int(box.cls[0])
                    obj_id = int(obj_id)

                    id_frame_count[obj_id] += 1

                    # Count stable tracks only
                    if id_frame_count[obj_id] == 15:
                        class_name = self.class_names[cls_id]
                        class_counts[class_name] += 1

            out.write(annotated)

        cap.release()
        out.release()

        # ---- Convert to browser compatible H264 ----
        converted_path = output_path.replace(".mp4", "_final.mp4")

        subprocess.run([
            "ffmpeg",
            "-y",
            "-i", output_path,
            "-vcodec", "libx264",
            "-preset", "fast",
            "-crf", "23",
            converted_path
        ], check=True)

        # Delete original OpenCV file
        if os.path.exists(output_path):
            os.remove(output_path)

        return converted_path, dict(class_counts)
