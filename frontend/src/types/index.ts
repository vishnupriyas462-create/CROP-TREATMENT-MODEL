export type Language = 'en' | 'ta';

export interface Crop {
  code: string;
  common_name: string;
  common_name_ta: string;
  scientific_name?: string;
  category: string;
  description?: string;
  description_ta?: string;
  icon?: string;
}

export interface GuidanceItem {
  id: number;
  crop_code: string;
  target_disease_or_pest: string;
  treatment_category: 'fungicide' | 'insecticide' | 'bactericide' | 'biological' | 'cultural' | 'organic';
  active_ingredient?: string;
  approved_product_name?: string;
  dosage_guidance?: string;
  non_chemical_control: string;
  prevention_practices: string;
  source_org: string;
  source_url?: string;
  reference_citation: string;
  jurisdiction: string;
  approved_label_restrictions?: string;
  safety_precautions: string;
  harvest_waiting_period_days: number;
  verification_date: string;
}

export interface AlternativeDiagnosis {
  class_name: string;
  crop: string;
  crop_ta: string;
  disease: string;
  disease_ta: string;
  disease_type: string;
  confidence_pct: number;
  is_healthy: boolean;
}

export interface ActionPlan {
  urgency: string;
  urgency_ta: string;
  step_1_immediate: string;
  step_1_immediate_ta: string;
  step_2_biological_cultural: string;
  step_2_biological_cultural_ta: string;
  step_3_chemical_application: string;
  step_3_chemical_application_ta: string;
  step_4_monitoring: string;
  step_4_monitoring_ta: string;
  critical_donots: string[];
  critical_donots_ta: string[];
}

export interface PredictionResult {
  success: boolean;
  analysis_id: string;
  timestamp: string;
  class_name: string;
  crop: string;
  crop_ta: string;
  disease: string;
  disease_ta: string;
  disease_type: string;
  severity: string;
  is_healthy: boolean;
  confidence_score: number;
  confidence_pct: number;
  confidence_level: 'High' | 'Moderate' | 'Low';
  confidence_interpretation: string;
  is_uncertain: boolean;
  model_version: string;
  model_weights_loaded: boolean;
  symptoms: string;
  symptoms_ta: string;
  causes: string;
  causes_ta: string;
  next_steps: string;
  next_steps_ta: string;
  prevention: string;
  prevention_ta: string;
  ipm: string;
  action_plan?: ActionPlan;
  alternatives: AlternativeDiagnosis[];
  verified_guidance: GuidanceItem[];
  has_verified_treatment: boolean;
  warning_notice?: string;
  image_preview?: string;
}

export interface AnalysisRecord {
  id: string;
  timestamp: string;
  crop_name: string;
  crop_name_ta?: string;
  disease_name: string;
  disease_name_ta?: string;
  disease_type: string;
  confidence: number;
  is_healthy: boolean;
  is_uncertain: boolean;
  growth_stage?: string;
  district?: string;
  image_data_url?: string;
  symptoms_summary?: string;
  alternatives: AlternativeDiagnosis[];
  guidance: GuidanceItem[];
  feedback_status?: string;
  notes?: string;
}

export interface AnalyticsResponse {
  total_analyses: number;
  healthy_count: number;
  diseased_count: number;
  uncertain_count: number;
  crop_distribution: { crop: string; count: number }[];
  disease_type_distribution: { type: string; count: number }[];
  recent_history: {
    id: string;
    timestamp: string;
    crop_name: string;
    disease_name: string;
    confidence: number;
    is_healthy: number;
    is_uncertain: number;
    feedback_status?: string;
  }[];
}

export interface AdvisoryContact {
  id: number;
  organization: string;
  service_type: string;
  phone?: string;
  email?: string;
  website?: string;
  state_region?: string;
  notes?: string;
}
