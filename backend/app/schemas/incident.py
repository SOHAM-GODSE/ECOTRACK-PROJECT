from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Any


class IncidentResponse(BaseModel):
    id: int
    organization_id: int
    title: str
    description: Optional[str] = None
    incident_type: str
    severity: str
    state: str
    assigned_to_user_id: Optional[int] = None
    detected_at: datetime
    acknowledged_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    impact_verified_at: Optional[datetime] = None
    ai_evidence: Optional[Any] = None
    ai_recommendations: Optional[Any] = None
    before_metrics: Optional[Any] = None
    after_metrics: Optional[Any] = None
    estimated_impact: Optional[str] = None
    verified_impact: Optional[str] = None
    is_simulated: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class IncidentTransition(BaseModel):
    new_state: str
    description: str
    after_metrics: Optional[dict] = None


class EvidenceCreate(BaseModel):
    title: str
    description: Optional[str] = None
    evidence_type: str = "note"
    data: Optional[dict] = None


class EvidenceResponse(BaseModel):
    id: int
    incident_id: int
    evidence_type: str
    title: str
    description: Optional[str] = None
    data: Optional[Any] = None
    created_at: datetime

    class Config:
        from_attributes = True
