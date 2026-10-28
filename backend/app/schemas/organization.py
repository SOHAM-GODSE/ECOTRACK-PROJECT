from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class OrganizationCreate(BaseModel):
    name: str = Field(min_length=2, max_length=255)
    slug: str = Field(min_length=2, max_length=100, pattern=r'^[a-z0-9-]+$')
    org_type: str = "college"
    description: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: str = "India"
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class OrganizationResponse(BaseModel):
    id: int
    name: str
    slug: str
    org_type: str
    description: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class MembershipResponse(BaseModel):
    id: int
    organization_id: int
    user_id: int
    role: str
    is_active: bool
    joined_at: datetime

    class Config:
        from_attributes = True
