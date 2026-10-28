from __future__ import annotations
import enum
from datetime import datetime
from typing import TYPE_CHECKING, List, Optional, Dict, Any
from sqlalchemy import String, Boolean, DateTime, Text, ForeignKey, Float, Integer, Enum, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

if TYPE_CHECKING:
    from app.models.organization import Organization


class IncidentState(str, enum.Enum):
    NEW = "new"
    ACKNOWLEDGED = "acknowledged"
    INVESTIGATING = "investigating"
    ACTION_REQUIRED = "action_required"
    RESOLVED = "resolved"
    IMPACT_VERIFIED = "impact_verified"
    REOPENED = "reopened"


class IncidentSeverity(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class IncidentType(str, enum.Enum):
    WATER_ANOMALY = "water_anomaly"
    ELECTRICITY_ANOMALY = "electricity_anomaly"
    WASTE_VIOLATION = "waste_violation"
    LEAK_SUSPECTED = "leak_suspected"
    UNUSUAL_CONSUMPTION = "unusual_consumption"
    METER_FAULT = "meter_fault"
    OTHER = "other"


class Incident(Base):
    __tablename__ = "incidents"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    incident_type: Mapped[IncidentType] = mapped_column(Enum(IncidentType), nullable=False)
    severity: Mapped[IncidentSeverity] = mapped_column(Enum(IncidentSeverity), default=IncidentSeverity.MEDIUM)
    state: Mapped[IncidentState] = mapped_column(Enum(IncidentState), default=IncidentState.NEW)
    assigned_to_user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True)
    created_by_user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True)
    detected_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    acknowledged_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    resolved_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    impact_verified_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    ai_evidence: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)  # structured evidence from agent
    ai_recommendations: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    before_metrics: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    after_metrics: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    estimated_impact: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    verified_impact: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    source_meter_type: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)  # water, electricity
    source_meter_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    is_simulated: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    organization: Mapped["Organization"] = relationship("Organization", back_populates="incidents")
    evidence_items: Mapped[List["IncidentEvidence"]] = relationship("IncidentEvidence", back_populates="incident", cascade="all, delete-orphan")
    actions: Mapped[List["IncidentAction"]] = relationship("IncidentAction", back_populates="incident", cascade="all, delete-orphan")


class IncidentEvidence(Base):
    __tablename__ = "incident_evidence"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    incident_id: Mapped[int] = mapped_column(ForeignKey("incidents.id"), nullable=False)
    evidence_type: Mapped[str] = mapped_column(String(50), nullable=False)  # reading, image, note, calculation
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    data: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    file_path: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    added_by_user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    incident: Mapped["Incident"] = relationship("Incident", back_populates="evidence_items")


class IncidentAction(Base):
    __tablename__ = "incident_actions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    incident_id: Mapped[int] = mapped_column(ForeignKey("incidents.id"), nullable=False)
    action_type: Mapped[str] = mapped_column(String(50), nullable=False)  # state_change, note, intervention
    description: Mapped[str] = mapped_column(Text, nullable=False)
    performed_by_user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True)
    old_state: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    new_state: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    incident: Mapped["Incident"] = relationship("Incident", back_populates="actions")
