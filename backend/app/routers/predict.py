"""
Core Image Classification and Diagnostic Prediction Router.
"""

import base64
import io
import json
import uuid
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, File, UploadFile, Form, HTTPException, status
from PIL import Image

from app.config import settings
from app.database import db_session
from app.ml.inference import CropDiseaseClassifier
from app.schemas import PredictionResponse, GuidanceItem, AlternativeDiagnosis
from app.services.knowledge_base import find_guidance_for_diagnosis

router = APIRouter(tags=["Prediction"])


@router.post("/predict", response_model=PredictionResponse)
async def predict_crop_disease(
    file: UploadFile = File(...),
    crop_hint: Optional[str] = Form("auto"),
    district: Optional[str] = Form(None),
    growth_stage: Optional[str] = Form(None),
    symptoms_notes: Optional[str] = Form(None)
):
    # 1. Validate MIME type
    if file.content_type not in settings.ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type '{file.content_type}'. Supported formats: JPEG, PNG, WebP."
        )

    # 2. Read bytes and validate size
    image_bytes = await file.read()
    max_bytes = settings.MAX_IMAGE_SIZE_MB * 1024 * 1024
    if len(image_bytes) > max_bytes:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"Image size exceeds limit of {settings.MAX_IMAGE_SIZE_MB}MB."
        )

    # 3. Execute PyTorch inference
    classifier = CropDiseaseClassifier.get_instance()
    try:
        result = classifier.predict(image_bytes=image_bytes, crop_hint=crop_hint)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Inference processing error: {str(e)}"
        )

    # Check foliar heuristic check
    if not result.get("success", False):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("message", "The uploaded photograph does not appear to contain a crop leaf.")
        )

    # 4. Query verified agricultural knowledge base
    verified_guidance_rows = find_guidance_for_diagnosis(
        crop_name=result["crop"],
        disease_name=result["disease"],
        disease_type=result["disease_type"],
        is_healthy=result["is_healthy"]
    )

    # 5. Build base64 preview thumbnail for storage and client feedback
    try:
        thumb_img = Image.open(io.BytesIO(image_bytes))
        thumb_img.thumbnail((320, 320))
        buffered = io.BytesIO()
        thumb_img.save(buffered, format="JPEG", quality=80)
        image_preview_url = f"data:image/jpeg;base64,{base64.b64encode(buffered.getvalue()).decode('utf-8')}"
    except Exception:
        image_preview_url = None

    analysis_id = f"AGR-{datetime.now(timezone.utc).strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"
    timestamp_iso = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    # 6. Safety Warning Flag
    warning_notice = None
    if result["is_uncertain"]:
        warning_notice = "Uncertain prediction (Confidence below 60%) — upload a clearer close-up photograph or consult your local Krishi Vigyan Kendra before taking chemical action."

    # 7. Persist to SQLite analysis_history table
    with db_session() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO analysis_history (
            id, timestamp, crop_name, crop_name_ta, disease_name, disease_name_ta,
            disease_type, confidence, is_healthy, is_uncertain, growth_stage,
            district, image_data_url, symptoms_summary, alternatives_json,
            guidance_json, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            analysis_id,
            timestamp_iso,
            result["crop"],
            result["crop_ta"],
            result["disease"],
            result["disease_ta"],
            result["disease_type"],
            result["confidence_pct"],
            1 if result["is_healthy"] else 0,
            1 if result["is_uncertain"] else 0,
            growth_stage,
            district,
            image_preview_url,
            result["symptoms"],
            json.dumps(result["alternatives"]),
            json.dumps(verified_guidance_rows),
            symptoms_notes
        ))

    # Format verified guidance into Pydantic models
    guidance_items = [
        GuidanceItem(**row) for row in verified_guidance_rows
    ]

    alt_items = [
        AlternativeDiagnosis(**alt) for alt in result["alternatives"]
    ]

    return PredictionResponse(
        success=True,
        analysis_id=analysis_id,
        timestamp=timestamp_iso,
        class_name=result["class_name"],
        crop=result["crop"],
        crop_ta=result["crop_ta"],
        disease=result["disease"],
        disease_ta=result["disease_ta"],
        disease_type=result["disease_type"],
        severity=result["severity"],
        is_healthy=result["is_healthy"],
        confidence_score=result["confidence_score"],
        confidence_pct=result["confidence_pct"],
        confidence_level=result["confidence_level"],
        confidence_interpretation=result["confidence_interpretation"],
        is_uncertain=result["is_uncertain"],
        model_version=result["model_version"],
        model_weights_loaded=result["model_weights_loaded"],
        symptoms=result["symptoms"],
        symptoms_ta=result["symptoms_ta"],
        causes=result["causes"],
        causes_ta=result["causes_ta"],
        next_steps=result["next_steps"],
        next_steps_ta=result["next_steps_ta"],
        prevention=result["prevention"],
        prevention_ta=result["prevention_ta"],
        ipm=result["ipm"],
        action_plan=result.get("action_plan"),
        alternatives=alt_items,
        verified_guidance=guidance_items,
        has_verified_treatment=len(guidance_items) > 0,
        warning_notice=warning_notice,
        image_preview=image_preview_url
    )
