import cv2
import time
from tracker import ObjectTracker

MODEL_PATH = "runs/detect/train2/weights/best.pt"
tracker = ObjectTracker(MODEL_PATH)

# Step 1: Record 10 seconds
cap = cv2.VideoCapture(0)

width = int(cap.get(3))
height = int(cap.get(4))
fps = 20

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
raw_video = "live_raw.mp4"
out = cv2.VideoWriter(raw_video, fourcc, fps, (width, height))

start_time = time.time()

print("Recording for 10 seconds...")

while time.time() - start_time < 10:
    ret, frame = cap.read()
    if not ret:
        break
    out.write(frame)
    cv2.imshow("Recording...", frame)
    if cv2.waitKey(1) == 27:
        break

cap.release()
out.release()
cv2.destroyAllWindows()

print("Recording finished. Processing...")

# Step 2: Process recorded video
output_video = "live_tracked_output.mp4"
output_path, counts = tracker.process_video(raw_video, output_video)

print("Final Counts:", counts)
