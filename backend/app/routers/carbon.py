from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from app.database import get_db
from app.models.carbon import CarbonCalculation, EmissionFactor
from app.models.organization import OrganizationMembership
from app.models.user import User
from app.services.auth import get_current_user
from app.services.carbon_engine import seed_emission_factors

router = APIRouter(prefix="/carbon", tags=["Carbon Footprint"])


@router.get("/factors")
def get_factors(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    seed_emission_factors(db)
    factors = db.query(EmissionFactor).all()
    return [
        {
            "id": f.id, "name": f.name, "category": f.category, "activity": f.activity,
            "factor_value": f.factor_value, "unit_numerator": f.unit_numerator,
            "unit_denominator": f.unit_denominator, "region": f.region,
            "source": f.source, "source_url": f.source_url, "notes": f.notes
        } for f in factors
    ]


@router.get("/calculations")
def list_calculations(
    org_id: int = Query(...),
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    calcs = db.query(CarbonCalculation).filter(CarbonCalculation.organization_id == org_id).order_by(desc(CarbonCalculation.calculated_at)).limit(limit).all()
    return [
        {
            "id": c.id, "category": c.category, "activity": c.activity,
            "activity_value": c.activity_value, "activity_unit": c.activity_unit,
            "emission_factor_value": c.emission_factor_value, "co2e_kg": c.co2e_kg,
            "period_start": c.period_start.isoformat() if c.period_start else None,
            "period_end": c.period_end.isoformat() if c.period_end else None,
            "calculated_at": c.calculated_at.isoformat(), "notes": c.notes
        } for c in calcs
    ]


@router.get("/summary")
def get_summary(org_id: int = Query(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    calcs = db.query(CarbonCalculation).filter(CarbonCalculation.organization_id == org_id).all()
    total = sum(c.co2e_kg for c in calcs)
    by_category = {}
    for c in calcs:
        by_category[c.category] = by_category.get(c.category, 0) + c.co2e_kg
    return {"total_co2e_kg": round(total, 3), "by_category": {k: round(v, 3) for k, v in by_category.items()}, "calculation_count": len(calcs)}
