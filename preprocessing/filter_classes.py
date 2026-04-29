import os
import shutil
import yaml

# ====== CONFIGURATION ======
ORIGINAL_DATASET = "dataset/original/COCO-1"
FILTERED_DATASET = "dataset/filtered"

# Put class names you WANT to keep (exact names from original data.yaml)
CLASSES_TO_KEEP = [
    "aeroplane", "apple", "backpack",
    "bicycle", "bird", "boat", "book",
    "bus", "car", "cat", "cell phone", "chair",
    "dog", "horse", "knife", "laptop",
    "motorbike", "person", "sofa", "traffic light", "wine glass"
]
   # <-- CHANGE THIS

# ============================


def load_yaml(path):
    with open(path, "r") as f:
        return yaml.safe_load(f)


def save_yaml(data, path):
    with open(path, "w") as f:
        yaml.dump(data, f)


def filter_split(split):
    images_path = os.path.join(ORIGINAL_DATASET, split, "images")
    labels_path = os.path.join(ORIGINAL_DATASET, split, "labels")

    new_images_path = os.path.join(FILTERED_DATASET, split, "images")
    new_labels_path = os.path.join(FILTERED_DATASET, split, "labels")

    os.makedirs(new_images_path, exist_ok=True)
    os.makedirs(new_labels_path, exist_ok=True)

    for label_file in os.listdir(labels_path):
        label_path = os.path.join(labels_path, label_file)

        with open(label_path, "r") as f:
            lines = f.readlines()

        new_lines = []

        for line in lines:
            class_id = int(line.split()[0])
            class_name = original_classes[class_id]

            if class_name in CLASSES_TO_KEEP:
                new_class_id = new_class_map[class_name]
                new_line = line.replace(str(class_id), str(new_class_id), 1)
                new_lines.append(new_line)

        # Keep only images that have selected classes
        if len(new_lines) > 0:
            image_file = label_file.replace(".txt", ".jpg")

            shutil.copy(
                os.path.join(images_path, image_file),
                os.path.join(new_images_path, image_file),
            )

            with open(os.path.join(new_labels_path, label_file), "w") as f:
                f.writelines(new_lines)


# ===== MAIN EXECUTION =====

original_yaml = load_yaml(os.path.join(ORIGINAL_DATASET, "data.yaml"))
original_classes = original_yaml["names"]

# Create new class mapping
new_class_map = {name: i for i, name in enumerate(CLASSES_TO_KEEP)}

# Remove old filtered folder if exists
if os.path.exists(FILTERED_DATASET):
    shutil.rmtree(FILTERED_DATASET)

# Filter each split
for split in ["train", "valid", "test"]:
    filter_split(split)

# Create new YAML
new_yaml = {
    "train": os.path.abspath(os.path.join(FILTERED_DATASET, "train", "images")),
    "val": os.path.abspath(os.path.join(FILTERED_DATASET, "valid", "images")),
    "test": os.path.abspath(os.path.join(FILTERED_DATASET, "test", "images")),
    "nc": len(CLASSES_TO_KEEP),
    "names": CLASSES_TO_KEEP,
}

os.makedirs("training", exist_ok=True)
save_yaml(new_yaml, "training/data.yaml")

print("Filtering complete.")
print("New dataset saved to dataset/filtered/")
print("New YAML saved to training/data.yaml")
