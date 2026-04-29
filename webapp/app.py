import os
import time
import sys
import cv2
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename

sys.path.append("../tracking")
from tracker import ObjectTracker

app = Flask(__name__,
            static_folder="static",
            template_folder="templates")


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
OUTPUT_FOLDER = os.path.join(BASE_DIR, "static", "outputs")
MODEL_PATH = "../runs/detect/train2/weights/best.pt"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

tracker = ObjectTracker(MODEL_PATH)


@app.route("/")
def index():
    return render_template("index.html")


# ---------------- VIDEO UPLOAD ----------------
@app.route("/upload", methods=["POST"])
def upload_video():

    if "video" not in request.files:
        return jsonify({"success": False, "message": "No file uploaded"})

    file = request.files["video"]
    filename = secure_filename(file.filename)

    input_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(input_path)

    output_name = f"output_{int(time.time())}.mp4"
    output_path = os.path.join(OUTPUT_FOLDER, output_name)

    final_output, counts = tracker.process_video(input_path, output_path)

    return jsonify({
        "success": True,
       "output_url": f"/static/outputs/{os.path.basename(final_output)}",
        "counts": counts
})


# ---------------- LIVE RECORD ----------------
@app.route("/live_record", methods=["POST"])
def live_record():

    cap = cv2.VideoCapture(0)

    width = int(cap.get(3))
    height = int(cap.get(4))
    fps = 15

    raw_video = os.path.join(UPLOAD_FOLDER, "live_raw.mp4")

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(raw_video, fourcc, fps, (width, height))

    start_time = time.time()

    while time.time() - start_time < 10:
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)

    cap.release()
    out.release()

    output_name = f"live_output_{int(time.time())}.mp4"
    output_path = os.path.join(OUTPUT_FOLDER, output_name)

    final_output, counts = tracker.process_video(raw_video, output_path)

    return jsonify({
        "success": True,
       "output_url": f"/static/outputs/{os.path.basename(final_output)}",
        "counts": counts
})



if __name__ == "__main__":
    app.run(debug=True)
