from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class ElectricityMeterCreate(BaseModel):
    name: str
    meter_id: str
    location: Optional[str] = None
    unit: str = "kWh"
    meter_type: str = "standard"
    notes: Optional[str] = None


class ElectricityMeterResponse(BaseModel):
    id: int
    organization_id: int
    name: str
    meter_id: str
    location: Optional[str] = None
    unit: str
    status: str
    meter_type: str
    notes: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ElectricityReadingCreate(BaseModel):
    reading_value: float = Field(gt=0)
    recorded_at: datetime
    notes: Optional[str] = None
    source: str = "manual"


class ElectricityReadingResponse(BaseModel):
    id: int
    meter_id: int
    reading_value: float
    unit: str
    source: str
    recorded_at: datetime
    consumption: Optional[float] = None
    cost_estimate: Optional[float] = None
    carbon_kg: Optional[float] = None
    is_anomaly: bool
    anomaly_score: Optional[float] = None
    notes: Optional[str] = None
    quality_flag: str
    created_at: datetime

    class Config:
        from_attributes = True
