"""
Extracts authentic PlantVillage images from Hugging Face data.zip
and trains/fine-tunes the PyTorch MobileNetV2 model.
"""

import os
import zipfile
from pathlib import Path
from collections import defaultdict
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import transforms, datasets
from torch.utils.data import DataLoader, random_split

from app.ml.classes import PLANTVILLAGE_CLASSES
from app.ml.model import build_crop_disease_model

ZIP_PATH = Path(os.environ["USERPROFILE"]) / ".cache" / "huggingface" / "hub" / "datasets--mohanty--PlantVillage" / "snapshots" / "9e97599868962bd0079b8db4b7f1efa9185fa1e7" / "data.zip"
TARGET_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "plantvillage_dataset"
WEIGHTS_PATH = Path(__file__).resolve().parent.parent.parent / "ml_weights" / "mobilenetv2_plantvillage.pth"


def extract_balanced_subset(samples_per_class: int = 40):
    """Extracts a balanced set of authentic images from raw/color/ for each of the 38 classes."""
    print(f"Reading archive: {ZIP_PATH}...")
    if not ZIP_PATH.exists():
        raise FileNotFoundError(f"Archive not found: {ZIP_PATH}")

    TARGET_DIR.mkdir(parents=True, exist_ok=True)
    counts = defaultdict(int)

    with zipfile.ZipFile(ZIP_PATH, 'r') as zf:
        for member in zf.namelist():
            # Match only raw/color/<class>/<file>.JPG or .png
            if member.startswith("raw/color/") and not member.endswith("/"):
                parts = member.split("/")
                if len(parts) >= 4:
                    cls_name = parts[2]
                    if cls_name in PLANTVILLAGE_CLASSES:
                        if counts[cls_name] < samples_per_class:
                            # Extract this file
                            dest_class_dir = TARGET_DIR / cls_name
                            dest_class_dir.mkdir(parents=True, exist_ok=True)
                            dest_file = dest_class_dir / Path(member).name
                            
                            with zf.open(member) as src, open(dest_file, "wb") as dst:
                                dst.write(src.read())
                            
                            counts[cls_name] += 1

    total_extracted = sum(counts.values())
    print(f"Extracted {total_extracted} real PlantVillage images across {len(counts)} classes into {TARGET_DIR}.")
    return total_extracted


def train_quick_epochs(epochs: int = 5, batch_size: int = 32, lr: float = 2e-4):
    """Fine-tunes the MobileNetV2 model on the extracted PlantVillage dataset."""
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Training on device: {device}")

    train_tfms = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.RandomHorizontalFlip(),
        transforms.RandomRotation(15),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

    dataset = datasets.ImageFolder(root=str(TARGET_DIR), transform=train_tfms)
    print(f"Dataset classes detected: {len(dataset.classes)}, Total images: {len(dataset)}")

    # Align class indices
    num_classes = len(PLANTVILLAGE_CLASSES)
    model = build_crop_disease_model(num_classes=num_classes, pretrained=True)
    model.to(device)

    # Class weights or standard CrossEntropy
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.AdamW(model.classifier.parameters(), lr=lr, weight_decay=1e-4)

    loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

    model.train()
    for ep in range(1, epochs + 1):
        running_loss = 0.0
        correct = 0
        total = 0

        for imgs, labels in loader:
            imgs, labels = imgs.to(device), labels.to(device)
            optimizer.zero_grad()
            outs = model(imgs)
            loss = criterion(outs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item() * imgs.size(0)
            _, preds = torch.max(outs, 1)
            correct += torch.sum(preds == labels).item()
            total += labels.size(0)

        epoch_acc = (correct / total) * 100 if total > 0 else 0
        epoch_loss = running_loss / total if total > 0 else 0
        print(f"Epoch [{ep}/{epochs}] - Loss: {epoch_loss:.4f} - Accuracy: {epoch_acc:.2f}%")

    # Save trained checkpoint
    WEIGHTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    torch.save(model.state_dict(), WEIGHTS_PATH)
    print(f"Successfully saved fine-tuned PlantVillage model weights to: {WEIGHTS_PATH}")
    print(f"Model file size: {WEIGHTS_PATH.stat().st_size / (1024*1024):.2f} MB")


if __name__ == "__main__":
    extract_balanced_subset(samples_per_class=35)
    train_quick_epochs(epochs=4, batch_size=32)
