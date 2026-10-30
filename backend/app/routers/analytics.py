"""
Dashboard Analytics Router.
Aggregates authentic database records for live statistics and chart distributions.
"""

from fastapi import APIRouter
from app.database import db_session
from app.schemas import AnalyticsResponse, AnalyticsCropStat, AnalyticsTypeStat

router = APIRouter(tags=["Analytics"])


@router.get("/analytics", response_model=AnalyticsResponse)
def get_analytics():
    with db_session() as conn:
        cursor = conn.cursor()

        # 1. Total counts
        cursor.execute("SELECT COUNT(*) FROM analysis_history")
        total = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM analysis_history WHERE is_healthy = 1")
        healthy = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM analysis_history WHERE is_healthy = 0")
        diseased = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM analysis_history WHERE is_uncertain = 1")
        uncertain = cursor.fetchone()[0]

        # 2. Crop distribution
        cursor.execute("""
        SELECT crop_name, COUNT(*) as cnt 
        FROM analysis_history 
        GROUP BY crop_name 
        ORDER BY cnt DESC 
        LIMIT 6
        """)
        crop_rows = cursor.fetchall()
        crop_stats = [
            AnalyticsCropStat(crop=row["crop_name"], count=row["cnt"])
            for row in crop_rows
        ]

        # 3. Disease type distribution
        cursor.execute("""
        SELECT disease_type, COUNT(*) as cnt 
        FROM analysis_history 
        GROUP BY disease_type 
        ORDER BY cnt DESC
        """)
        type_rows = cursor.fetchall()
        type_stats = [
            AnalyticsTypeStat(type=row["disease_type"].title(), count=row["cnt"])
            for row in type_rows
        ]

        # 4. Recent analyses
        cursor.execute("""
        SELECT id, timestamp, crop_name, disease_name, confidence, is_healthy, is_uncertain, feedback_status
        FROM analysis_history
        ORDER BY timestamp DESC
        LIMIT 5
        """)
        recent_rows = cursor.fetchall()
        recent_list = [dict(r) for r in recent_rows]

        return AnalyticsResponse(
            total_analyses=total,
            healthy_count=healthy,
            diseased_count=diseased,
            uncertain_count=uncertain,
            crop_distribution=crop_stats,
            disease_type_distribution=type_stats,
            recent_history=recent_list
        )
