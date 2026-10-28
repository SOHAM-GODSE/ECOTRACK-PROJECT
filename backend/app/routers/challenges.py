from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.database import get_db
from app.models.challenge import GreenChallenge, ChallengeParticipant, ChallengeSubmission
from app.models.user import User
from app.services.auth import get_current_user

router = APIRouter(prefix="/challenges", tags=["Green Challenges"])


@router.get("")
def list_challenges(org_id: int = Query(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    challenges = db.query(GreenChallenge).filter(GreenChallenge.organization_id == org_id).order_by(desc(GreenChallenge.created_at)).all()
    return [
        {
            "id": c.id, "title": c.title, "description": c.description,
            "category": c.category, "status": c.status,
            "start_date": c.start_date.isoformat(), "end_date": c.end_date.isoformat(),
            "participant_count": len(c.participants), "submission_count": len(c.submissions)
        } for c in challenges
    ]


@router.post("/{challenge_id}/join")
def join_challenge(challenge_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    challenge = db.query(GreenChallenge).filter(GreenChallenge.id == challenge_id).first()
    if not challenge:
        raise HTTPException(404, "Challenge not found")
    existing = db.query(ChallengeParticipant).filter(
        ChallengeParticipant.challenge_id == challenge_id,
        ChallengeParticipant.user_id == current_user.id
    ).first()
    if existing:
        raise HTTPException(400, "Already joined")
    p = ChallengeParticipant(challenge_id=challenge_id, user_id=current_user.id)
    db.add(p)
    db.commit()
    return {"message": "Joined challenge"}


@router.get("/{challenge_id}/leaderboard")
def leaderboard(challenge_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    participants = db.query(ChallengeParticipant).filter(
        ChallengeParticipant.challenge_id == challenge_id
    ).order_by(desc(ChallengeParticipant.score)).all()
    return [{"user_id": p.user_id, "score": p.score, "joined_at": p.joined_at.isoformat()} for p in participants]
