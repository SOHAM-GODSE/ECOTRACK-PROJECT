from __future__ import annotations
import enum
from datetime import datetime
from typing import TYPE_CHECKING, List, Optional
from sqlalchemy import String, Boolean, DateTime, Enum, Text, ForeignKey, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.water import WaterMeter
    from app.models.electricity import ElectricityMeter
    from app.models.incident import Incident
    from app.models.recommendation import Recommendation
    from app.models.challenge import GreenChallenge
    from app.models.iot import IoTDevice
    from app.models.carbon import CarbonCalculation


class MemberRole(str, enum.Enum):
    ADMIN = "admin"
    MEMBER = "member"
    MAINTENANCE = "maintenance"
    VIEWER = "viewer"


class Organization(Base):
    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    org_type: Mapped[str] = mapped_column(String(50), default="college")  # college, housing, business, household
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    city: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    state: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    country: Mapped[str] = mapped_column(String(100), default="India")
    latitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    longitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    memberships: Mapped[List["OrganizationMembership"]] = relationship("OrganizationMembership", back_populates="organization")
    water_meters: Mapped[List["WaterMeter"]] = relationship("WaterMeter", back_populates="organization")
    electricity_meters: Mapped[List["ElectricityMeter"]] = relationship("ElectricityMeter", back_populates="organization")
    incidents: Mapped[List["Incident"]] = relationship("Incident", back_populates="organization")
    recommendations: Mapped[List["Recommendation"]] = relationship("Recommendation", back_populates="organization")
    challenges: Mapped[List["GreenChallenge"]] = relationship("GreenChallenge", back_populates="organization")
    iot_devices: Mapped[List["IoTDevice"]] = relationship("IoTDevice", back_populates="organization")
    carbon_calculations: Mapped[List["CarbonCalculation"]] = relationship("CarbonCalculation", back_populates="organization")


class OrganizationMembership(Base):
    __tablename__ = "organization_memberships"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    role: Mapped[MemberRole] = mapped_column(Enum(MemberRole), default=MemberRole.MEMBER)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    joined_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    organization: Mapped["Organization"] = relationship("Organization", back_populates="memberships")
    user: Mapped["User"] = relationship("User", back_populates="memberships")
