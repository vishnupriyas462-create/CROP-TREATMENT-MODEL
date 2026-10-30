"""
Crops, Disease Library, and Advisory Directory endpoints.
"""

from typing import List, Dict, Any
from fastapi import APIRouter
from app.database import db_session
from app.schemas import CropResponse, AdvisoryContactResponse
from app.ml.classes import DISEASE_PROFILES

router = APIRouter(tags=["Crops & Library"])


@router.get("/crops", response_model=List[CropResponse])
def get_crops():
    """Retrieve list of crops supported by the system."""
    with db_session() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM crops ORDER BY common_name ASC")
        rows = cursor.fetchall()
        return [dict(r) for r in rows]


@router.get("/diseases")
def get_diseases():
    """Retrieve all supported disease classes with symptom descriptions and IPM guidance."""
    return [
        {"class_code": k, **v}
        for k, v in DISEASE_PROFILES.items()
    ]


@router.get("/advisory-contacts", response_model=List[AdvisoryContactResponse])
def get_advisory_contacts():
    """Official agricultural advisory helplines and university contacts."""
    with db_session() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM advisory_contacts ORDER BY id ASC")
        rows = cursor.fetchall()
        return [dict(r) for r in rows]
