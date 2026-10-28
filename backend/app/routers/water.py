from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime
from typing import Optional
from app.database import get_db
from app.models.water import WaterMeter, WaterReading
from app.models.organization import OrganizationMembership
from app.models.user import User
from app.schemas.water import WaterMeterCreate, WaterMeterResponse, WaterReadingCreate, WaterReadingResponse
from app.services.auth import get_current_user
from app.services.anomaly import combined_anomaly_detection
from app.services.incident_agent import create_incident_from_anomaly
from app.utils.unit_conversion import normalize_water_consumption

router = APIRouter(prefix="/water", tags=["Water Intelligence"])


def check_org_access(org_id: int, user: User, db: Session):
    membership = db.query(OrganizationMembership).filter(
        OrganizationMembership.organization_id == org_id,
        OrganizationMembership.user_id == user.id,
        OrganizationMembership.is_active == True
    ).first()
    if not membership:
        raise HTTPException(403, "Not a member of this organization")
    return membership


@router.get("/meters", response_model=list[WaterMeterResponse])
def list_meters(org_id: int = Query(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    check_org_access(org_id, current_user, db)
    meters = db.query(WaterMeter).filter(WaterMeter.organization_id == org_id).all()
    return [WaterMeterResponse.model_validate(m) for m in meters]


@router.post("/meters", response_model=WaterMeterResponse, status_code=201)
def create_meter(org_id: int = Query(...), payload: WaterMeterCreate = ..., db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    check_org_access(org_id, current_user, db)
    if db.query(WaterMeter).filter(WaterMeter.meter_id == payload.meter_id).first():
        raise HTTPException(400, "Meter ID already exists")
    meter = WaterMeter(organization_id=org_id, **payload.model_dump())
    db.add(meter)
    db.commit()
    db.refresh(meter)
    return WaterMeterResponse.model_validate(meter)


@router.get("/meters/{meter_id}/readings", response_model=list[WaterReadingResponse])
def get_readings(meter_id: int, limit: int = 90, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    meter = db.query(WaterMeter).filter(WaterMeter.id == meter_id).first()
    if not meter:
        raise HTTPException(404, "Meter not found")
    check_org_access(meter.organization_id, current_user, db)
    readings = db.query(WaterReading).filter(WaterReading.meter_id == meter_id).order_by(desc(WaterReading.recorded_at)).limit(limit).all()
    return [WaterReadingResponse.model_validate(r) for r in readings]


@router.post("/meters/{meter_id}/readings", response_model=WaterReadingResponse, status_code=201)
def add_reading(meter_id: int, payload: WaterReadingCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    meter = db.query(WaterMeter).filter(WaterMeter.id == meter_id).first()
    if not meter:
        raise HTTPException(404, "Meter not found")
    check_org_access(meter.organization_id, current_user, db)
    
    # Get previous reading for consumption calculation
    prev_reading = db.query(WaterReading).filter(
        WaterReading.meter_id == meter_id
    ).order_by(desc(WaterReading.recorded_at)).first()
    
    consumption = None
    quality_flag = "ok"
    
    if prev_reading and meter.is_cumulative:
        if payload.reading_value < prev_reading.reading_value:
            quality_flag = "suspect"  # possible meter reset
        else:
            consumption = normalize_water_consumption(
                payload.reading_value, prev_reading.reading_value, meter.unit
            )
    
    # Anomaly detection on consumption
    is_anomaly = False
    anomaly_score = None
    
    if consumption is not None:
        past_consumptions = []
        past_readings = db.query(WaterReading).filter(
            WaterReading.meter_id == meter_id,
            WaterReading.consumption != None
        ).order_by(desc(WaterReading.recorded_at)).limit(30).all()
        past_consumptions = [r.consumption for r in past_readings if r.consumption]
        
        if len(past_consumptions) >= 7:
            anomaly_result = combined_anomaly_detection(past_consumptions, consumption)
            is_anomaly = anomaly_result["is_anomaly"]
            anomaly_score = anomaly_result.get("anomaly_score")
            
            # Auto-create incident if anomaly detected
            if is_anomaly:
                mean_val = sum(past_consumptions) / len(past_consumptions)
                create_incident_from_anomaly(
                    db, meter.organization_id, "water", meter.id, meter.name,
                    anomaly_result, consumption, mean_val, meter.unit, current_user.id
                )
    
    reading = WaterReading(
        meter_id=meter_id,
        reading_value=payload.reading_value,
        unit=meter.unit,
        source=payload.source,
        recorded_at=payload.recorded_at,
        entered_by_user_id=current_user.id,
        consumption=consumption,
        is_anomaly=is_anomaly,
        anomaly_score=anomaly_score,
        notes=payload.notes,
        quality_flag=quality_flag
    )
    db.add(reading)
    db.commit()
    db.refresh(reading)
    return WaterReadingResponse.model_validate(reading)
