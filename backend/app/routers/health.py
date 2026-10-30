"""
Health check and system diagnostics endpoint.
"""

from fastapi import APIRouter
from app.config import settings
from app.database import get_db_connection
from app.ml.inference import CropDiseaseClassifier
from app.schemas import HealthResponse

router = APIRouter(tags=["Health"])


@router.get("/health", response_model=HealthResponse)
def get_health():
    # Test DB connection
    db_ok = False
    try:
        conn = get_db_connection()
        conn.execute("SELECT 1;")
        conn.close()
        db_ok = True
    except Exception:
        db_ok = False

    classifier = CropDiseaseClassifier.get_instance()

    return HealthResponse(
        status="healthy" if db_ok else "degraded",
        service=settings.PROJECT_NAME,
        version=settings.VERSION,
        model_loaded=classifier.model_loaded,
        model_architecture="MobileNetV2 (PyTorch)",
        database_connected=db_ok,
        environment=settings.ENVIRONMENT
    )
