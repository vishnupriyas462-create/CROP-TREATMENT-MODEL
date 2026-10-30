"""
Verified Agricultural Guidance and Pesticide/IPM Knowledge Base Endpoints.
"""

from typing import List, Optional
from fastapi import APIRouter, Query
from app.schemas import GuidanceItem
from app.services.knowledge_base import search_guidance

router = APIRouter(tags=["Guidance & Knowledge Base"])


@router.get("/recommendations", response_model=List[GuidanceItem])
def get_recommendations(
    crop: Optional[str] = Query(None, description="Crop filter (tomato, potato, corn, pepper, rice, cotton, etc.)"),
    category: Optional[str] = Query(None, description="Category filter (fungicide, insecticide, bactericide, biological, organic)"),
    search: Optional[str] = Query(None, description="Keyword search in disease name, active ingredient, or product")
):
    """
    Search and filter verified agricultural guidance with official ICAR, DPPQS, and TNAU citations.
    """
    rows = search_guidance(crop=crop, category=category, query=search)
    return [GuidanceItem(**r) for r in rows]
