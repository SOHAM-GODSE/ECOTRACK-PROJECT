export interface User {
  id: number;
  email: string;
  full_name: string;
  role: 'individual' | 'org_admin' | 'maintenance' | 'platform_admin';
  is_active: boolean;
  is_verified: boolean;
  phone?: string;
  avatar_url?: string;
  created_at: string;
}

export interface Organization {
  id: number;
  name: string;
  slug: string;
  org_type: string;
  description?: string;
  city?: string;
  state?: string;
  country: string;
  latitude?: number;
  longitude?: number;
  is_active: boolean;
  created_at: string;
}

export interface WaterMeter {
  id: number;
  organization_id: number;
  name: string;
  meter_id: string;
  location?: string;
  unit: string;
  status: string;
  is_cumulative: boolean;
  created_at: string;
}

export interface WaterReading {
  id: number;
  meter_id: number;
  reading_value: number;
  unit: string;
  source: string;
  recorded_at: string;
  consumption?: number;
  is_anomaly: boolean;
  anomaly_score?: number;
  notes?: string;
  quality_flag: string;
  created_at: string;
}

export interface ElectricityMeter {
  id: number;
  organization_id: number;
  name: string;
  meter_id: string;
  location?: string;
  unit: string;
  status: string;
  meter_type: string;
  created_at: string;
}

export interface ElectricityReading {
  id: number;
  meter_id: number;
  reading_value: number;
  unit: string;
  source: string;
  recorded_at: string;
  consumption?: number;
  cost_estimate?: number;
  carbon_kg?: number;
  is_anomaly: boolean;
  anomaly_score?: number;
  notes?: string;
  quality_flag: string;
  created_at: string;
}

export interface Incident {
  id: number;
  organization_id: number;
  title: string;
  description?: string;
  incident_type: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  state: 'new' | 'acknowledged' | 'investigating' | 'action_required' | 'resolved' | 'impact_verified' | 'reopened';
  assigned_to_user_id?: number;
  detected_at: string;
  acknowledged_at?: string;
  resolved_at?: string;
  impact_verified_at?: string;
  ai_evidence?: any;
  ai_recommendations?: any;
  before_metrics?: any;
  after_metrics?: any;
  estimated_impact?: string;
  verified_impact?: string;
  is_simulated: boolean;
  created_at: string;
  updated_at: string;
}

export interface Recommendation {
  id: number;
  organization_id: number;
  incident_id?: number;
  title: string;
  description: string;
  category: string;
  status: 'pending' | 'accepted' | 'rejected' | 'deferred' | 'completed';
  priority_score: number;
  estimated_savings_kwh?: number;
  estimated_savings_liters?: number;
  estimated_savings_inr?: number;
  estimated_co2_reduction_kg?: number;
  implementation_effort: string;
  implementation_cost: string;
  evidence_summary?: string;
  how_to_verify?: string;
  actual_savings?: any;
  accepted_at?: string;
  completed_at?: string;
  created_at: string;
}

export interface WasteClassification {
  id: number;
  category: string;
  confidence: number;
  all_predictions: Record<string, number>;
  disposal_guidance: string;
  model_used: string;
  is_fallback: boolean;
  note?: string;
}

export interface DashboardSummary {
  water_today_liters: number;
  electricity_today_kwh: number;
  active_incidents: number;
  carbon_today_kg: number;
  water_trend_pct: number;
  electricity_trend_pct: number;
  pending_recommendations: number;
  water_chart: Array<{date: string; consumption: number}>;
  electricity_chart: Array<{date: string; consumption: number}>;
  recent_incidents: Incident[];
  top_recommendations: Recommendation[];
}

export interface Notification {
  id: number;
  title: string;
  message: string;
  notification_type: string;
  is_read: boolean;
  action_url?: string;
  created_at: string;
}
