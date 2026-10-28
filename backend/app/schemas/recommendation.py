from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Any


class RecommendationResponse(BaseModel):
    id: int
    organization_id: int
    incident_id: Optional[int] = None
    title: str
    description: str
    category: str
    status: str
    priority_score: float
    estimated_savings_kwh: Optional[float] = None
    estimated_savings_liters: Optional[float] = None
    estimated_savings_inr: Optional[float] = None
    estimated_co2_reduction_kg: Optional[float] = None
    implementation_effort: str
    implementation_cost: str
    evidence_summary: Optional[str] = None
    how_to_verify: Optional[str] = None
    actual_savings: Optional[Any] = None
    accepted_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class StatusUpdate(BaseModel):
    status: str
