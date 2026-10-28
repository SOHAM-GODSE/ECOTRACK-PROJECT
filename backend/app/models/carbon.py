from __future__ import annotations
from datetime import datetime, date
from typing import TYPE_CHECKING, Optional
from sqlalchemy import String, Boolean, DateTime, Text, ForeignKey, Float, Integer, Date, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

if TYPE_CHECKING:
    from app.models.organization import Organization


class EmissionFactor(Base):
    __tablename__ = "emission_factors"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False)  # electricity, transport, waste
    activity: Mapped[str] = mapped_column(String(255), nullable=False)  # grid_electricity_india, petrol_car, etc
    factor_value: Mapped[float] = mapped_column(Float, nullable=False)
    unit_numerator: Mapped[str] = mapped_column(String(50), nullable=False)  # kg_co2e
    unit_denominator: Mapped[str] = mapped_column(String(50), nullable=False)  # kWh, km, kg
    region: Mapped[str] = mapped_column(String(100), default="India")
    source: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    source_url: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    effective_from: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    effective_to: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class CarbonCalculation(Base):
    __tablename__ = "carbon_calculations"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"), nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    activity: Mapped[str] = mapped_column(String(255), nullable=False)
    activity_value: Mapped[float] = mapped_column(Float, nullable=False)
    activity_unit: Mapped[str] = mapped_column(String(50), nullable=False)
    emission_factor_id: Mapped[Optional[int]] = mapped_column(ForeignKey("emission_factors.id"), nullable=True)
    emission_factor_value: Mapped[float] = mapped_column(Float, nullable=False)
    co2e_kg: Mapped[float] = mapped_column(Float, nullable=False)
    period_start: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    period_end: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    calculated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    source_reference: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)  # e.g. electricity_reading:42

    organization: Mapped["Organization"] = relationship("Organization", back_populates="carbon_calculations")
