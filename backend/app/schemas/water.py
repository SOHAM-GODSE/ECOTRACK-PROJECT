from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class WaterMeterCreate(BaseModel):
    name: str
    meter_id: str
    location: Optional[str] = None
    unit: str = "liters"
    is_cumulative: bool = True
    notes: Optional[str] = None


class WaterMeterResponse(BaseModel):
    id: int
    organization_id: int
    name: str
    meter_id: str
    location: Optional[str] = None
    unit: str
    status: str
    is_cumulative: bool
    notes: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class WaterReadingCreate(BaseModel):
    reading_value: float = Field(gt=0)
    recorded_at: datetime
    notes: Optional[str] = None
    source: str = "manual"


class WaterReadingResponse(BaseModel):
    id: int
    meter_id: int
    reading_value: float
    unit: str
    source: str
    recorded_at: datetime
    consumption: Optional[float] = None
    is_anomaly: bool
    anomaly_score: Optional[float] = None
    notes: Optional[str] = None
    quality_flag: str
    created_at: datetime

    class Config:
        from_attributes = True
