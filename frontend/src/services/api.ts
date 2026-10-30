import {
  Crop,
  PredictionResult,
  GuidanceItem,
  AnalysisRecord,
  AnalyticsResponse,
  AdvisoryContact
} from '../types';

const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000').replace(/\/+$/, '');

export async function checkBackendHealth(): Promise<{ status: string; model_loaded: boolean }> {
  const res = await fetch(`${API_BASE_URL}/api/health`);
  if (!res.ok) throw new Error('Health check failed');
  return res.json();
}

export async function fetchCrops(): Promise<Crop[]> {
  const res = await fetch(`${API_BASE_URL}/api/crops`);
  if (!res.ok) throw new Error('Failed to load crops');
  return res.json();
}

export async function fetchDiseases(): Promise<any[]> {
  const res = await fetch(`${API_BASE_URL}/api/diseases`);
  if (!res.ok) throw new Error('Failed to load diseases');
  return res.json();
}

export async function fetchAdvisoryContacts(): Promise<AdvisoryContact[]> {
  const res = await fetch(`${API_BASE_URL}/api/advisory-contacts`);
  if (!res.ok) throw new Error('Failed to load advisory contacts');
  return res.json();
}

export async function fetchRecommendations(crop?: string, category?: string, search?: string): Promise<GuidanceItem[]> {
  const params = new URLSearchParams();
  if (crop && crop !== 'all') params.append('crop', crop);
  if (category && category !== 'all') params.append('category', category);
  if (search && search.trim()) params.append('search', search.trim());

  const res = await fetch(`${API_BASE_URL}/api/recommendations?${params.toString()}`);
  if (!res.ok) throw new Error('Failed to fetch recommendations');
  return res.json();
}

export async function analyzeCropImage(
  file: File,
  cropHint: string = 'auto',
  district?: string,
  growthStage?: string,
  symptomsNotes?: string
): Promise<PredictionResult> {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('crop_hint', cropHint);
  if (district) formData.append('district', district);
  if (growthStage) formData.append('growth_stage', growthStage);
  if (symptomsNotes) formData.append('symptoms_notes', symptomsNotes);

  const res = await fetch(`${API_BASE_URL}/api/predict`, {
    method: 'POST',
    body: formData
  });

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({ detail: 'Analysis failed' }));
    throw new Error(errorData.detail || 'Prediction failed');
  }

  return res.json();
}

export async function fetchHistory(crop?: string, statusFilter?: string): Promise<AnalysisRecord[]> {
  const params = new URLSearchParams();
  if (crop && crop !== 'all') params.append('crop', crop);
  if (statusFilter && statusFilter !== 'all') params.append('status_filter', statusFilter);

  const res = await fetch(`${API_BASE_URL}/api/history?${params.toString()}`);
  if (!res.ok) throw new Error('Failed to fetch analysis history');
  return res.json();
}

export async function fetchAnalysisRecord(id: string): Promise<AnalysisRecord> {
  const res = await fetch(`${API_BASE_URL}/api/history/${id}`);
  if (!res.ok) throw new Error('Failed to fetch analysis record');
  return res.json();
}

export async function deleteAnalysisRecord(id: string): Promise<void> {
  const res = await fetch(`${API_BASE_URL}/api/history/${id}`, {
    method: 'DELETE'
  });
  if (!res.ok) throw new Error('Failed to delete analysis record');
}

export async function submitFeedback(payload: {
  analysis_id: string;
  feedback_type: string;
  comment?: string;
  crop_name?: string;
  predicted_disease?: string;
}): Promise<void> {
  const res = await fetch(`${API_BASE_URL}/api/feedback`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  if (!res.ok) throw new Error('Failed to submit feedback');
}

export async function fetchAnalytics(): Promise<AnalyticsResponse> {
  const res = await fetch(`${API_BASE_URL}/api/analytics`);
  if (!res.ok) throw new Error('Failed to fetch analytics');
  return res.json();
}

export function getPdfDownloadUrl(analysisId: string): string {
  return `${API_BASE_URL}/api/history/${analysisId}/pdf`;
}
