"""
Pydantic Schemas for Request and Response Validation.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
    model_loaded: bool
    model_architecture: str
    database_connected: bool
    environment: str


class CropResponse(BaseModel):
    code: str
    common_name: str
    common_name_ta: str
    scientific_name: Optional[str] = None
    category: str
    description: Optional[str] = None
    description_ta: Optional[str] = None
    icon: Optional[str] = None


class GuidanceItem(BaseModel):
    id: int
    crop_code: str
    target_disease_or_pest: str
    treatment_category: str  # fungicide, insecticide, bactericide, biological, cultural, organic
    active_ingredient: Optional[str] = None
    approved_product_name: Optional[str] = None
    dosage_guidance: Optional[str] = None
    non_chemical_control: str
    prevention_practices: str
    source_org: str
    source_url: Optional[str] = None
    reference_citation: str
    jurisdiction: str
    approved_label_restrictions: Optional[str] = None
    safety_precautions: str
    harvest_waiting_period_days: int
    verification_date: str


class AlternativeDiagnosis(BaseModel):
    class_name: str
    crop: str
    crop_ta: str
    disease: str
    disease_ta: str
    disease_type: str
    confidence_pct: float
    is_healthy: bool


class ActionPlan(BaseModel):
    urgency: str
    urgency_ta: str
    step_1_immediate: str
    step_1_immediate_ta: str
    step_2_biological_cultural: str
    step_2_biological_cultural_ta: str
    step_3_chemical_application: str
    step_3_chemical_application_ta: str
    step_4_monitoring: str
    step_4_monitoring_ta: str
    critical_donots: List[str]
    critical_donots_ta: List[str]


class PredictionResponse(BaseModel):
    success: bool
    analysis_id: str
    timestamp: str
    class_name: str
    crop: str
    crop_ta: str
    disease: str
    disease_ta: str
    disease_type: str
    severity: str
    is_healthy: bool
    confidence_score: float
    confidence_pct: float
    confidence_level: str
    confidence_interpretation: str
    is_uncertain: bool
    model_version: str
    model_weights_loaded: bool
    symptoms: str
    symptoms_ta: str
    causes: str
    causes_ta: str
    next_steps: str
    next_steps_ta: str
    prevention: str
    prevention_ta: str
    ipm: str
    action_plan: Optional[ActionPlan] = None
    alternatives: List[AlternativeDiagnosis] = []
    verified_guidance: List[GuidanceItem] = []
    has_verified_treatment: bool
    warning_notice: Optional[str] = None
    image_preview: Optional[str] = None


class AnalysisRecordResponse(BaseModel):
    id: str
    timestamp: str
    crop_name: str
    crop_name_ta: Optional[str] = None
    disease_name: str
    disease_name_ta: Optional[str] = None
    disease_type: str
    confidence: float
    is_healthy: bool
    is_uncertain: bool
    growth_stage: Optional[str] = None
    district: Optional[str] = None
    image_data_url: Optional[str] = None
    symptoms_summary: Optional[str] = None
    alternatives: List[Dict[str, Any]] = []
    guidance: List[Dict[str, Any]] = []
    feedback_status: Optional[str] = "none"
    notes: Optional[str] = None


class FeedbackCreate(BaseModel):
    analysis_id: str
    feedback_type: str = Field(..., description="correct, incorrect, poor_image, expert_required")
    comment: Optional[str] = None
    crop_name: Optional[str] = None
    predicted_disease: Optional[str] = None


class FeedbackResponse(BaseModel):
    success: bool
    message: str
    feedback_id: int


class AnalyticsCropStat(BaseModel):
    crop: str
    count: int


class AnalyticsTypeStat(BaseModel):
    type: str
    count: int


class AnalyticsResponse(BaseModel):
    total_analyses: int
    healthy_count: int
    diseased_count: int
    uncertain_count: int
    crop_distribution: List[AnalyticsCropStat]
    disease_type_distribution: List[AnalyticsTypeStat]
    recent_history: List[Dict[str, Any]]


class AdvisoryContactResponse(BaseModel):
    id: int
    organization: str
    service_type: str
    phone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    state_region: Optional[str] = None
    notes: Optional[str] = None
