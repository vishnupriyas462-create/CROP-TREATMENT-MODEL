import os
import zipfile
from collections import defaultdict
from pathlib import Path

zip_path = Path(os.environ["USERPROFILE"]) / ".cache" / "huggingface" / "hub" / "datasets--mohanty--PlantVillage" / "snapshots" / "9e97599868962bd0079b8db4b7f1efa9185fa1e7" / "data.zip"
print(f"Reading {zip_path}...")

counts = defaultdict(int)
with zipfile.ZipFile(zip_path, 'r') as zf:
    for name in zf.namelist():
        if name.startswith("raw/color/") and not name.endswith("/"):
            parts = name.split("/")
            if len(parts) >= 4:
                cls_folder = parts[2]
                counts[cls_folder] += 1

print(f"Total classes found in raw/color/: {len(counts)}")
total_imgs = sum(counts.values())
print(f"Total color images: {total_imgs}")
for cls, cnt in sorted(counts.items()):
    print(f"  {cls}: {cnt}")
