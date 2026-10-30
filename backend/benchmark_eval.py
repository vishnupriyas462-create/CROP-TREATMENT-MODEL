import os
import time
import zipfile
import io
from pathlib import Path
from PIL import Image
import torch
from torchvision import transforms
from transformers import MobileNetV2ForImageClassification

torch.set_num_threads(8)

zip_path = Path(os.environ["USERPROFILE"]) / ".cache" / "huggingface" / "hub" / "datasets--mohanty--PlantVillage" / "snapshots" / "9e97599868962bd0079b8db4b7f1efa9185fa1e7" / "data.zip"
model_path = Path(r"c:\Users\Admin\cdis\backend\ml_weights\plant_disease_model")

print("Loading model...")
model = MobileNetV2ForImageClassification.from_pretrained(str(model_path))
model.eval()

tfms = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

print("Gathering 100 sample members from zip...")
samples = []
with zipfile.ZipFile(zip_path, 'r') as zf:
    for name in zf.namelist():
        if name.startswith("raw/color/") and not name.endswith("/"):
            samples.append(name)
            if len(samples) >= 100:
                break

print(f"Benchmarking inference on {len(samples)} images...")
t0 = time.time()
with zipfile.ZipFile(zip_path, 'r') as zf:
    batch = []
    for s in samples:
        img_bytes = zf.read(s)
        img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
        tensor = tfms(img)
        batch.append(tensor)
        if len(batch) == 20:
            b_tensor = torch.stack(batch)
            with torch.no_grad():
                _ = model(b_tensor)
            batch = []

t1 = time.time()
elapsed = t1 - t0
rate = len(samples) / elapsed
print(f"Elapsed: {elapsed:.2f}s | Throughput: {rate:.1f} images/sec")
print(f"Estimated time for 1,900 images (50/class): {1900/rate:.1f}s")
print(f"Estimated time for 3,800 images (100/class): {3800/rate:.1f}s")
print(f"Estimated time for 54,305 images: {54305/rate/60:.1f} mins")
