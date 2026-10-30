"""
Evaluation and Confusion Matrix Generator for Crop Disease Classification.
Outputs comprehensive metrics: Accuracy, Precision, Recall, Macro F1, Weighted F1,
and produces a serialized confusion matrix breakdown.
"""

import argparse
import json
import logging
from pathlib import Path
from typing import Dict, Any

import numpy as np
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, precision_recall_fscore_support
import torch
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

from app.ml.classes import PLANTVILLAGE_CLASSES
from app.ml.model import build_crop_disease_model

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("agriguard.evaluate")

eval_transforms = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])


def evaluate_model(
    test_data_dir: str,
    weights_path: str = "./ml_weights/mobilenetv2_plantvillage.pth",
    batch_size: int = 32,
    output_report_json: str = "./ml_weights/evaluation_report.json"
) -> Dict[str, Any]:
    """Evaluates a saved PyTorch checkpoint on an independent test dataset."""
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    logger.info(f"Using device: {device}")

    dataset = datasets.ImageFolder(root=test_data_dir, transform=eval_transforms)
    class_names = dataset.classes
    loader = DataLoader(dataset, batch_size=batch_size, shuffle=False, num_workers=2)

    model = build_crop_disease_model(num_classes=len(class_names), pretrained=False)
    state_dict = torch.load(weights_path, map_location=device)
    model.load_state_dict(state_dict)
    model.to(device)
    model.eval()

    all_preds = []
    all_targets = []

    with torch.no_grad():
        for images, labels in loader:
            images = images.to(device)
            outputs = model(images)
            _, preds = torch.max(outputs, 1)
            all_preds.extend(preds.cpu().numpy())
            all_targets.extend(labels.numpy())

    y_true = np.array(all_targets)
    y_pred = np.array(all_preds)

    acc = accuracy_score(y_true, y_pred)
    prec, rec, f1, _ = precision_recall_fscore_support(y_true, y_pred, average="weighted", zero_division=0)
    macro_prec, macro_rec, macro_f1, _ = precision_recall_fscore_support(y_true, y_pred, average="macro", zero_division=0)
    cm = confusion_matrix(y_true, y_pred)
    clf_report = classification_report(y_true, y_pred, target_names=class_names, output_dict=True, zero_division=0)

    report_payload = {
        "model_architecture": "MobileNetV2",
        "dataset": "PlantVillage Standard Validation/Test Split",
        "num_classes": len(class_names),
        "total_test_samples": len(y_true),
        "accuracy": float(acc),
        "weighted_precision": float(prec),
        "weighted_recall": float(rec),
        "weighted_f1": float(f1),
        "macro_precision": float(macro_prec),
        "macro_recall": float(macro_rec),
        "macro_f1": float(macro_f1),
        "confusion_matrix": cm.tolist(),
        "per_class_metrics": clf_report
    }

    out_file = Path(output_report_json)
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(report_payload, f, indent=2)

    logger.info(f"Evaluation report saved to {out_file}")
    logger.info(f"Accuracy: {acc*100:.2f}%, Weighted F1: {f1*100:.2f}%")
    return report_payload


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate Plant Disease Classifier")
    parser.add_argument("--test_dir", type=str, required=True, help="Path to test image folder")
    parser.add_argument("--weights", type=str, default="./ml_weights/mobilenetv2_plantvillage.pth")
    parser.add_argument("--output", type=str, default="./ml_weights/evaluation_report.json")
    args = parser.parse_args()

    evaluate_model(test_data_dir=args.test_dir, weights_path=args.weights, output_report_json=args.output)
