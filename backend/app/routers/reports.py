from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional
import csv, io
from app.database import get_db
from app.models.water import WaterReading, WaterMeter
from app.models.electricity import ElectricityReading, ElectricityMeter
from app.models.incident import Incident
from app.models.recommendation import Recommendation
from app.models.user import User
from app.services.auth import get_current_user

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("/water/csv")
def export_water_csv(
    org_id: int = Query(...),
    meter_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Date", "Meter", "Reading", "Consumption (L)", "Anomaly", "Quality", "Source"])
    
    meters = db.query(WaterMeter).filter(WaterMeter.organization_id == org_id)
    if meter_id:
        meters = meters.filter(WaterMeter.id == meter_id)
    
    for meter in meters.all():
        readings = db.query(WaterReading).filter(WaterReading.meter_id == meter.id).order_by(WaterReading.recorded_at).all()
        for r in readings:
            writer.writerow([r.recorded_at.isoformat(), meter.name, r.reading_value,
                            r.consumption or "", r.is_anomaly, r.quality_flag, r.source])
    
    return Response(content=output.getvalue(), media_type="text/csv",
                   headers={"Content-Disposition": "attachment; filename=water_report.csv"})


@router.get("/electricity/csv")
def export_electricity_csv(
    org_id: int = Query(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Date", "Meter", "Reading (kWh)", "Consumption (kWh)", "Cost (INR)", "CO2e (kg)", "Anomaly", "Source"])
    
    for meter in db.query(ElectricityMeter).filter(ElectricityMeter.organization_id == org_id).all():
        for r in db.query(ElectricityReading).filter(ElectricityReading.meter_id == meter.id).order_by(ElectricityReading.recorded_at).all():
            writer.writerow([r.recorded_at.isoformat(), meter.name, r.reading_value,
                            r.consumption or "", r.cost_estimate or "", r.carbon_kg or "",
                            r.is_anomaly, r.source])
    
    return Response(content=output.getvalue(), media_type="text/csv",
                   headers={"Content-Disposition": "attachment; filename=electricity_report.csv"})


@router.get("/incidents/csv")
def export_incidents_csv(org_id: int = Query(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Title", "Type", "Severity", "State", "Detected", "Resolved", "Simulated"])
    for i in db.query(Incident).filter(Incident.organization_id == org_id).all():
        inc_type = i.incident_type.value if hasattr(i.incident_type, "value") else str(i.incident_type)
        sev = i.severity.value if hasattr(i.severity, "value") else str(i.severity)
        st = i.state.value if hasattr(i.state, "value") else str(i.state)
        writer.writerow([i.id, i.title, inc_type, sev, st,
                        i.detected_at.isoformat(), i.resolved_at.isoformat() if i.resolved_at else "", i.is_simulated])
    return Response(content=output.getvalue(), media_type="text/csv",
                   headers={"Content-Disposition": "attachment; filename=incidents_report.csv"})
