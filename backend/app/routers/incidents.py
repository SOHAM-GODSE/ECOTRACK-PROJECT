from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import Optional
from app.database import get_db
from app.models.incident import Incident, IncidentEvidence, IncidentAction
from app.models.organization import OrganizationMembership
from app.models.user import User
from app.schemas.incident import IncidentResponse, IncidentTransition, EvidenceCreate, EvidenceResponse
from app.services.auth import get_current_user
from app.services.incident_agent import transition_incident

router = APIRouter(prefix="/incidents", tags=["Incidents"])


def check_org(org_id, user, db):
    m = db.query(OrganizationMembership).filter(
        OrganizationMembership.organization_id == org_id,
        OrganizationMembership.user_id == user.id,
        OrganizationMembership.is_active == True
    ).first()
    if not m:
        raise HTTPException(403, "Access denied")


@router.get("", response_model=list[IncidentResponse])
def list_incidents(
    org_id: int = Query(...),
    state: Optional[str] = None,
    severity: Optional[str] = None,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    check_org(org_id, current_user, db)
    q = db.query(Incident).filter(Incident.organization_id == org_id)
    if state:
        q = q.filter(Incident.state == state)
    if severity:
        q = q.filter(Incident.severity == severity)
    incidents = q.order_by(desc(Incident.created_at)).limit(limit).all()
    return [IncidentResponse.model_validate(i) for i in incidents]


@router.get("/{incident_id}", response_model=IncidentResponse)
def get_incident(incident_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(404, "Incident not found")
    check_org(incident.organization_id, current_user, db)
    return IncidentResponse.model_validate(incident)


@router.post("/{incident_id}/transition", response_model=IncidentResponse)
def transition(
    incident_id: int,
    payload: IncidentTransition,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(404, "Incident not found")
    check_org(incident.organization_id, current_user, db)
    try:
        updated = transition_incident(db, incident, payload.new_state, payload.description,
                                     current_user.id, payload.after_metrics)
    except ValueError as e:
        raise HTTPException(400, str(e))
    return IncidentResponse.model_validate(updated)


@router.post("/{incident_id}/evidence", response_model=EvidenceResponse, status_code=201)
def add_evidence(
    incident_id: int,
    payload: EvidenceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(404, "Incident not found")
    check_org(incident.organization_id, current_user, db)
    evidence = IncidentEvidence(
        incident_id=incident_id,
        evidence_type=payload.evidence_type,
        title=payload.title,
        description=payload.description,
        data=payload.data,
        added_by_user_id=current_user.id
    )
    db.add(evidence)
    db.commit()
    db.refresh(evidence)
    return EvidenceResponse.model_validate(evidence)


@router.get("/{incident_id}/evidence", response_model=list[EvidenceResponse])
def get_evidence(incident_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(404, "Incident not found")
    check_org(incident.organization_id, current_user, db)
    items = db.query(IncidentEvidence).filter(IncidentEvidence.incident_id == incident_id).all()
    return [EvidenceResponse.model_validate(e) for e in items]


@router.get("/{incident_id}/actions")
def get_actions(incident_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(404, "Incident not found")
    check_org(incident.organization_id, current_user, db)
    actions = db.query(IncidentAction).filter(IncidentAction.incident_id == incident_id).order_by(IncidentAction.created_at).all()
    return [{"id": a.id, "action_type": a.action_type, "description": a.description,
             "old_state": a.old_state, "new_state": a.new_state, "created_at": a.created_at.isoformat()} for a in actions]
