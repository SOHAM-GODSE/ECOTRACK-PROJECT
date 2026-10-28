from __future__ import annotations
import enum
from datetime import datetime
from typing import TYPE_CHECKING, Optional, Dict, Any
from sqlalchemy import String, Boolean, DateTime, Text, ForeignKey, Float, Integer, Enum, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

if TYPE_CHECKING:
    from app.models.organization import Organization


class RecommendationStatus(str, enum.Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    DEFERRED = "deferred"
    COMPLETED = "completed"


class Recommendation(Base):
    __tablename__ = "recommendations"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"), nullable=False)
    incident_id: Mapped[Optional[int]] = mapped_column(ForeignKey("incidents.id"), nullable=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False)  # water, electricity, waste, general
    status: Mapped[RecommendationStatus] = mapped_column(Enum(RecommendationStatus), default=RecommendationStatus.PENDING)
    priority_score: Mapped[float] = mapped_column(Float, default=0.0)  # 0-100
    estimated_savings_kwh: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    estimated_savings_liters: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    estimated_savings_inr: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    estimated_co2_reduction_kg: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    implementation_effort: Mapped[str] = mapped_column(String(20), default="medium")  # low, medium, high
    implementation_cost: Mapped[str] = mapped_column(String(20), default="medium")  # low, medium, high
    evidence_summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    how_to_verify: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    supporting_data: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    accepted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    actual_savings: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)  # measured outcomes
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    organization: Mapped["Organization"] = relationship("Organization", back_populates="recommendations")
