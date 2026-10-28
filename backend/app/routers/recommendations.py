from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime
from app.database import get_db
from app.models.recommendation import Recommendation, RecommendationStatus
from app.models.organization import OrganizationMembership
from app.models.user import User
from app.schemas.recommendation import RecommendationResponse, StatusUpdate
from app.services.auth import get_current_user

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])


@router.get("", response_model=list[RecommendationResponse])
def list_recommendations(org_id: int = Query(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    recs = db.query(Recommendation).filter(
        Recommendation.organization_id == org_id
    ).order_by(desc(Recommendation.priority_score)).all()
    return [RecommendationResponse.model_validate(r) for r in recs]


@router.patch("/{rec_id}/status", response_model=RecommendationResponse)
def update_status(rec_id: int, payload: StatusUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    rec = db.query(Recommendation).filter(Recommendation.id == rec_id).first()
    if not rec:
        raise HTTPException(404, "Recommendation not found")
    try:
        rec.status = RecommendationStatus(payload.status)
    except ValueError:
        raise HTTPException(400, f"Invalid status: {payload.status}")
    if payload.status == "accepted":
        rec.accepted_at = datetime.utcnow()
    elif payload.status == "completed":
        rec.completed_at = datetime.utcnow()
    db.commit()
    db.refresh(rec)
    return RecommendationResponse.model_validate(rec)
