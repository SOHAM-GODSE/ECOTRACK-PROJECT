from __future__ import annotations
import enum
from datetime import datetime
from typing import TYPE_CHECKING, List, Optional
from sqlalchemy import String, Boolean, DateTime, Text, ForeignKey, Float, Integer, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

if TYPE_CHECKING:
    from app.models.organization import Organization


class MeterStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    FAULTY = "faulty"
    MAINTENANCE = "maintenance"


class ReadingSource(str, enum.Enum):
    MANUAL = "manual"
    IOT = "iot"
    IMPORT = "import"
    SIMULATED = "simulated"


class WaterMeter(Base):
    __tablename__ = "water_meters"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    meter_id: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    location: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    unit: Mapped[str] = mapped_column(String(20), default="liters")  # liters, cubic_meters, gallons
    status: Mapped[MeterStatus] = mapped_column(Enum(MeterStatus), default=MeterStatus.ACTIVE)
    is_cumulative: Mapped[bool] = mapped_column(Boolean, default=True)  # cumulative vs flow rate
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    installed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    organization: Mapped["Organization"] = relationship("Organization", back_populates="water_meters")
    readings: Mapped[List["WaterReading"]] = relationship("WaterReading", back_populates="meter", order_by="WaterReading.recorded_at")
    bills: Mapped[List["WaterBill"]] = relationship("WaterBill", back_populates="meter")


class WaterReading(Base):
    __tablename__ = "water_readings"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    meter_id: Mapped[int] = mapped_column(ForeignKey("water_meters.id"), nullable=False)
    reading_value: Mapped[float] = mapped_column(Float, nullable=False)
    unit: Mapped[str] = mapped_column(String(20), default="liters")
    source: Mapped[ReadingSource] = mapped_column(Enum(ReadingSource), default=ReadingSource.MANUAL)
    recorded_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)
    entered_by_user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True)
    consumption: Mapped[Optional[float]] = mapped_column(Float, nullable=True)  # calculated: current - previous
    is_anomaly: Mapped[bool] = mapped_column(Boolean, default=False)
    anomaly_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    quality_flag: Mapped[str] = mapped_column(String(20), default="ok")  # ok, suspect, invalid
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    meter: Mapped["WaterMeter"] = relationship("WaterMeter", back_populates="readings")


class WaterBill(Base):
    __tablename__ = "water_bills"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    meter_id: Mapped[int] = mapped_column(ForeignKey("water_meters.id"), nullable=False)
    bill_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    period_start: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    period_end: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    total_consumption: Mapped[float] = mapped_column(Float, nullable=False)
    unit: Mapped[str] = mapped_column(String(20), default="liters")
    amount: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    currency: Mapped[str] = mapped_column(String(10), default="INR")
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    meter: Mapped["WaterMeter"] = relationship("WaterMeter", back_populates="bills")
