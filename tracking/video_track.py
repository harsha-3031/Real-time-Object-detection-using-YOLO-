from tracker import ObjectTracker

MODEL_PATH = "runs/detect/train2/weights/best.pt"

tracker = ObjectTracker(MODEL_PATH)

input_video = "test_video.mp4"
output_video = "output_tracked.mp4"

output_path, counts = tracker.process_video(input_video, output_video)

print("✅ Done Processing")
print("Counts:", counts)
