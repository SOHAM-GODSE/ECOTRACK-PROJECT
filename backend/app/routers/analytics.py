from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.database import get_db
from app.models.water import WaterReading, WaterMeter
from app.models.electricity import ElectricityReading, ElectricityMeter
from app.models.incident import Incident
from app.models.user import User
from app.services.auth import get_current_user
from app.services.forecasting import linear_forecast, compute_baseline_stats
from datetime import datetime

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/anomalies")
def get_anomalies(org_id: int = Query(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Water anomalies
    water_meters = db.query(WaterMeter).filter(WaterMeter.organization_id == org_id).all()
    water_anomalies = []
    for meter in water_meters:
        readings = db.query(WaterReading).filter(
            WaterReading.meter_id == meter.id,
            WaterReading.is_anomaly == True
        ).order_by(desc(WaterReading.recorded_at)).limit(10).all()
        for r in readings:
            water_anomalies.append({
                "type": "water", "meter_name": meter.name,
                "value": r.consumption, "unit": meter.unit,
                "anomaly_score": r.anomaly_score,
                "recorded_at": r.recorded_at.isoformat()
            })
    
    # Electricity anomalies
    elec_meters = db.query(ElectricityMeter).filter(ElectricityMeter.organization_id == org_id).all()
    elec_anomalies = []
    for meter in elec_meters:
        readings = db.query(ElectricityReading).filter(
            ElectricityReading.meter_id == meter.id,
            ElectricityReading.is_anomaly == True
        ).order_by(desc(ElectricityReading.recorded_at)).limit(10).all()
        for r in readings:
            elec_anomalies.append({
                "type": "electricity", "meter_name": meter.name,
                "value": r.consumption, "unit": "kWh",
                "anomaly_score": r.anomaly_score,
                "recorded_at": r.recorded_at.isoformat()
            })
    
    return {"water": water_anomalies, "electricity": elec_anomalies, "total": len(water_anomalies) + len(elec_anomalies)}


@router.get("/forecast/{meter_type}/{meter_id}")
def get_forecast(meter_type: str, meter_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if meter_type == "water":
        readings = db.query(WaterReading).filter(
            WaterReading.meter_id == meter_id, WaterReading.consumption != None
        ).order_by(WaterReading.recorded_at).all()
        values = [r.consumption for r in readings if r.consumption]
        dates = [r.recorded_at for r in readings if r.consumption]
    elif meter_type == "electricity":
        readings = db.query(ElectricityReading).filter(
            ElectricityReading.meter_id == meter_id, ElectricityReading.consumption != None
        ).order_by(ElectricityReading.recorded_at).all()
        values = [r.consumption for r in readings if r.consumption]
        dates = [r.recorded_at for r in readings if r.consumption]
    else:
        return {"error": "meter_type must be 'water' or 'electricity'"}
    
    baseline = compute_baseline_stats(values)
    forecast = linear_forecast(values, dates, 7)
    
    return {
        "meter_type": meter_type,
        "meter_id": meter_id,
        "n_historical": len(values),
        "baseline": baseline,
        "forecast": forecast
    }
