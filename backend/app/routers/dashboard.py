from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from datetime import datetime, timedelta
from app.database import get_db
from app.models.water import WaterReading, WaterMeter
from app.models.electricity import ElectricityReading, ElectricityMeter
from app.models.incident import Incident, IncidentState
from app.models.recommendation import Recommendation, RecommendationStatus
from app.models.carbon import CarbonCalculation
from app.models.notification import Notification
from app.models.user import User
from app.schemas.incident import IncidentResponse
from app.schemas.recommendation import RecommendationResponse
from app.services.auth import get_current_user

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/summary")
def get_summary(org_id: int = Query(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    today = datetime.utcnow().date()
    today_start = datetime.combine(today, datetime.min.time())
    
    # Water today
    water_meters = db.query(WaterMeter).filter(WaterMeter.organization_id == org_id).all()
    water_today = 0.0
    water_chart_data = []
    
    for meter in water_meters:
        readings = db.query(WaterReading).filter(
            WaterReading.meter_id == meter.id,
            WaterReading.recorded_at >= today_start,
            WaterReading.consumption != None
        ).all()
        water_today += sum(r.consumption for r in readings if r.consumption)
    
    # Water chart: last 30 days
    for i in range(29, -1, -1):
        day = today - timedelta(days=i)
        day_start = datetime.combine(day, datetime.min.time())
        day_end = datetime.combine(day, datetime.max.time())
        total = 0.0
        for meter in water_meters:
            readings = db.query(WaterReading).filter(
                WaterReading.meter_id == meter.id,
                WaterReading.recorded_at.between(day_start, day_end),
                WaterReading.consumption != None
            ).all()
            total += sum(r.consumption for r in readings if r.consumption)
        water_chart_data.append({"date": day.isoformat(), "consumption": round(total, 2)})
    
    # Electricity today
    elec_meters = db.query(ElectricityMeter).filter(ElectricityMeter.organization_id == org_id).all()
    elec_today = 0.0
    elec_chart_data = []
    
    for meter in elec_meters:
        readings = db.query(ElectricityReading).filter(
            ElectricityReading.meter_id == meter.id,
            ElectricityReading.recorded_at >= today_start,
            ElectricityReading.consumption != None
        ).all()
        elec_today += sum(r.consumption for r in readings if r.consumption)
    
    for i in range(29, -1, -1):
        day = today - timedelta(days=i)
        day_start = datetime.combine(day, datetime.min.time())
        day_end = datetime.combine(day, datetime.max.time())
        total = 0.0
        for meter in elec_meters:
            readings = db.query(ElectricityReading).filter(
                ElectricityReading.meter_id == meter.id,
                ElectricityReading.recorded_at.between(day_start, day_end),
                ElectricityReading.consumption != None
            ).all()
            total += sum(r.consumption for r in readings if r.consumption)
        elec_chart_data.append({"date": day.isoformat(), "consumption": round(total, 4)})
    
    # Active incidents
    active_states = [IncidentState.NEW, IncidentState.ACKNOWLEDGED, IncidentState.INVESTIGATING, IncidentState.ACTION_REQUIRED]
    active_incidents = db.query(Incident).filter(
        Incident.organization_id == org_id,
        Incident.state.in_(active_states)
    ).order_by(desc(Incident.created_at)).limit(5).all()
    
    # Carbon today
    carbon_calcs = db.query(CarbonCalculation).filter(
        CarbonCalculation.organization_id == org_id,
        CarbonCalculation.calculated_at >= today_start
    ).all()
    carbon_today = sum(c.co2e_kg for c in carbon_calcs)
    
    # Pending recommendations
    pending_recs = db.query(Recommendation).filter(
        Recommendation.organization_id == org_id,
        Recommendation.status == RecommendationStatus.PENDING
    ).order_by(desc(Recommendation.priority_score)).limit(3).all()
    
    return {
        "water_today_liters": round(water_today, 2),
        "electricity_today_kwh": round(elec_today, 4),
        "active_incidents": len(active_incidents),
        "carbon_today_kg": round(carbon_today, 4),
        "water_trend_pct": 0,
        "electricity_trend_pct": 0,
        "pending_recommendations": db.query(Recommendation).filter(
            Recommendation.organization_id == org_id,
            Recommendation.status == RecommendationStatus.PENDING
        ).count(),
        "water_chart": water_chart_data,
        "electricity_chart": elec_chart_data,
        "recent_incidents": [IncidentResponse.model_validate(i).model_dump() for i in active_incidents],
        "top_recommendations": [RecommendationResponse.model_validate(r).model_dump() for r in pending_recs]
    }
