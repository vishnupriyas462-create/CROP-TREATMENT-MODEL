import requests
from pathlib import Path

BASE_URL = "http://localhost:8001"

# 1. Health check
res = requests.get(f"{BASE_URL}/api/health")
print("Health Check:", res.status_code, res.json())

# 2. Test predict with real healthy tomato leaf
healthy_tomato_path = Path("frontend/public/samples/sample_healthy_tomato.jpg")
with open(healthy_tomato_path, "rb") as f:
    files = {"file": ("healthy_tomato.jpg", f, "image/jpeg")}
    data = {"crop_hint": "tomato"}
    res = requests.post(f"{BASE_URL}/api/predict", files=files, data=data)
    print("\n--- Test: Healthy Tomato Leaf ---")
    print("Status:", res.status_code)
    pred = res.json()
    print(f"Crop: {pred.get('crop')} | Disease: {pred.get('disease')}")
    print(f"Is Healthy: {pred.get('is_healthy')} | Confidence: {pred.get('confidence_pct')}%")
    print(f"Severity: {pred.get('severity')}")

# 3. Test predict with real early blight tomato leaf
early_blight_path = Path("frontend/public/samples/sample_early_blight_tomato.jpg")
with open(early_blight_path, "rb") as f:
    files = {"file": ("early_blight.jpg", f, "image/jpeg")}
    data = {"crop_hint": "tomato"}
    res = requests.post(f"{BASE_URL}/api/predict", files=files, data=data)
    print("\n--- Test: Early Blight Tomato Leaf ---")
    print("Status:", res.status_code)
    pred = res.json()
    print(f"Crop: {pred.get('crop')} | Disease: {pred.get('disease')}")
    print(f"Is Healthy: {pred.get('is_healthy')} | Confidence: {pred.get('confidence_pct')}%")
    print(f"Severity: {pred.get('severity')}")
    if pred.get("action_plan"):
        print("Action Plan Hour 0:", pred["action_plan"].get("hour_0"))

# 4. Test predict with real healthy potato leaf
healthy_potato_path = Path("frontend/public/samples/sample_healthy_potato.jpg")
with open(healthy_potato_path, "rb") as f:
    files = {"file": ("healthy_potato.jpg", f, "image/jpeg")}
    data = {"crop_hint": "potato"}
    res = requests.post(f"{BASE_URL}/api/predict", files=files, data=data)
    print("\n--- Test: Healthy Potato Leaf ---")
    print("Status:", res.status_code)
    pred = res.json()
    print(f"Crop: {pred.get('crop')} | Disease: {pred.get('disease')}")
    print(f"Is Healthy: {pred.get('is_healthy')} | Confidence: {pred.get('confidence_pct')}%")
