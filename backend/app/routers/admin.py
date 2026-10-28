from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User, UserRole
from app.models.organization import Organization
from app.models.audit import AuditLog
from app.services.auth import get_current_user

router = APIRouter(prefix="/admin", tags=["Administration"])


def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.role not in [UserRole.PLATFORM_ADMIN, UserRole.ORG_ADMIN]:
        raise HTTPException(403, "Admin access required")
    return current_user


@router.get("/users")
def list_users(db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    users = db.query(User).all()
    return [{"id": u.id, "email": u.email, "full_name": u.full_name, "role": u.role,
             "is_active": u.is_active, "created_at": u.created_at.isoformat()} for u in users]


@router.get("/organizations")
def list_orgs(db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    orgs = db.query(Organization).all()
    return [{"id": o.id, "name": o.name, "slug": o.slug, "org_type": o.org_type,
             "is_active": o.is_active, "created_at": o.created_at.isoformat()} for o in orgs]


@router.get("/audit-logs")
def get_audit_logs(limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    logs = db.query(AuditLog).order_by(AuditLog.created_at.desc()).limit(limit).all()
    return [{"id": l.id, "user_id": l.user_id, "action": l.action, "resource_type": l.resource_type,
             "description": l.description, "created_at": l.created_at.isoformat()} for l in logs]


@router.get("/health")
def system_health(db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    user_count = db.query(User).count()
    org_count = db.query(Organization).count()
    return {"status": "healthy", "users": user_count, "organizations": org_count}
