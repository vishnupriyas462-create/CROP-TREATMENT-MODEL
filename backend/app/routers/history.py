"""
Analysis History, Individual Report Details, Deletion, and PDF Export Endpoints.
"""

import json
from typing import List, Optional
from fastapi import APIRouter, HTTPException, status, Response, Query
from app.database import db_session
from app.schemas import AnalysisRecordResponse
from app.services.pdf_service import generate_crop_health_pdf

router = APIRouter(tags=["History & Reports"])


@router.get("/history", response_model=List[AnalysisRecordResponse])
def get_history(
    crop: Optional[str] = Query(None, description="Filter by crop name"),
    status_filter: Optional[str] = Query(None, description="all, healthy, diseased"),
    limit: int = Query(50, ge=1, le=200)
):
    with db_session() as conn:
        cursor = conn.cursor()
        sql = "SELECT * FROM analysis_history WHERE 1=1"
        params = []

        if crop and crop.lower() != "all":
            sql += " AND LOWER(crop_name) = ?"
            params.append(crop.lower().strip())

        if status_filter == "healthy":
            sql += " AND is_healthy = 1"
        elif status_filter == "diseased":
            sql += " AND is_healthy = 0"

        sql += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)

        cursor.execute(sql, params)
        rows = cursor.fetchall()

        results = []
        for r in rows:
            record = dict(r)
            record["alternatives"] = json.loads(record.get("alternatives_json") or "[]")
            record["guidance"] = json.loads(record.get("guidance_json") or "[]")
            results.append(AnalysisRecordResponse(**record))

        return results


@router.get("/history/{analysis_id}", response_model=AnalysisRecordResponse)
def get_analysis_by_id(analysis_id: str):
    with db_session() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM analysis_history WHERE id = ?", (analysis_id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Analysis report '{analysis_id}' not found."
            )
        record = dict(row)
        record["alternatives"] = json.loads(record.get("alternatives_json") or "[]")
        record["guidance"] = json.loads(record.get("guidance_json") or "[]")
        return AnalysisRecordResponse(**record)


@router.delete("/history/{analysis_id}")
def delete_analysis(analysis_id: str):
    with db_session() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM analysis_history WHERE id = ?", (analysis_id,))
        if not cursor.fetchone():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Analysis report '{analysis_id}' not found."
            )
        cursor.execute("DELETE FROM analysis_history WHERE id = ?", (analysis_id,))
        return {"success": True, "message": f"Report '{analysis_id}' successfully deleted."}


@router.get("/history/{analysis_id}/pdf")
def export_pdf_report(analysis_id: str):
    with db_session() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM analysis_history WHERE id = ?", (analysis_id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Analysis report '{analysis_id}' not found."
            )
        record = dict(row)
        record["alternatives"] = json.loads(record.get("alternatives_json") or "[]")
        record["guidance"] = json.loads(record.get("guidance_json") or "[]")

        pdf_bytes = generate_crop_health_pdf(record)
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=AgriGuard_Report_{analysis_id}.pdf"
            }
        )
