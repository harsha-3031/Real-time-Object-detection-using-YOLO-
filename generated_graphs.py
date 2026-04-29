import pandas as pd
import matplotlib.pyplot as plt

# Load YOLOv8 results file
df = pd.read_csv("runs/detect/train2/results.csv")

# -------- Graph 1 Detection Metrics --------
plt.figure()
plt.plot(df['epoch'], df['metrics/precision(B)'], label="Precision")
plt.plot(df['epoch'], df['metrics/recall(B)'], label="Recall")
plt.plot(df['epoch'], df['metrics/mAP50(B)'], label="mAP@0.5")
plt.plot(df['epoch'], df['metrics/mAP50-95(B)'], label="mAP@0.5:0.95")
plt.xlabel("Epoch")
plt.ylabel("Score")
plt.title("Detection Performance Metrics")
plt.legend()
plt.savefig("graph_detection_metrics.png")

# -------- Graph 2 Training Loss --------
plt.figure()
plt.plot(df['epoch'], df['train/box_loss'], label="Box Loss")
plt.plot(df['epoch'], df['train/cls_loss'], label="Class Loss")
plt.plot(df['epoch'], df['train/dfl_loss'], label="DFL Loss")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.title("Training Loss")
plt.legend()
plt.savefig("graph_training_loss.png")

# -------- Graph 3 Validation Loss --------
plt.figure()
plt.plot(df['epoch'], df['val/box_loss'], label="Val Box Loss")
plt.plot(df['epoch'], df['val/cls_loss'], label="Val Class Loss")
plt.plot(df['epoch'], df['val/dfl_loss'], label="Val DFL Loss")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.title("Validation Loss")
plt.legend()
plt.savefig("graph_validation_loss.png")

# -------- Graph 4 mAP Improvement --------
plt.figure()
plt.plot(df['epoch'], df['metrics/mAP50(B)'], label="mAP@0.5")
plt.plot(df['epoch'], df['metrics/mAP50-95(B)'], label="mAP@0.5:0.95")
plt.xlabel("Epoch")
plt.ylabel("Accuracy")
plt.title("mAP Improvement During Training")
plt.legend()
plt.savefig("graph_map_improvement.png")

print("Graphs generated successfully!")