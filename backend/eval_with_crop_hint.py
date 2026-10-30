"""
Evaluate the 1140-image benchmark WITH CROP HINT (as utilized in AgriGuard AI web app).
"""

import io
import json
import os
import random
import sys
import time
import zipfile
from collections import defaultdict
from pathlib import Path

import numpy as np
from PIL import Image
import torch
from torchvision import transforms
from transformers import MobileNetV2ForImageClassification

sys.path.insert(0, str(Path(__file__).resolve().parent))
from app.ml.classes import PLANTVILLAGE_CLASSES, get_class_profile

torch.set_num_threads(8)

ZIP_PATH = Path(os.environ["USERPROFILE"]) / ".cache" / "huggingface" / "hub" / "datasets--mohanty--PlantVillage" / "snapshots" / "9e97599868962bd0079b8db4b7f1efa9185fa1e7" / "data.zip"
MODEL_PATH = Path(__file__).resolve().parent / "ml_weights" / "plant_disease_model"

model = MobileNetV2ForImageClassification.from_pretrained(str(MODEL_PATH))
model.eval()

tfms = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

def normalize_folder_name(name: str) -> str:
    norm = name.replace(" ", "_")
    for pv_cls in PLANTVILLAGE_CLASSES:
        if pv_cls.lower() == norm.lower():
            return pv_cls
    return norm

class_images = defaultdict(list)
with zipfile.ZipFile(ZIP_PATH, 'r') as zf:
    for member in zf.namelist():
        if member.startswith("raw/color/") and not member.endswith("/"):
            parts = member.split("/")
            if len(parts) >= 4:
                pv_cls = normalize_folder_name(parts[2])
                if pv_cls in PLANTVILLAGE_CLASSES:
                    class_images[pv_cls].append(member)

SAMPLES_PER_CLASS = 30
eval_set = []
random.seed(42)

for cls_name, members in class_images.items():
    sampled = random.sample(members, min(SAMPLES_PER_CLASS, len(members)))
    for s in sampled:
        crop_name = cls_name.split("___")[0].replace("Corn_(maize)", "Corn").replace("Pepper,_bell", "Pepper")
        eval_set.append((s, cls_name, crop_name))

random.shuffle(eval_set)
total_eval = len(eval_set)

correct_top1 = 0
correct_top3 = 0
healthy_correct = 0
healthy_total = 0
diseased_correct = 0
diseased_total = 0

per_crop_stats = defaultdict(lambda: {"total": 0, "top1": 0})

t0 = time.time()
batch_size = 32

with zipfile.ZipFile(ZIP_PATH, 'r') as zf:
    for i in range(0, total_eval, batch_size):
        batch_slice = eval_set[i:i + batch_size]
        batch_tensors = []
        batch_classes = []
        batch_crops = []

        for member_path, true_cls, crop in batch_slice:
            img_bytes = zf.read(member_path)
            img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
            batch_tensors.append(tfms(img))
            batch_classes.append(true_cls)
            batch_crops.append(crop)

        stacked = torch.stack(batch_tensors)
        with torch.no_grad():
            logits = model(stacked).logits
            probs = torch.softmax(logits, dim=-1).cpu().numpy()

        for j, (true_cls, crop) in enumerate(zip(batch_classes, batch_crops)):
            sample_probs = probs[j]
            hint_norm = crop.lower()

            matching_indices = [
                idx for idx, c in enumerate(PLANTVILLAGE_CLASSES)
                if hint_norm in c.lower().split("___")[0] or (hint_norm in "corn" and "corn" in c.lower()) or (hint_norm in "pepper" and "pepper" in c.lower())
            ]

            if matching_indices:
                crop_probs = sample_probs[matching_indices]
                sorted_crop_rel = np.argsort(crop_probs)[::-1]
                pred_top1_idx = matching_indices[sorted_crop_rel[0]]
                top3_classes = [matching_indices[idx] for idx in sorted_crop_rel[:3]]
                top3_class_names = [PLANTVILLAGE_CLASSES[idx] for idx in top3_classes]
            else:
                sorted_all = np.argsort(sample_probs)[::-1]
                pred_top1_idx = int(sorted_all[0])
                top3_class_names = [PLANTVILLAGE_CLASSES[idx] for idx in sorted_all[:3]]

            pred_top1_cls = PLANTVILLAGE_CLASSES[pred_top1_idx]
            is_top1 = (pred_top1_cls == true_cls)
            is_top3 = (true_cls in top3_class_names)

            if is_top1:
                correct_top1 += 1
            if is_top3:
                correct_top3 += 1

            true_profile = get_class_profile(true_cls)
            pred_profile = get_class_profile(pred_top1_cls)

            if true_profile["is_healthy"]:
                healthy_total += 1
                if pred_profile["is_healthy"]:
                    healthy_correct += 1
            else:
                diseased_total += 1
                if not pred_profile["is_healthy"]:
                    diseased_correct += 1

            per_crop_stats[crop]["total"] += 1
            if is_top1:
                per_crop_stats[crop]["top1"] += 1

t1 = time.time()
total_time = t1 - t0

print("\n" + "=" * 60)
print("EVALUATION WITH CROP CONTEXT (AGRIGUARD AI ENGINE)")
print("=" * 60)
print(f"Total Images Evaluated: {total_eval}")
print(f"Execution Time:         {total_time:.1f}s ({total_eval/total_time:.1f} img/s)")
print(f"Top-1 Accuracy:         {(correct_top1 / total_eval) * 100:.2f}% ({correct_top1}/{total_eval})")
print(f"Top-3 Accuracy:         {(correct_top3 / total_eval) * 100:.2f}% ({correct_top3}/{total_eval})")
print(f"Healthy Recall:         {(healthy_correct / healthy_total) * 100:.2f}% ({healthy_correct}/{healthy_total})")
print(f"Diseased Recall:        {(diseased_correct / diseased_total) * 100:.2f}% ({diseased_correct}/{diseased_total})")

print("\n--- PER-CROP ACCURACY WITH CROP HINT ---")
for crop, st in sorted(per_crop_stats.items()):
    c_acc = (st["top1"] / st["total"]) * 100
    print(f"  {crop:<20}: {c_acc:6.2f}% ({st['top1']}/{st['total']})")
