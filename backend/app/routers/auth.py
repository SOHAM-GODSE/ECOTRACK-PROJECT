from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db
from app.models.user import User
from app.models.audit import AuditLog
from app.schemas.auth import UserRegister, UserLogin, TokenResponse, UserResponse
from app.services.auth import get_password_hash, verify_password, create_access_token, get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=TokenResponse, status_code=201)
def register(payload: UserRegister, request: Request, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(400, "Email already registered")
    user = User(
        email=payload.email,
        full_name=payload.full_name,
        hashed_password=get_password_hash(payload.password),
        phone=payload.phone,
        is_verified=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Auto-link to default organization
    from app.models.organization import Organization, OrganizationMembership, MemberRole
    default_org = db.query(Organization).filter(Organization.is_active == True).first()
    if default_org:
        db.add(OrganizationMembership(organization_id=default_org.id, user_id=user.id, role=MemberRole.ADMIN))
        db.commit()

    db.add(AuditLog(user_id=user.id, action="register", resource_type="user", resource_id=user.id,
                    description=f"Registered: {user.email}",
                    ip_address=getattr(request.client, 'host', None)))
    db.commit()
    token = create_access_token({"sub": str(user.id)})
    return TokenResponse(access_token=token, user=UserResponse.model_validate(user))


@router.post("/login", response_model=TokenResponse)
def login(payload: UserLogin, request: Request, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email, User.is_active == True).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(401, "Invalid email or password")
    user.last_login = datetime.utcnow()
    db.add(AuditLog(user_id=user.id, action="login", resource_type="user", resource_id=user.id,
                    ip_address=getattr(request.client, 'host', None)))
    db.commit()
    db.refresh(user)
    token = create_access_token({"sub": str(user.id)})
    return TokenResponse(access_token=token, user=UserResponse.model_validate(user))


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return UserResponse.model_validate(current_user)


@router.put("/me", response_model=UserResponse)
def update_me(data: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    for key, value in data.items():
        if key in {"full_name", "phone"}:
            setattr(current_user, key, value)
    db.commit()
    db.refresh(current_user)
    return UserResponse.model_validate(current_user)
