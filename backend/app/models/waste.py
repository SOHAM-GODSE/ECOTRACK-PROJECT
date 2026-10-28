from __future__ import annotations
from datetime import datetime
from typing import Optional, Dict, Any
from sqlalchemy import String, Boolean, DateTime, Text, ForeignKey, Float, Integer, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class WasteClassification(Base):
    __tablename__ = "waste_classifications"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    organization_id: Mapped[Optional[int]] = mapped_column(ForeignKey("organizations.id"), nullable=True)
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True)
    image_path: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    predicted_category: Mapped[str] = mapped_column(String(100), nullable=False)  # wet_organic, dry_recyclable, plastic, paper, metal, glass, e_waste, hazardous, other
    confidence: Mapped[float] = mapped_column(Float, nullable=False)  # 0.0 - 1.0
    all_predictions: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)  # {category: confidence}
    user_correction: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)  # user-corrected category
    disposal_guidance: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    model_version: Mapped[str] = mapped_column(String(50), default="mobilenetv3_waste_v1")
    is_simulated: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class WasteLog(Base):
    __tablename__ = "waste_logs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"), nullable=False)
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True)
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    quantity_kg: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    disposal_method: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)  # recycled, landfill, composted, incinerated
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    logged_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
