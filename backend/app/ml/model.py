"""
PyTorch Neural Network Architecture for Crop Leaf Disease Classification.
Uses MobileNetV2 with custom head tailored to PlantVillage multi-crop classes.
"""

import torch
import torch.nn as nn
from torchvision import models
from torchvision.models import MobileNet_V2_Weights


def build_crop_disease_model(num_classes: int = 38, pretrained: bool = False) -> nn.Module:
    """
    Constructs a MobileNetV2 architecture with a custom classification head
    tailored for plant leaf disease recognition.
    """
    weights = MobileNet_V2_Weights.DEFAULT if pretrained else None
    try:
        model = models.mobilenet_v2(weights=weights)
    except Exception:
        # Fallback if offline / weights unavailable
        model = models.mobilenet_v2(weights=None)

    in_features = model.classifier[1].in_features
    model.classifier = nn.Sequential(
        nn.Dropout(p=0.3),
        nn.Linear(in_features, 256),
        nn.ReLU(inplace=True),
        nn.Dropout(p=0.2),
        nn.Linear(256, num_classes)
    )
    return model
