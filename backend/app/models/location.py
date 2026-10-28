from __future__ import annotations
from datetime import datetime, date
from typing import Optional, Dict, Any
from sqlalchemy import String, Boolean, DateTime, Text, Float, Date, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class RecyclingLocation(Base):
    __tablename__ = "recycling_locations"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    location_type: Mapped[str] = mapped_column(String(50), nullable=False)  # recycling_centre, e_waste, collection_point, composting
    address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    city: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    state: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    accepts_categories: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)  # list of waste categories accepted
    operating_hours: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    website: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    last_verified_at: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    source: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
