from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models.location import RecyclingLocation
from app.models.user import User
from app.services.auth import get_current_user

router = APIRouter(prefix="/locations", tags=["Recycling Locations"])


@router.get("")
def list_locations(
    city: Optional[str] = Query(None),
    location_type: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    q = db.query(RecyclingLocation).filter(RecyclingLocation.is_active == True)
    if city:
        q = q.filter(RecyclingLocation.city.ilike(f"%{city}%"))
    if location_type:
        q = q.filter(RecyclingLocation.location_type == location_type)
    locations = q.all()
    return [
        {
            "id": l.id, "name": l.name, "location_type": l.location_type,
            "address": l.address, "city": l.city, "state": l.state,
            "latitude": l.latitude, "longitude": l.longitude,
            "accepts_categories": l.accepts_categories,
            "operating_hours": l.operating_hours, "phone": l.phone,
            "is_verified": l.is_verified, "source": l.source
        } for l in locations
    ]
