"""Seed script for EcoTrack AI demo environment."""
import sys
from pathlib import Path
from datetime import datetime, timedelta
import random

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from app.database import Base, engine, SessionLocal
from app.models.user import User, UserRole
from app.models.organization import Organization, OrganizationMembership, MemberRole
from app.models.carbon import EmissionFactor
from app.models.water import WaterMeter, WaterReading, ReadingSource, MeterStatus
from app.models.electricity import ElectricityMeter, ElectricityReading
from app.models.incident import Incident, IncidentState, IncidentSeverity, IncidentType
from app.models.recommendation import Recommendation, RecommendationStatus
from app.models.challenge import GreenChallenge, ChallengeStatus
from app.models.location import RecyclingLocation
from app.models.iot import IoTDevice
from app.services.auth import get_password_hash


def seed_data():
    db = SessionLocal()
    try:
        print("Ensuring database tables exist...")
        Base.metadata.create_all(bind=engine)

        # 1. Emission Factors
        if db.query(EmissionFactor).count() == 0:
            print("Seeding emission factors...")
            factors = [
                EmissionFactor(
                    name="India Grid Electricity Average",
                    category="electricity",
                    activity="grid_electricity_india",
                    factor_value=0.716,
                    unit_numerator="kg_co2e",
                    unit_denominator="kWh",
                    region="India",
                    source="CEA CO2 Baseline Database 2022-23"
                ),
                EmissionFactor(
                    name="Diesel Fuel Combustion",
                    category="transport",
                    activity="diesel_transport",
                    factor_value=2.68,
                    unit_numerator="kg_co2e",
                    unit_denominator="liter",
                    region="Global",
                    source="IPCC 2006 Guidelines"
                ),
                EmissionFactor(
                    name="Petrol Fuel Combustion",
                    category="transport",
                    activity="petrol_transport",
                    factor_value=2.31,
                    unit_numerator="kg_co2e",
                    unit_denominator="liter",
                    region="Global",
                    source="IPCC 2006 Guidelines"
                ),
                EmissionFactor(
                    name="Municipal Solid Waste to Landfill",
                    category="waste",
                    activity="landfill_waste",
                    factor_value=0.5,
                    unit_numerator="kg_co2e",
                    unit_denominator="kg",
                    region="Global",
                    source="IPCC 2006 Waste Guidelines"
                ),
            ]
            db.add_all(factors)
            db.commit()

        # 2. Demo User
        admin_user = db.query(User).filter(User.email == "admin@ecotrack.ai").first()
        if not admin_user:
            print("Creating demo admin user (admin@ecotrack.ai / ecotrack123)...")
            admin_user = User(
                email="admin@ecotrack.ai",
                full_name="Alex Rivera (Sustainability Lead)",
                hashed_password=get_password_hash("ecotrack123"),
                role=UserRole.ORG_ADMIN,
                is_active=True,
                is_verified=True,
                phone="+91 9876543210"
            )
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)

        # 3. Demo Organization
        org = db.query(Organization).filter(Organization.slug == "ecotech-campus").first()
        if not org:
            print("Creating demo organization 'EcoTech Smart Campus'...")
            org = Organization(
                name="EcoTech Smart Campus",
                slug="ecotech-campus",
                org_type="college",
                description="Innovation campus driving net-zero environmental initiatives and real-time monitoring.",
                city="Bengaluru",
                state="Karnataka",
                country="India",
                latitude=12.9716,
                longitude=77.5946,
                is_active=True
            )
            db.add(org)
            db.commit()
            db.refresh(org)

            # Membership
            membership = OrganizationMembership(
                organization_id=org.id,
                user_id=admin_user.id,
                role=MemberRole.ADMIN
            )
            db.add(membership)
            db.commit()

        # 4. Meters & Readings
        if db.query(WaterMeter).filter(WaterMeter.organization_id == org.id).count() == 0:
            print("Seeding water meters and 30-day historical readings...")
            wm1 = WaterMeter(organization_id=org.id, name="Academic Block Main Meter", meter_id="WM-ACAD-01", location="Building A, Basement", unit="liters", status=MeterStatus.ACTIVE, is_cumulative=True)
            wm2 = WaterMeter(organization_id=org.id, name="Hostel & Dining Hall Meter", meter_id="WM-HOST-02", location="Block H, Ground Floor", unit="liters", status=MeterStatus.ACTIVE, is_cumulative=True)
            db.add_all([wm1, wm2])
            db.commit()
            db.refresh(wm1)
            db.refresh(wm2)

            now = datetime.utcnow()
            for i in range(30, -1, -1):
                reading_date = now - timedelta(days=i)
                cons1 = round(random.uniform(1800, 2400), 1)
                db.add(WaterReading(
                    meter_id=wm1.id,
                    reading_value=50000 + (30 - i) * 2100,
                    consumption=cons1,
                    unit="liters",
                    source=ReadingSource.IOT,
                    recorded_at=reading_date,
                    is_anomaly=False
                ))
                is_leak = (i == 3)
                cons2 = round(random.uniform(7500, 8900) if is_leak else random.uniform(3200, 4100), 1)
                db.add(WaterReading(
                    meter_id=wm2.id,
                    reading_value=120000 + (30 - i) * 3600,
                    consumption=cons2,
                    unit="liters",
                    source=ReadingSource.IOT,
                    recorded_at=reading_date,
                    is_anomaly=is_leak,
                    anomaly_score=4.2 if is_leak else 0.1,
                    notes="Overnight surge detected by AI monitor" if is_leak else None
                ))
            db.commit()

        if db.query(ElectricityMeter).filter(ElectricityMeter.organization_id == org.id).count() == 0:
            print("Seeding electricity meters and 30-day historical readings...")
            em1 = ElectricityMeter(organization_id=org.id, name="Solar Inverter & Main Grid Inflow", meter_id="EM-GRID-01", location="Substation 1", unit="kWh", status="ACTIVE", meter_type="grid")
            em2 = ElectricityMeter(organization_id=org.id, name="Computing Lab & Data Center", meter_id="EM-LAB-02", location="Tech Block 2nd Floor", unit="kWh", status="ACTIVE", meter_type="sub")
            db.add_all([em1, em2])
            db.commit()
            db.refresh(em1)
            db.refresh(em2)

            now = datetime.utcnow()
            for i in range(30, -1, -1):
                reading_date = now - timedelta(days=i)
                cons_em1 = round(random.uniform(350, 490), 1)
                db.add(ElectricityReading(
                    meter_id=em1.id,
                    reading_value=25000 + (30 - i) * 420,
                    consumption=cons_em1,
                    unit="kWh",
                    source="iot",
                    recorded_at=reading_date,
                    is_anomaly=False
                ))
                cons_em2 = round(random.uniform(180, 260), 1)
                db.add(ElectricityReading(
                    meter_id=em2.id,
                    reading_value=15000 + (30 - i) * 220,
                    consumption=cons_em2,
                    unit="kWh",
                    source="iot",
                    recorded_at=reading_date,
                    is_anomaly=False
                ))
            db.commit()

        # 5. Incidents
        if db.query(Incident).filter(Incident.organization_id == org.id).count() == 0:
            print("Seeding sample AI incidents...")
            inc1 = Incident(
                organization_id=org.id,
                title="Continuous Underground Pipe Leak Suspected",
                incident_type=IncidentType.LEAK_SUSPECTED,
                severity=IncidentSeverity.CRITICAL,
                state=IncidentState.INVESTIGATING,
                description="Overnight baseline water draw spiked to 3.8x normal between 02:00 AM - 05:00 AM in Hostel Block H.",
                estimated_impact="185 L/hr loss (est. ₹14,500/mo waste)",
                ai_evidence={"overnight_draw_liters": 4200, "normal_baseline": 850, "z_score": 4.2},
                ai_recommendations={"action": "Isolate valve H-2 and inspect southern irrigation junction for pressure loss."}
            )
            inc2 = Incident(
                organization_id=org.id,
                title="HVAC Weekend Overconsumption Anomaly",
                incident_type=IncidentType.ELECTRICITY_ANOMALY,
                severity=IncidentSeverity.MEDIUM,
                state=IncidentState.RESOLVED,
                description="Air conditioning chillers remained at full cooling load through Sunday when campus was closed.",
                estimated_impact="42 kWh/hr unnecessary draw (₹5,800 total excess)",
                ai_evidence={"sunday_draw_kwh": 650, "expected_baseline": 110},
                ai_recommendations={"action": "Set automated thermostat setback timer to trigger off at Friday 20:00."}
            )
            db.add_all([inc1, inc2])
            db.commit()

        # 6. Recommendations
        if db.query(Recommendation).filter(Recommendation.organization_id == org.id).count() == 0:
            print("Seeding actionable recommendations...")
            recs = [
                Recommendation(
                    organization_id=org.id,
                    title="Install Smart Aerators in Academic Restrooms",
                    description="Retrofit 64 faucets with 1.5 LPM pressure-compensating aerators to cut flow rate by 55%.",
                    category="Water Conservation",
                    status=RecommendationStatus.PENDING,
                    priority_score=92.0,
                    estimated_savings_liters=45000.0,
                    estimated_savings_inr=18200.0,
                    estimated_co2_reduction_kg=120.0,
                    implementation_effort="low",
                    implementation_cost="low",
                    evidence_summary="Flow rate audit showed 3.8 GPM average across older brass fittings.",
                    how_to_verify="Measure 10-second volume output in sampled restrooms after installation."
                ),
                Recommendation(
                    organization_id=org.id,
                    title="Optimize Server Room AC Setpoint from 19°C to 23°C",
                    description="Modern ASHRAE TC9.9 guidelines permit data centers up to 27°C with no reliability impact.",
                    category="Energy Efficiency",
                    status=RecommendationStatus.ACCEPTED,
                    priority_score=87.0,
                    estimated_savings_kwh=1250.0,
                    estimated_savings_inr=11250.0,
                    estimated_co2_reduction_kg=895.0,
                    implementation_effort="low",
                    implementation_cost="low",
                    evidence_summary="Server intake ambient sensor averages 18.4°C, well below thermal thresholds.",
                    how_to_verify="Check EM-LAB-02 daily kWh reduction over 14 consecutive days."
                ),
                Recommendation(
                    organization_id=org.id,
                    title="Solar Rooftop Net-Metering Expansion",
                    description="Utilize 450 sq.m of unshaded library roof space for a 40kWp solar PV array.",
                    category="Renewable Energy",
                    status=RecommendationStatus.PENDING,
                    priority_score=81.0,
                    estimated_savings_kwh=4800.0,
                    estimated_savings_inr=43200.0,
                    estimated_co2_reduction_kg=3436.8,
                    implementation_effort="high",
                    implementation_cost="high",
                    evidence_summary="Pyranometer data shows 5.2 peak sun hours/day in Bengaluru region.",
                    how_to_verify="Bi-directional grid meter export logs."
                ),
            ]
            db.add_all(recs)
            db.commit()

        # 7. Green Challenges
        if db.query(GreenChallenge).count() == 0:
            print("Seeding green challenges...")
            chals = [
                GreenChallenge(
                    organization_id=org.id,
                    created_by_user_id=admin_user.id,
                    title="Zero Plastic November Challenge",
                    description="Bring your own reusable flask and container for 21 days straight. Log your daily single-use plastic avoided.",
                    category="Waste Reduction",
                    status=ChallengeStatus.ACTIVE,
                    start_date=datetime.utcnow() - timedelta(days=5),
                    end_date=datetime.utcnow() + timedelta(days=25),
                    target_metric="reusable_uses",
                    target_value=21.0,
                    scoring_method="participation"
                ),
                GreenChallenge(
                    organization_id=org.id,
                    created_by_user_id=admin_user.id,
                    title="Campus Stair-Climb & Energy Saver",
                    description="Skip the elevator for floors 1-3 to conserve building electricity and stay fit.",
                    category="Energy Conservation",
                    status=ChallengeStatus.ACTIVE,
                    start_date=datetime.utcnow() - timedelta(days=2),
                    end_date=datetime.utcnow() + timedelta(days=28),
                    target_metric="flights_climbed",
                    target_value=50.0,
                    scoring_method="participation"
                )
            ]
            db.add_all(chals)
            db.commit()

        # 8. Recycling Locations
        if db.query(RecyclingLocation).count() == 0:
            print("Seeding recycling locations...")
            locs = [
                RecyclingLocation(
                    name="Campus E-Waste & Battery Drop Box",
                    location_type="e_waste",
                    address="Student Union Center, Main Foyer",
                    city="Bengaluru",
                    latitude=12.9720,
                    longitude=77.5950,
                    accepts_categories={"categories": ["batteries", "laptops", "cables"]},
                    operating_hours="Mon-Sat: 08:00 - 20:00",
                    is_active=True
                ),
                RecyclingLocation(
                    name="Organic Composting Hub",
                    location_type="compost",
                    address="Behind Cafeteria 2, Garden Side",
                    city="Bengaluru",
                    latitude=12.9710,
                    longitude=77.5940,
                    accepts_categories={"categories": ["food_waste", "coffee_grounds", "yard_trimmings"]},
                    operating_hours="Daily: 06:00 - 18:00",
                    is_active=True
                ),
                RecyclingLocation(
                    name="Paper & Cardboard Baling Center",
                    location_type="paper",
                    address="Library Loading Dock B",
                    city="Bengaluru",
                    latitude=12.9715,
                    longitude=77.5960,
                    accepts_categories={"categories": ["paper", "cardboard", "magazines"]},
                    operating_hours="Mon-Fri: 09:00 - 17:00",
                    is_active=True
                ),
            ]
            db.add_all(locs)
            db.commit()

        # 9. IoT Devices
        if db.query(IoTDevice).filter(IoTDevice.organization_id == org.id).count() == 0:
            print("Seeding IoT devices...")
            devs = [
                IoTDevice(
                    organization_id=org.id,
                    device_id="IOT-FLOW-091",
                    name="Ultrasonic Pipe Flow Meter A",
                    device_type="water_flow",
                    is_active=True,
                    is_simulated=False,
                    firmware_version="v2.4.1",
                    last_heartbeat=datetime.utcnow()
                ),
                IoTDevice(
                    organization_id=org.id,
                    device_id="IOT-PWR-104",
                    name="3-Phase Digital Power Monitor",
                    device_type="smart_meter",
                    is_active=True,
                    is_simulated=False,
                    firmware_version="v1.8.0",
                    last_heartbeat=datetime.utcnow()
                )
            ]
            db.add_all(devs)
            db.commit()

        print("SUCCESS! Demo seed data created completely.")

    except Exception as e:
        db.rollback()
        print(f"Error seeding data: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_data()
