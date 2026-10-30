import os
import sys
import zipfile
import io
import random
from pathlib import Path
from PIL import Image
import torch
from torchvision import transforms
from transformers import AutoImageProcessor, AutoModelForImageClassification

sys.path.insert(0, str(Path(__file__).resolve().parent))
from app.ml.classes import PLANTVILLAGE_CLASSES, get_class_profile

MODEL_NAME = "surgeonwz/plant-village"
print(f"Loading {MODEL_NAME}...")
processor = AutoImageProcessor.from_pretrained(MODEL_NAME)
model = AutoModelForImageClassification.from_pretrained(MODEL_NAME)
model.eval()

ZIP_PATH = Path(os.environ["USERPROFILE"]) / ".cache" / "huggingface" / "hub" / "datasets--mohanty--PlantVillage" / "snapshots" / "9e97599868962bd0079b8db4b7f1efa9185fa1e7" / "data.zip"

def normalize_folder(name: str) -> str:
    norm = name.replace(" ", "_")
    for pv_cls in PLANTVILLAGE_CLASSES:
        if pv_cls.lower() == norm.lower():
            return pv_cls
    return norm

# Map model's id2label to PLANTVILLAGE_CLASSES
id2label_mapped = {}
for idx, lbl in model.config.id2label.items():
    id2label_mapped[int(idx)] = normalize_folder(lbl)

print(f"Mapped {len(id2label_mapped)} classes.")

# Sample 100 images across different classes
class_images = {}
with zipfile.ZipFile(ZIP_PATH, 'r') as zf:
    for member in zf.namelist():
        if member.startswith("raw/color/") and not member.endswith("/"):
            parts = member.split("/")
            if len(parts) >= 4:
                pv_cls = normalize_folder(parts[2])
                if pv_cls in PLANTVILLAGE_CLASSES:
                    if pv_cls not in class_images:
                        class_images[pv_cls] = []
                    class_images[pv_cls].append(member)

test_samples = []
random.seed(42)
for cls_name, files in class_images.items():
    for f in random.sample(files, min(4, len(files))):
        test_samples.append((f, cls_name))

print(f"Evaluating {len(test_samples)} images with {MODEL_NAME}...")

correct = 0
total = 0
healthy_correct = 0
healthy_total = 0

with zipfile.ZipFile(ZIP_PATH, 'r') as zf:
    for fpath, true_cls in test_samples:
        img_bytes = zf.read(fpath)
        img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
        inputs = processor(img, return_tensors="pt")
        with torch.no_grad():
            logits = model(**inputs).logits
            probs = torch.softmax(logits, dim=-1)[0]
            pred_idx = int(logits.argmax(-1).item())
            pred_cls = id2label_mapped[pred_idx]
            conf = probs[pred_idx].item()

        is_match = (pred_cls == true_cls)
        total += 1
        if is_match:
            correct += 1

        is_true_healthy = "healthy" in true_cls.lower()
        is_pred_healthy = "healthy" in pred_cls.lower()
        if is_true_healthy:
            healthy_total += 1
            if is_pred_healthy:
                healthy_correct += 1

print(f"\nResults for {MODEL_NAME}:")
print(f"Top-1 Accuracy: {correct}/{total} ({correct/total*100:.2f}%)")
print(f"Healthy Recall: {healthy_correct}/{healthy_total} ({healthy_correct/healthy_total*100:.2f}%)")
