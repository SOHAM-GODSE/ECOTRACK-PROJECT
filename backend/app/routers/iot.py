from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime
from app.database import get_db
from app.models.iot import IoTDevice, SensorTelemetry
from app.models.user import User
from app.services.auth import get_current_user

router = APIRouter(prefix="/iot", tags=["IoT Devices"])


@router.get("/devices")
def list_devices(org_id: int = Query(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    devices = db.query(IoTDevice).filter(IoTDevice.organization_id == org_id).all()
    return [
        {
            "id": d.id, "device_id": d.device_id, "name": d.name,
            "device_type": d.device_type, "is_active": d.is_active,
            "is_simulated": d.is_simulated,
            "last_heartbeat": d.last_heartbeat.isoformat() if d.last_heartbeat else None,
            "status": "online" if d.last_heartbeat and (datetime.utcnow() - d.last_heartbeat).seconds < 300 else "offline"
        } for d in devices
    ]


@router.post("/telemetry")
def ingest_telemetry(
    payload: dict,
    db: Session = Depends(get_db)
):
    """IoT telemetry ingestion endpoint. Device authenticates via device_id."""
    device_id = payload.get("device_id")
    device = db.query(IoTDevice).filter(IoTDevice.device_id == device_id, IoTDevice.is_active == True).first()
    if not device:
        raise HTTPException(404, "Device not found or inactive")
    
    device.last_heartbeat = datetime.utcnow()
    
    raw_ts = payload.get("timestamp", datetime.utcnow().isoformat())
    if isinstance(raw_ts, str):
        timestamp = datetime.fromisoformat(raw_ts.replace("Z", "+00:00"))
    else:
        timestamp = datetime.utcnow()

    telemetry = SensorTelemetry(
        device_id=device.id,
        measurement_type=payload.get("measurement_type", "unknown"),
        value=payload.get("value", 0),
        unit=payload.get("unit", ""),
        timestamp=timestamp,
        is_simulated=device.is_simulated,
        raw_payload=payload
    )
    db.add(telemetry)
    db.commit()
    return {"status": "accepted", "device_id": device_id}


@router.post("/heartbeat/{device_id}")
def heartbeat(device_id: str, db: Session = Depends(get_db)):
    device = db.query(IoTDevice).filter(IoTDevice.device_id == device_id).first()
    if not device:
        raise HTTPException(404, "Device not found")
    device.last_heartbeat = datetime.utcnow()
    db.commit()
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}
