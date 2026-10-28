"""Deterministic carbon footprint calculation engine.

Emissions = Activity data × Applicable emission factor

India electricity factor (CEA 2022-23): 0.716 kg CO2e per kWh
Source: Central Electricity Authority CO2 Baseline Database for Indian Power Sector, 2022-23
"""
from datetime import datetime, date
from sqlalchemy.orm import Session
from app.models.carbon import EmissionFactor, CarbonCalculation

# Default India emission factors (used as fallback if DB empty)
DEFAULT_FACTORS = {
    "grid_electricity_india": {
        "factor": 0.716,
        "unit_from": "kWh",
        "unit_to": "kg_co2e",
        "source": "CEA CO2 Baseline Database for Indian Power Sector, 2022-23",
        "source_url": "https://cea.nic.in/wp-content/uploads/baseline/2024/02/CO2_Baseline_Database_for_the_Indian_Power_Sector_User_Guide_Ver_18.pdf",
        "region": "India",
        "notes": "National average grid emission factor. Actual factor varies by state and year."
    },
    "diesel_transport": {
        "factor": 2.68,
        "unit_from": "liter",
        "unit_to": "kg_co2e",
        "source": "IPCC 2006 Guidelines",
        "source_url": "https://www.ipcc-nggip.iges.or.jp/public/2006gl/",
        "region": "Global",
    },
    "petrol_transport": {
        "factor": 2.31,
        "unit_from": "liter",
        "unit_to": "kg_co2e",
        "source": "IPCC 2006 Guidelines",
        "source_url": "https://www.ipcc-nggip.iges.or.jp/public/2006gl/",
        "region": "Global",
    },
    "landfill_waste": {
        "factor": 0.5,
        "unit_from": "kg",
        "unit_to": "kg_co2e",
        "source": "IPCC 2006 Waste Guidelines (estimated)",
        "source_url": "https://www.ipcc-nggip.iges.or.jp/public/2006gl/",
        "region": "Global",
        "notes": "Approximate. Actual factor depends on waste composition and landfill type."
    },
}


def get_emission_factor(db: Session, activity: str) -> dict:
    """Get emission factor from DB, fall back to defaults."""
    factor_row = db.query(EmissionFactor).filter(
        EmissionFactor.activity == activity,
        EmissionFactor.effective_to == None
    ).first()
    
    if factor_row:
        return {
            "factor": factor_row.factor_value,
            "unit_from": factor_row.unit_denominator,
            "unit_to": factor_row.unit_numerator,
            "source": factor_row.source,
            "source_url": factor_row.source_url,
            "region": factor_row.region,
            "notes": factor_row.notes,
            "factor_id": factor_row.id
        }
    
    default = DEFAULT_FACTORS.get(activity)
    if default:
        return {**default, "factor_id": None}
    
    raise ValueError(f"No emission factor found for activity: {activity}")


def calculate_electricity_emissions(
    db: Session,
    org_id: int,
    kwh: float,
    period_start: datetime | None = None,
    period_end: datetime | None = None,
    source_reference: str | None = None
) -> CarbonCalculation:
    """Calculate CO2e from electricity consumption. Returns saved CarbonCalculation."""
    if kwh <= 0:
        raise ValueError("kWh must be positive")
    
    factor_data = get_emission_factor(db, "grid_electricity_india")
    co2e_kg = round(kwh * factor_data["factor"], 4)
    
    calc = CarbonCalculation(
        organization_id=org_id,
        category="electricity",
        activity="grid_electricity_india",
        activity_value=kwh,
        activity_unit="kWh",
        emission_factor_id=factor_data.get("factor_id"),
        emission_factor_value=factor_data["factor"],
        co2e_kg=co2e_kg,
        period_start=period_start,
        period_end=period_end,
        notes=f"Emission factor source: {factor_data.get('source', 'N/A')}. "
              f"Note: {factor_data.get('notes', '')}",
        calculated_at=datetime.utcnow(),
        source_reference=source_reference
    )
    db.add(calc)
    db.commit()
    db.refresh(calc)
    return calc


def seed_emission_factors(db: Session) -> None:
    """Seed default emission factors if DB is empty."""
    if db.query(EmissionFactor).count() > 0:
        return
    
    for activity, data in DEFAULT_FACTORS.items():
        factor = EmissionFactor(
            name=activity.replace("_", " ").title(),
            category="electricity" if "electricity" in activity else "transport" if "transport" in activity else "waste",
            activity=activity,
            factor_value=data["factor"],
            unit_numerator=data["unit_to"],
            unit_denominator=data["unit_from"],
            region=data.get("region", "Global"),
            source=data.get("source"),
            source_url=data.get("source_url"),
            notes=data.get("notes"),
            effective_from=date(2023, 1, 1)
        )
        db.add(factor)
    db.commit()
