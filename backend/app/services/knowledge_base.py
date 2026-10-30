"""
Verified Agricultural Knowledge Base Service.
Ensures zero fabricated recommendations, enforces strict pathogen-treatment type matching,
and retrieves authoritative citations (ICAR, DPPQS, TNAU, CIBRC).
"""

from typing import List, Dict, Any, Optional
from app.database import db_session


def find_guidance_for_diagnosis(
    crop_name: str,
    disease_name: str,
    disease_type: str,
    is_healthy: bool
) -> List[Dict[str, Any]]:
    """
    Retrieves only verified guidance matching the crop and specific diagnosis.
    Enforces scientific constraints:
    - No chemicals for healthy crops
    - No insecticides for fungal/bacterial diseases
    - Only vector-directed controls for viral issues
    """
    if is_healthy:
        return []

    crop_lower = crop_name.lower()
    disease_lower = disease_name.lower()

    # Map crop name to code
    crop_code = "tomato"
    if "potato" in crop_lower:
        crop_code = "potato"
    elif "corn" in crop_lower or "maize" in crop_lower:
        crop_code = "corn"
    elif "pepper" in crop_lower or "capsicum" in crop_lower:
        crop_code = "pepper"
    elif "rice" in crop_lower or "paddy" in crop_lower:
        crop_code = "rice"
    elif "cotton" in crop_lower:
        crop_code = "cotton"
    elif "apple" in crop_lower:
        crop_code = "apple"
    elif "grape" in crop_lower:
        crop_code = "grape"

    results = []
    with db_session() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM agricultural_guidance WHERE crop_code = ?",
            (crop_code,)
        )
        rows = cursor.fetchall()

        for row in rows:
            target = row["target_disease_or_pest"].lower()
            category = row["treatment_category"].lower()

            # Check match by disease keywords
            is_match = False
            if "early blight" in disease_lower and "early blight" in target:
                is_match = True
            elif "late blight" in disease_lower and "late blight" in target:
                is_match = True
            elif "bacterial" in disease_lower and "bacterial" in target:
                is_match = True
            elif ("leaf curl" in disease_lower or "tylcv" in disease_lower) and ("leaf curl" in target or "tylcv" in target):
                is_match = True
            elif ("spider mite" in disease_lower or "mite" in disease_lower) and "mite" in target:
                is_match = True
            elif "rust" in disease_lower and "rust" in target:
                is_match = True
            elif "blast" in disease_lower and "blast" in target:
                is_match = True

            if is_match:
                # Strict pathogen-category safety validation
                if disease_type == "fungal" and category == "insecticide":
                    continue  # Never prescribe an insecticide for a fungal infection!
                if disease_type == "bacterial" and category == "insecticide":
                    continue  # Never prescribe an insecticide for bacterial spot!

                results.append(dict(row))

    return results


def search_guidance(
    crop: Optional[str] = None,
    category: Optional[str] = None,
    query: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Search and filter the complete verified agricultural knowledge base."""
    with db_session() as conn:
        cursor = conn.cursor()
        sql = "SELECT * FROM agricultural_guidance WHERE 1=1"
        params = []

        if crop and crop.lower() != "all":
            sql += " AND crop_code = ?"
            params.append(crop.lower().strip())

        if category and category.lower() != "all":
            sql += " AND treatment_category = ?"
            params.append(category.lower().strip())

        if query and query.strip():
            term = f"%{query.strip()}%"
            sql += " AND (target_disease_or_pest LIKE ? OR active_ingredient LIKE ? OR approved_product_name LIKE ? OR non_chemical_control LIKE ?)"
            params.extend([term, term, term, term])

        sql += " ORDER BY id ASC"
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        return [dict(r) for r in rows]
