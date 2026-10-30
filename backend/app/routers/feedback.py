"""
Farmer & Agronomist Diagnostic Feedback Router.
Stores feedback separately without corrupting ground-truth models.
"""

from fastapi import APIRouter, HTTPException, status
from app.database import db_session
from app.schemas import FeedbackCreate, FeedbackResponse

router = APIRouter(tags=["Feedback"])


@router.post("/feedback", response_model=FeedbackResponse)
def submit_feedback(payload: FeedbackCreate):
    valid_types = {"correct", "incorrect", "poor_image", "expert_required"}
    if payload.feedback_type not in valid_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid feedback type '{payload.feedback_type}'. Allowed: {', '.join(valid_types)}"
        )

    with db_session() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO user_feedback (analysis_id, feedback_type, comment, crop_name, predicted_disease)
        VALUES (?, ?, ?, ?, ?)
        """, (
            payload.analysis_id,
            payload.feedback_type,
            payload.comment,
            payload.crop_name,
            payload.predicted_disease
        ))
        feedback_id = cursor.lastrowid

        # Update status in history table for quick UI badge display
        cursor.execute("""
        UPDATE analysis_history SET feedback_status = ? WHERE id = ?
        """, (payload.feedback_type, payload.analysis_id))

    return FeedbackResponse(
        success=True,
        message="Feedback logged successfully for agricultural review.",
        feedback_id=feedback_id
    )
