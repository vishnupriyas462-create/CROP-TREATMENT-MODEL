"""
Comprehensive API and Machine Learning Pipeline Tests.
"""

from pathlib import Path
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.database import init_db
from app.data.seed_data import seed_database
from app.ml.inference import CropDiseaseClassifier

client = TestClient(app)
SAMPLE_DIR = Path(__file__).resolve().parent / "sample_images"


@pytest.fixture(autouse=True)
def setup_test_db():
    init_db()
    seed_database()


def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ("healthy", "degraded")
    assert "AgriGuard" in data["service"]
    assert data["database_connected"] is True


def test_crops_endpoint():
    response = client.get("/api/crops")
    assert response.status_code == 200
    crops = response.json()
    assert len(crops) >= 5
    codes = [c["code"] for c in crops]
    assert "tomato" in codes
    assert "potato" in codes
    assert "corn" in codes
    assert "rice" in codes


def test_diseases_endpoint():
    response = client.get("/api/diseases")
    assert response.status_code == 200
    diseases = response.json()
    assert len(diseases) > 0
    first = diseases[0]
    assert "disease_ta" in first
    assert "symptoms" in first
    assert "ipm" in first


def test_recommendations_filtering_and_safety():
    # 1. Search for Tomato Early Blight
    response = client.get("/api/recommendations?crop=tomato&search=Early+Blight")
    assert response.status_code == 200
    items = response.json()
    assert len(items) > 0
    for item in items:
        # Crucial Safety check: Early Blight is fungal, so chemical category must NOT be insecticide
        assert item["treatment_category"] in ("fungicide", "biological", "organic", "cultural")
        assert "source_org" in item
        assert "reference_citation" in item

    # 2. Search for all
    response_all = client.get("/api/recommendations")
    assert response_all.status_code == 200
    assert len(response_all.json()) >= 10


def test_predict_foliar_leaf_image():
    leaf_path = SAMPLE_DIR / "sample_diseased_leaf.jpg"
    assert leaf_path.exists()

    with open(leaf_path, "rb") as f:
        response = client.post(
            "/api/predict",
            files={"file": ("leaf.jpg", f, "image/jpeg")},
            data={"crop_hint": "tomato", "growth_stage": "Fruiting", "district": "Salem"}
        )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "analysis_id" in data
    assert "confidence_pct" in data
    assert "crop" in data
    assert "disease" in data
    assert "symptoms_ta" in data
    assert "next_steps" in data
    assert isinstance(data["alternatives"], list)


def test_predict_rejects_non_leaf_image():
    non_leaf_path = SAMPLE_DIR / "sample_non_leaf.jpg"
    assert non_leaf_path.exists()

    with open(non_leaf_path, "rb") as f:
        response = client.post(
            "/api/predict",
            files={"file": ("blue_box.jpg", f, "image/jpeg")}
        )

    # Should be rejected with 400 Bad Request because foliar ratio is near 0
    assert response.status_code == 400
    assert "does not appear to contain a crop leaf" in response.json()["detail"]


def test_history_and_feedback_and_pdf_flow():
    # First, make a prediction
    leaf_path = SAMPLE_DIR / "sample_healthy_leaf.jpg"
    with open(leaf_path, "rb") as f:
        pred_res = client.post(
            "/api/predict",
            files={"file": ("leaf.jpg", f, "image/jpeg")},
            data={"crop_hint": "tomato"}
        )
    assert pred_res.status_code == 200
    analysis_id = pred_res.json()["analysis_id"]

    # 1. Fetch history
    hist_res = client.get("/api/history")
    assert hist_res.status_code == 200
    hist = hist_res.json()
    ids = [item["id"] for item in hist]
    assert analysis_id in ids

    # 2. Fetch specific record
    rec_res = client.get(f"/api/history/{analysis_id}")
    assert rec_res.status_code == 200
    assert rec_res.json()["id"] == analysis_id

    # 3. Submit feedback
    fb_res = client.post(
        "/api/feedback",
        json={
            "analysis_id": analysis_id,
            "feedback_type": "correct",
            "comment": "Accurate prediction on trial plot."
        }
    )
    assert fb_res.status_code == 200
    assert fb_res.json()["success"] is True

    # 4. Generate and download PDF
    pdf_res = client.get(f"/api/history/{analysis_id}/pdf")
    assert pdf_res.status_code == 200
    assert pdf_res.headers["content-type"] == "application/pdf"
    assert len(pdf_res.content) > 1000  # valid PDF bytes

    # 5. Delete analysis
    del_res = client.delete(f"/api/history/{analysis_id}")
    assert del_res.status_code == 200

    # Verify deletion
    not_found = client.get(f"/api/history/{analysis_id}")
    assert not_found.status_code == 404
