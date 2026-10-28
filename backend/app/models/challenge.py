from __future__ import annotations
import enum
from datetime import datetime
from typing import TYPE_CHECKING, List, Optional
from sqlalchemy import String, Boolean, DateTime, Text, ForeignKey, Float, Integer, Enum, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

if TYPE_CHECKING:
    from app.models.organization import Organization


class ChallengeStatus(str, enum.Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class GreenChallenge(Base):
    __tablename__ = "green_challenges"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"), nullable=False)
    created_by_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[ChallengeStatus] = mapped_column(Enum(ChallengeStatus), default=ChallengeStatus.ACTIVE)
    start_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    target_metric: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    target_value: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    scoring_method: Mapped[str] = mapped_column(String(100), default="participation")  # participation, metric_reduction
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    organization: Mapped["Organization"] = relationship("Organization", back_populates="challenges")
    participants: Mapped[List["ChallengeParticipant"]] = relationship("ChallengeParticipant", back_populates="challenge", cascade="all, delete-orphan")
    submissions: Mapped[List["ChallengeSubmission"]] = relationship("ChallengeSubmission", back_populates="challenge", cascade="all, delete-orphan")


class ChallengeParticipant(Base):
    __tablename__ = "challenge_participants"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    challenge_id: Mapped[int] = mapped_column(ForeignKey("green_challenges.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    score: Mapped[float] = mapped_column(Float, default=0.0)
    joined_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    challenge: Mapped["GreenChallenge"] = relationship("GreenChallenge", back_populates="participants")


class ChallengeSubmission(Base):
    __tablename__ = "challenge_submissions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    challenge_id: Mapped[int] = mapped_column(ForeignKey("green_challenges.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    evidence_url: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="pending")  # pending, approved, rejected
    reviewer_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    points_awarded: Mapped[float] = mapped_column(Float, default=0.0)
    submitted_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    reviewed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    challenge: Mapped["GreenChallenge"] = relationship("GreenChallenge", back_populates="submissions")
