"""
Comprehensive Multi-Class Validation Suite for PlantVillage Dataset.
Evaluates accuracy across all 38 classes, measuring:
- Overall Top-1 & Top-3 accuracy
- Healthy vs Diseased classification accuracy (False Positive / False Negative rates)
- Per-crop performance
- Detailed classification report
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
OUTPUT_REPORT_PATH = Path(__file__).resolve().parent / "evaluation_report.json"

print(f"Loading MobileNetV2 classifier from {MODEL_PATH}...")
model = MobileNetV2ForImageClassification.from_pretrained(str(MODEL_PATH))
model.eval()

tfms = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# Normalize ZIP folder names to match PLANTVILLAGE_CLASSES
def normalize_folder_name(name: str) -> str:
    norm = name.replace(" ", "_")
    for pv_cls in PLANTVILLAGE_CLASSES:
        if pv_cls.lower() == norm.lower():
            return pv_cls
    return norm

# Scan ZIP and group files by class
print("Scanning ZIP archive for 38 class color images...")
class_images = defaultdict(list)
with zipfile.ZipFile(ZIP_PATH, 'r') as zf:
    for member in zf.namelist():
        if member.startswith("raw/color/") and not member.endswith("/"):
            parts = member.split("/")
            if len(parts) >= 4:
                raw_folder = parts[2]
                pv_cls = normalize_folder_name(raw_folder)
                if pv_cls in PLANTVILLAGE_CLASSES:
                    class_images[pv_cls].append(member)

print(f"Found {len(class_images)} valid classes, total {sum(len(v) for v in class_images.values())} color images.")

# Sample 30 images per class for a fast, statistically representative benchmark of ~1,140 images
SAMPLES_PER_CLASS = 30
eval_set = []
random.seed(42)

for cls_name, members in class_images.items():
    sampled = random.sample(members, min(SAMPLES_PER_CLASS, len(members)))
    for s in sampled:
        eval_set.append((s, cls_name))

random.shuffle(eval_set)
total_eval = len(eval_set)
print(f"Running evaluation benchmark on {total_eval} sampled images ({SAMPLES_PER_CLASS} per class across all 38 classes)...")

# Evaluation metrics
correct_top1 = 0
correct_top3 = 0
healthy_correct = 0
healthy_total = 0
diseased_correct = 0
diseased_total = 0

per_class_stats = defaultdict(lambda: {"total": 0, "top1": 0, "top3": 0})
per_crop_stats = defaultdict(lambda: {"total": 0, "top1": 0})
confusion_pairs = defaultdict(int)

t0 = time.time()
batch_size = 32

with zipfile.ZipFile(ZIP_PATH, 'r') as zf:
    for i in range(0, total_eval, batch_size):
        batch_slice = eval_set[i:i + batch_size]
        batch_tensors = []
        batch_labels = []

        for member_path, true_cls in batch_slice:
            img_bytes = zf.read(member_path)
            img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
            batch_tensors.append(tfms(img))
            batch_labels.append(true_cls)

        stacked = torch.stack(batch_tensors)
        with torch.no_grad():
            outputs = model(stacked)
            logits = outputs.logits
            probs = torch.softmax(logits, dim=-1).cpu().numpy()

        for j, true_cls in enumerate(batch_labels):
            sample_probs = probs[j]
            sorted_indices = np.argsort(sample_probs)[::-1]
            pred_top1_idx = int(sorted_indices[0])
            pred_top1_cls = PLANTVILLAGE_CLASSES[pred_top1_idx]
            top3_classes = [PLANTVILLAGE_CLASSES[idx] for idx in sorted_indices[:3]]

            true_profile = get_class_profile(true_cls)
            pred_profile = get_class_profile(pred_top1_cls)

            is_top1 = (pred_top1_cls == true_cls)
            is_top3 = (true_cls in top3_classes)

            if is_top1:
                correct_top1 += 1
            else:
                confusion_pairs[(true_cls, pred_top1_cls)] += 1

            if is_top3:
                correct_top3 += 1

            # Healthy vs Diseased check
            true_is_healthy = true_profile["is_healthy"]
            pred_is_healthy = pred_profile["is_healthy"]

            if true_is_healthy:
                healthy_total += 1
                if pred_is_healthy:
                    healthy_correct += 1
            else:
                diseased_total += 1
                if not pred_is_healthy:
                    diseased_correct += 1

            # Per-class metrics
            per_class_stats[true_cls]["total"] += 1
            if is_top1:
                per_class_stats[true_cls]["top1"] += 1
            if is_top3:
                per_class_stats[true_cls]["top3"] += 1

            # Per-crop metrics
            crop = true_profile["crop"]
            per_crop_stats[crop]["total"] += 1
            if is_top1:
                per_crop_stats[crop]["top1"] += 1

        processed = min(i + batch_size, total_eval)
        if processed % 160 == 0 or processed == total_eval:
            current_top1 = (correct_top1 / processed) * 100
            print(f"Processed [{processed}/{total_eval}] ({processed/total_eval*100:.1f}%) | Current Top-1: {current_top1:.2f}%")

t1 = time.time()
total_time = t1 - t0

top1_acc = (correct_top1 / total_eval) * 100
top3_acc = (correct_top3 / total_eval) * 100
healthy_acc = (healthy_correct / max(healthy_total, 1)) * 100
diseased_acc = (diseased_correct / max(diseased_total, 1)) * 100

print("\n" + "=" * 60)
print("EVALUATION BENCHMARK RESULTS")
print("=" * 60)
print(f"Total Images Evaluated: {total_eval} across 38 classes")
print(f"Total Execution Time:   {total_time:.1f}s ({total_eval/total_time:.1f} images/sec)")
print(f"Top-1 Accuracy:         {top1_acc:.2f}% ({correct_top1}/{total_eval})")
print(f"Top-3 Accuracy:         {top3_acc:.2f}% ({correct_top3}/{total_eval})")
print(f"Healthy Plant Recall:   {healthy_acc:.2f}% ({healthy_correct}/{healthy_total})")
print(f"Diseased Plant Recall:  {diseased_acc:.2f}% ({diseased_correct}/{diseased_total})")

print("\n--- PER-CROP ACCURACY ---")
for crop, st in sorted(per_crop_stats.items()):
    c_acc = (st["top1"] / st["total"]) * 100
    print(f"  {crop:<20}: {c_acc:6.2f}% ({st['top1']}/{st['total']})")

print("\n--- HEALTHY CLASSES RECALL ---")
for cls_name, st in sorted(per_class_stats.items()):
    if "healthy" in cls_name.lower():
        c_acc = (st["top1"] / st["total"]) * 100
        print(f"  {cls_name:<35}: {c_acc:6.2f}% ({st['top1']}/{st['total']})")

# Save structured report
report_data = {
    "total_images": total_eval,
    "elapsed_seconds": round(total_time, 2),
    "throughput_fps": round(total_eval / total_time, 2),
    "top1_accuracy_pct": round(top1_acc, 2),
    "top3_accuracy_pct": round(top3_acc, 2),
    "healthy_recall_pct": round(healthy_acc, 2),
    "diseased_recall_pct": round(diseased_acc, 2),
    "per_crop_accuracy": {c: round((st["top1"] / st["total"]) * 100, 2) for c, st in per_crop_stats.items()},
    "healthy_classes": {
        c: round((st["top1"] / st["total"]) * 100, 2)
        for c, st in per_class_stats.items() if "healthy" in c.lower()
    },
    "top_confusions": [
        {"true": k[0], "predicted": k[1], "count": v}
        for k, v in sorted(confusion_pairs.items(), key=lambda item: item[1], reverse=True)[:10]
    ]
}

with open(OUTPUT_REPORT_PATH, "w") as f:
    json.dump(report_data, f, indent=2)

print(f"\nReport written to {OUTPUT_REPORT_PATH}")
