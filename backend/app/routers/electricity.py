from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime
from app.database import get_db
from app.models.electricity import ElectricityMeter, ElectricityReading
from app.models.organization import OrganizationMembership
from app.models.user import User
from app.schemas.electricity import ElectricityMeterCreate, ElectricityMeterResponse, ElectricityReadingCreate, ElectricityReadingResponse
from app.services.auth import get_current_user
from app.services.anomaly import combined_anomaly_detection
from app.services.incident_agent import create_incident_from_anomaly
from app.services.carbon_engine import calculate_electricity_emissions

ELECTRICITY_TARIFF_INR_PER_KWH = 7.0  # Default tariff for India

router = APIRouter(prefix="/electricity", tags=["Electricity Intelligence"])


def check_org_access(org_id: int, user: User, db: Session):
    m = db.query(OrganizationMembership).filter(
        OrganizationMembership.organization_id == org_id,
        OrganizationMembership.user_id == user.id,
        OrganizationMembership.is_active == True
    ).first()
    if not m:
        raise HTTPException(403, "Not a member of this organization")
    return m


@router.get("/meters", response_model=list[ElectricityMeterResponse])
def list_meters(org_id: int = Query(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    check_org_access(org_id, current_user, db)
    meters = db.query(ElectricityMeter).filter(ElectricityMeter.organization_id == org_id).all()
    return [ElectricityMeterResponse.model_validate(m) for m in meters]


@router.post("/meters", response_model=ElectricityMeterResponse, status_code=201)
def create_meter(org_id: int = Query(...), payload: ElectricityMeterCreate = ..., db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    check_org_access(org_id, current_user, db)
    if db.query(ElectricityMeter).filter(ElectricityMeter.meter_id == payload.meter_id).first():
        raise HTTPException(400, "Meter ID already exists")
    meter = ElectricityMeter(organization_id=org_id, **payload.model_dump())
    db.add(meter)
    db.commit()
    db.refresh(meter)
    return ElectricityMeterResponse.model_validate(meter)


@router.get("/meters/{meter_id}/readings", response_model=list[ElectricityReadingResponse])
def get_readings(meter_id: int, limit: int = 90, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    meter = db.query(ElectricityMeter).filter(ElectricityMeter.id == meter_id).first()
    if not meter:
        raise HTTPException(404, "Meter not found")
    check_org_access(meter.organization_id, current_user, db)
    readings = db.query(ElectricityReading).filter(ElectricityReading.meter_id == meter_id).order_by(desc(ElectricityReading.recorded_at)).limit(limit).all()
    return [ElectricityReadingResponse.model_validate(r) for r in readings]


@router.post("/meters/{meter_id}/readings", response_model=ElectricityReadingResponse, status_code=201)
def add_reading(meter_id: int, payload: ElectricityReadingCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    meter = db.query(ElectricityMeter).filter(ElectricityMeter.id == meter_id).first()
    if not meter:
        raise HTTPException(404, "Meter not found")
    check_org_access(meter.organization_id, current_user, db)
    
    prev = db.query(ElectricityReading).filter(
        ElectricityReading.meter_id == meter_id
    ).order_by(desc(ElectricityReading.recorded_at)).first()
    
    consumption = None
    quality_flag = "ok"
    if prev:
        if payload.reading_value < prev.reading_value:
            quality_flag = "suspect"
        else:
            consumption = round(payload.reading_value - prev.reading_value, 4)
    
    cost_estimate = round(consumption * ELECTRICITY_TARIFF_INR_PER_KWH, 2) if consumption else None
    carbon_kg = None
    
    # Carbon calculation
    if consumption and consumption > 0:
        try:
            carbon_calc = calculate_electricity_emissions(
                db, meter.organization_id, consumption,
                source_reference=f"electricity_reading:{meter_id}"
            )
            carbon_kg = carbon_calc.co2e_kg
        except Exception:
            carbon_kg = round(consumption * 0.716, 4)  # fallback
    
    # Anomaly detection
    is_anomaly = False
    anomaly_score = None
    
    if consumption is not None:
        past = db.query(ElectricityReading).filter(
            ElectricityReading.meter_id == meter_id,
            ElectricityReading.consumption != None
        ).order_by(desc(ElectricityReading.recorded_at)).limit(30).all()
        past_vals = [r.consumption for r in past if r.consumption]
        
        if len(past_vals) >= 7:
            ar = combined_anomaly_detection(past_vals, consumption)
            is_anomaly = ar["is_anomaly"]
            anomaly_score = ar.get("anomaly_score")
            if is_anomaly:
                mean_val = sum(past_vals) / len(past_vals)
                create_incident_from_anomaly(
                    db, meter.organization_id, "electricity", meter.id, meter.name,
                    ar, consumption, mean_val, "kWh", current_user.id
                )
    
    reading = ElectricityReading(
        meter_id=meter_id,
        reading_value=payload.reading_value,
        unit=meter.unit,
        source=payload.source,
        recorded_at=payload.recorded_at,
        entered_by_user_id=current_user.id,
        consumption=consumption,
        cost_estimate=cost_estimate,
        carbon_kg=carbon_kg,
        is_anomaly=is_anomaly,
        anomaly_score=anomaly_score,
        notes=payload.notes,
        quality_flag=quality_flag
    )
    db.add(reading)
    db.commit()
    db.refresh(reading)
    return ElectricityReadingResponse.model_validate(reading)
