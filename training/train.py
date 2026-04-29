from ultralytics import YOLO

def main():
    # Load lightweight pretrained model
    model = YOLO("yolov8n.pt")   # Nano version (fastest)

    model.train(
        data="training/data.yaml",
        
        # -------- Core Training Settings --------
        epochs=15,          # Keep low for CPU
        imgsz=416,          # Smaller = much faster
        batch=6,            # Safe for i5
        device="cpu",
        workers=2,
        freeze=10,          # Freeze backbone (BIG speed boost)
        
        # -------- Reduce Heavy Augmentation --------
        hsv_h=0.015,
        hsv_s=0.5,
        hsv_v=0.3,
        degrees=3,
        translate=0.08,
        scale=0.3,
        shear=1.0,
        fliplr=0.5,
        mosaic=0.5,         # Reduced from 1.0
        mixup=0.0,          # Disabled (heavy on CPU)
        
        # -------- Training Stability --------
        patience=5,
        optimizer="SGD",    # Lighter than AdamW on CPU
        verbose=True
    )

if __name__ == "__main__":
    main()
