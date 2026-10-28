from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.organization import Organization, OrganizationMembership, MemberRole
from app.models.user import User
from app.schemas.organization import OrganizationCreate, OrganizationResponse, MembershipResponse
from app.services.auth import get_current_user

router = APIRouter(prefix="/organizations", tags=["Organizations"])


@router.post("", response_model=OrganizationResponse, status_code=201)
def create_org(payload: OrganizationCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if db.query(Organization).filter(Organization.slug == payload.slug).first():
        raise HTTPException(400, "Slug already taken")
    org = Organization(**payload.model_dump())
    db.add(org)
    db.flush()
    membership = OrganizationMembership(organization_id=org.id, user_id=current_user.id, role=MemberRole.ADMIN)
    db.add(membership)
    db.commit()
    db.refresh(org)
    return OrganizationResponse.model_validate(org)


@router.get("", response_model=list[OrganizationResponse])
def list_orgs(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    memberships = db.query(OrganizationMembership).filter(
        OrganizationMembership.user_id == current_user.id,
        OrganizationMembership.is_active == True
    ).all()
    org_ids = [m.organization_id for m in memberships]
    orgs = db.query(Organization).filter(Organization.id.in_(org_ids), Organization.is_active == True).all()
    return [OrganizationResponse.model_validate(o) for o in orgs]


@router.get("/my", response_model=list[OrganizationResponse])
def my_orgs(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    memberships = db.query(OrganizationMembership).filter(
        OrganizationMembership.user_id == current_user.id,
        OrganizationMembership.is_active == True
    ).all()
    orgs = [m.organization for m in memberships if m.organization and m.organization.is_active]
    
    # If user has no active organization, automatically link to default facility
    if not orgs:
        default_org = db.query(Organization).filter(Organization.is_active == True).first()
        if default_org:
            membership = OrganizationMembership(
                organization_id=default_org.id,
                user_id=current_user.id,
                role=MemberRole.ADMIN
            )
            db.add(membership)
            db.commit()
            orgs = [default_org]
            
    return [OrganizationResponse.model_validate(o) for o in orgs]


@router.get("/{org_id}", response_model=OrganizationResponse)
def get_org(org_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    org = db.query(Organization).filter(Organization.id == org_id).first()
    if not org:
        raise HTTPException(404, "Organization not found")
    return OrganizationResponse.model_validate(org)


@router.post("/{org_id}/join")
def join_org(org_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    org = db.query(Organization).filter(Organization.id == org_id, Organization.is_active == True).first()
    if not org:
        raise HTTPException(404, "Organization not found")
    existing = db.query(OrganizationMembership).filter(
        OrganizationMembership.organization_id == org_id,
        OrganizationMembership.user_id == current_user.id
    ).first()
    if existing:
        if existing.is_active:
            raise HTTPException(400, "Already a member")
        existing.is_active = True
        db.commit()
        return {"message": "Rejoined organization"}
    membership = OrganizationMembership(organization_id=org_id, user_id=current_user.id)
    db.add(membership)
    db.commit()
    return {"message": "Joined organization"}
