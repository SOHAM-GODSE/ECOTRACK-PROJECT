"""Authentication and authorization services for EcoTrack AI."""
import bcrypt
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.config import get_settings
from app.database import get_db
from app.models.user import User, UserRole
from app.models.organization import OrganizationMembership, MemberRole

settings = get_settings()
bearerScheme = HTTPBearer(auto_error=False)


def verify_password(plain: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(plain.encode('utf-8'), hashed.encode('utf-8'))
    except Exception:
        return False


def get_password_hash(password: str) -> str:
    # bcrypt limits passwords to 72 bytes
    pwd_bytes = password.encode('utf-8')[:72]
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt).decode('utf-8')


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.access_token_expire_minutes))
    to_encode["exp"] = expire
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearerScheme),
    db: Session = Depends(get_db)
) -> User:
    if not credentials:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Authentication required")
    try:
        payload = jwt.decode(credentials.credentials, settings.secret_key, algorithms=[settings.algorithm])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid token")
    except JWTError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid or expired token")
    user = db.query(User).filter(User.id == int(user_id), User.is_active == True).first()
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "User not found")
    return user


def require_platform_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != UserRole.PLATFORM_ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Platform admin access required")
    return current_user


def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearerScheme),
    db: Session = Depends(get_db)
) -> Optional[User]:
    if not credentials:
        return None
    try:
        return get_current_user(credentials, db)
    except HTTPException:
        return None


def get_user_primary_org_id(user: User, db: Session) -> Optional[int]:
    """Helper to get user's active organization ID if any."""
    membership = (
        db.query(OrganizationMembership)
        .filter(OrganizationMembership.user_id == user.id, OrganizationMembership.is_active == True)
        .first()
    )
    return membership.organization_id if membership else None


def require_org_access(
    org_id: int,
    current_user: User,
    db: Session,
    min_role: Optional[MemberRole] = None
) -> OrganizationMembership:
    """Verifies that current user has access to specified organization."""
    if current_user.role == UserRole.PLATFORM_ADMIN:
        membership = (
            db.query(OrganizationMembership)
            .filter(OrganizationMembership.organization_id == org_id, OrganizationMembership.user_id == current_user.id)
            .first()
        )
        if membership:
            return membership
        return OrganizationMembership(organization_id=org_id, user_id=current_user.id, role=MemberRole.ADMIN, is_active=True)

    membership = (
        db.query(OrganizationMembership)
        .filter(
            OrganizationMembership.organization_id == org_id,
            OrganizationMembership.user_id == current_user.id,
            OrganizationMembership.is_active == True,
        )
        .first()
    )
    if not membership:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied for this organization")

    if min_role == MemberRole.ADMIN and membership.role != MemberRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Organization admin role required")

    return membership
