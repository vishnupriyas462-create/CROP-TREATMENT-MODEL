"""
Utility to create sample crop leaf test images for automated testing and demo analysis.
"""

from pathlib import Path
import numpy as np
import cv2

def create_sample_leaf_images(output_dir: str = "./tests/sample_images"):
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    # 1. Healthy green leaf texture (256x256)
    img_healthy = np.zeros((256, 256, 3), dtype=np.uint8)
    # Green background
    img_healthy[:] = [45, 140, 50]
    # Add vein-like textures
    cv2.line(img_healthy, (128, 20), (128, 236), (60, 180, 70), 3)
    for y in range(40, 220, 30):
        cv2.line(img_healthy, (128, y), (50, y - 15), (55, 170, 65), 2)
        cv2.line(img_healthy, (128, y), (206, y - 15), (55, 170, 65), 2)
    # Smooth a bit
    img_healthy = cv2.GaussianBlur(img_healthy, (5, 5), 0)
    cv2.imwrite(str(out_path / "sample_healthy_leaf.jpg"), cv2.cvtColor(img_healthy, cv2.COLOR_RGB2BGR))

    # 2. Diseased leaf with dark concentric target lesions (Early Blight simulation)
    img_diseased = img_healthy.copy()
    # Draw necrotic brown/black target spot with concentric rings
    cv2.circle(img_diseased, (90, 110), 28, (180, 170, 50), -1)   # yellow halo
    cv2.circle(img_diseased, (90, 110), 22, (50, 40, 30), -1)     # dark brown necrotic center
    cv2.circle(img_diseased, (90, 110), 15, (80, 60, 40), 2)      # ring 1
    cv2.circle(img_diseased, (90, 110), 8, (40, 30, 20), 2)       # center target

    # Second lesion
    cv2.circle(img_diseased, (160, 160), 24, (170, 160, 45), -1)
    cv2.circle(img_diseased, (160, 160), 18, (45, 35, 25), -1)
    cv2.circle(img_diseased, (160, 160), 10, (75, 55, 35), 2)

    img_diseased = cv2.GaussianBlur(img_diseased, (3, 3), 0)
    cv2.imwrite(str(out_path / "sample_diseased_leaf.jpg"), cv2.cvtColor(img_diseased, cv2.COLOR_RGB2BGR))

    # 3. Non-leaf invalid image (plain bright blue sky background, no foliar colors)
    img_non_leaf = np.zeros((256, 256, 3), dtype=np.uint8)
    img_non_leaf[:] = [30, 144, 255] # Sky blue (RGB)
    cv2.imwrite(str(out_path / "sample_non_leaf.jpg"), cv2.cvtColor(img_non_leaf, cv2.COLOR_RGB2BGR))

    print(f"Generated sample images in {out_path.resolve()}")

if __name__ == "__main__":
    create_sample_leaf_images()
