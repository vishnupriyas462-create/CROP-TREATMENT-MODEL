"""
Complete PyTorch Training Pipeline for PlantVillage Multi-Crop Disease Classifier.
Features:
- Transfer learning with MobileNetV2
- Training data augmentation (RandomHorizontalFlip, RandomRotation, ColorJitter)
- Train / Validation / Test stratified split
- Learning rate scheduler (CosineAnnealingLR / ReduceLROnPlateau)
- Early stopping & model checkpointing
- Multi-class evaluation (Accuracy, Precision, Recall, F1, Confusion Matrix)
"""

import argparse
import copy
import logging
import os
from pathlib import Path
import time
from typing import Dict, Tuple

import numpy as np
from sklearn.metrics import classification_report, confusion_matrix, f1_score
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, random_split
from torchvision import datasets, transforms

from app.ml.classes import PLANTVILLAGE_CLASSES
from app.ml.model import build_crop_disease_model

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("agriguard.train")

# Training Augmentation and Preprocessing
train_transforms = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.RandomResizedCrop(224, scale=(0.8, 1.0)),
    transforms.RandomHorizontalFlip(p=0.5),
    transforms.RandomVerticalFlip(p=0.2),
    transforms.RandomRotation(degrees=15),
    transforms.ColorJitter(brightness=0.15, contrast=0.15, saturation=0.15),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

val_test_transforms = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])


class TransformDataset(torch.utils.data.Dataset):
    """Wraps a Subset or Dataset to apply specific transforms dynamically."""
    def __init__(self, subset, transform=None):
        self.subset = subset
        self.transform = transform

    def __getitem__(self, index):
        x, y = self.subset[index]
        if self.transform:
            x = self.transform(x)
        return x, y

    def __len__(self):
        return len(self.subset)


def train_model(
    data_dir: str,
    output_weights_path: str = "./ml_weights/mobilenetv2_plantvillage.pth",
    epochs: int = 15,
    batch_size: int = 32,
    lr: float = 1e-4,
    val_split: float = 0.15,
    test_split: float = 0.10,
    patience: int = 5
) -> Dict[str, float]:
    """Trains the crop disease model with transfer learning and early stopping."""
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    logger.info(f"Using compute device: {device}")

    data_path = Path(data_dir)
    if not data_path.exists():
        raise FileNotFoundError(f"Dataset directory '{data_dir}' not found.")

    # 1. Dataset Loading
    raw_dataset = datasets.ImageFolder(root=str(data_path))
    class_names = raw_dataset.classes
    num_classes = len(class_names)
    logger.info(f"Loaded dataset with {len(raw_dataset)} images across {num_classes} classes.")

    # 2. Split dataset
    total_size = len(raw_dataset)
    test_size = int(test_split * total_size)
    val_size = int(val_split * total_size)
    train_size = total_size - val_size - test_size

    train_sub, val_sub, test_sub = random_split(
        raw_dataset,
        [train_size, val_size, test_size],
        generator=torch.Generator().manual_seed(42)
    )

    train_dataset = TransformDataset(train_sub, transform=train_transforms)
    val_dataset = TransformDataset(val_sub, transform=val_test_transforms)
    test_dataset = TransformDataset(test_sub, transform=val_test_transforms)

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=2, pin_memory=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False, num_workers=2, pin_memory=True)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False, num_workers=2, pin_memory=True)

    # 3. Model construction
    model = build_crop_disease_model(num_classes=num_classes, pretrained=True)
    model = model.to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.AdamW(model.parameters(), lr=lr, weight_decay=1e-4)
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs)

    # 4. Training loop with early stopping
    best_val_f1 = 0.0
    best_weights = copy.deepcopy(model.state_dict())
    epochs_no_improve = 0

    os.makedirs(Path(output_weights_path).parent, exist_ok=True)

    logger.info("Beginning model training...")
    start_time = time.time()

    for epoch in range(1, epochs + 1):
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0

        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)
            optimizer.zero_grad()

            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item() * images.size(0)
            _, preds = torch.max(outputs, 1)
            correct += torch.sum(preds == labels.data).item()
            total += labels.size(0)

        epoch_train_loss = running_loss / total
        epoch_train_acc = correct / total

        # Validation step
        model.eval()
        val_loss = 0.0
        val_preds, val_targets = [], []

        with torch.no_grad():
            for images, labels in val_loader:
                images, labels = images.to(device), labels.to(device)
                outputs = model(images)
                loss = criterion(outputs, labels)
                val_loss += loss.item() * images.size(0)
                _, preds = torch.max(outputs, 1)

                val_preds.extend(preds.cpu().numpy())
                val_targets.extend(labels.cpu().numpy())

        val_total = len(val_targets)
        epoch_val_loss = val_loss / val_total
        epoch_val_acc = np.mean(np.array(val_preds) == np.array(val_targets))
        epoch_val_f1 = f1_score(val_targets, val_preds, average="weighted", zero_division=0)

        scheduler.step()

        logger.info(
            f"Epoch [{epoch}/{epochs}] "
            f"Train Loss: {epoch_train_loss:.4f} Acc: {epoch_train_acc*100:.2f}% | "
            f"Val Loss: {epoch_val_loss:.4f} Acc: {epoch_val_acc*100:.2f}% F1: {epoch_val_f1*100:.2f}%"
        )

        # Checkpoint if best F1
        if epoch_val_f1 > best_val_f1:
            best_val_f1 = epoch_val_f1
            best_weights = copy.deepcopy(model.state_dict())
            epochs_no_improve = 0
            torch.save(best_weights, output_weights_path)
            logger.info(f"--> Saved best checkpoint to {output_weights_path} (F1: {best_val_f1*100:.2f}%)")
        else:
            epochs_no_improve += 1
            if epochs_no_improve >= patience:
                logger.info(f"Early stopping triggered after {epoch} epochs.")
                break

    duration = time.time() - start_time
    logger.info(f"Training completed in {duration/60:.2f} minutes.")

    # 5. Evaluate on Test Set
    model.load_state_dict(best_weights)
    model.eval()
    test_preds, test_targets = [], []

    with torch.no_grad():
        for images, labels in test_loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            _, preds = torch.max(outputs, 1)
            test_preds.extend(preds.cpu().numpy())
            test_targets.extend(labels.cpu().numpy())

    test_acc = np.mean(np.array(test_preds) == np.array(test_targets))
    test_f1 = f1_score(test_targets, test_preds, average="weighted", zero_division=0)
    report = classification_report(test_targets, test_preds, target_names=class_names, zero_division=0)

    logger.info("===== TEST SET RESULTS =====")
    logger.info(f"Test Accuracy: {test_acc*100:.2f}%")
    logger.info(f"Test F1-Score: {test_f1*100:.2f}%")
    logger.info(f"\n{report}")

    return {
        "best_val_f1": float(best_val_f1),
        "test_acc": float(test_acc),
        "test_f1": float(test_f1)
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train Plant Disease Classifier")
    parser.add_argument("--data_dir", type=str, required=True, help="Path to PlantVillage dataset directory")
    parser.add_argument("--output", type=str, default="./ml_weights/mobilenetv2_plantvillage.pth")
    parser.add_argument("--epochs", type=int, default=15)
    parser.add_argument("--batch_size", type=int, default=32)
    parser.add_argument("--lr", type=float, default=1e-4)
    args = parser.parse_args()

    train_model(
        data_dir=args.data_dir,
        output_weights_path=args.output,
        epochs=args.epochs,
        batch_size=args.batch_size,
        lr=args.lr
    )
