import os
from PIL import Image

DATASET_PATH = "dataset/filtered"

def check_images(split):
    image_path = os.path.join(DATASET_PATH, split, "images")
    for img in os.listdir(image_path):
        try:
            Image.open(os.path.join(image_path, img)).verify()
        except:
            print(f"Corrupted image found: {img}")

for s in ["train", "valid", "test"]:
    check_images(s)

print("Check complete.")
