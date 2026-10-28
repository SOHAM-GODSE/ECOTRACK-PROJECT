from __future__ import annotations
import enum
from datetime import datetime
from typing import TYPE_CHECKING, List, Optional
from sqlalchemy import String, Boolean, DateTime, Text, ForeignKey, Float, Integer, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

if TYPE_CHECKING:
    from app.models.organization import Organization


class ElectricityMeter(Base):
    __tablename__ = "electricity_meters"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    meter_id: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    location: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    unit: Mapped[str] = mapped_column(String(20), default="kWh")
    status: Mapped[str] = mapped_column(String(20), default="active")
    meter_type: Mapped[str] = mapped_column(String(50), default="standard")  # standard, smart, industrial
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    installed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    organization: Mapped["Organization"] = relationship("Organization", back_populates="electricity_meters")
    readings: Mapped[List["ElectricityReading"]] = relationship("ElectricityReading", back_populates="meter", order_by="ElectricityReading.recorded_at")
    bills: Mapped[List["ElectricityBill"]] = relationship("ElectricityBill", back_populates="meter")


class ElectricityReading(Base):
    __tablename__ = "electricity_readings"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    meter_id: Mapped[int] = mapped_column(ForeignKey("electricity_meters.id"), nullable=False)
    reading_value: Mapped[float] = mapped_column(Float, nullable=False)  # cumulative kWh
    unit: Mapped[str] = mapped_column(String(20), default="kWh")
    source: Mapped[str] = mapped_column(String(20), default="manual")  # manual, iot, import, simulated
    recorded_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)
    entered_by_user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True)
    consumption: Mapped[Optional[float]] = mapped_column(Float, nullable=True)  # kWh consumed since last reading
    cost_estimate: Mapped[Optional[float]] = mapped_column(Float, nullable=True)  # INR
    carbon_kg: Mapped[Optional[float]] = mapped_column(Float, nullable=True)  # kg CO2e
    is_anomaly: Mapped[bool] = mapped_column(Boolean, default=False)
    anomaly_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    quality_flag: Mapped[str] = mapped_column(String(20), default="ok")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    meter: Mapped["ElectricityMeter"] = relationship("ElectricityMeter", back_populates="readings")


class ElectricityBill(Base):
    __tablename__ = "electricity_bills"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    meter_id: Mapped[int] = mapped_column(ForeignKey("electricity_meters.id"), nullable=False)
    bill_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    period_start: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    period_end: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    total_consumption: Mapped[float] = mapped_column(Float, nullable=False)  # kWh
    amount: Mapped[Optional[float]] = mapped_column(Float, nullable=True)  # INR
    currency: Mapped[str] = mapped_column(String(10), default="INR")
    tariff_rate: Mapped[Optional[float]] = mapped_column(Float, nullable=True)  # INR per kWh
    carbon_kg: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    meter: Mapped["ElectricityMeter"] = relationship("ElectricityMeter", back_populates="bills")
