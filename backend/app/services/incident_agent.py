"""AI Environmental Incident Response Agent.

Workflow: anomaly detected → evidence gathering → urgency scoring → 
recommendations → incident creation → state management.
"""
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.incident import Incident, IncidentEvidence, IncidentAction, IncidentState, IncidentSeverity, IncidentType
from app.models.notification import Notification

# Valid state transitions
STATE_TRANSITIONS = {
    IncidentState.NEW: [IncidentState.ACKNOWLEDGED, IncidentState.RESOLVED],
    IncidentState.ACKNOWLEDGED: [IncidentState.INVESTIGATING, IncidentState.RESOLVED],
    IncidentState.INVESTIGATING: [IncidentState.ACTION_REQUIRED, IncidentState.RESOLVED],
    IncidentState.ACTION_REQUIRED: [IncidentState.RESOLVED, IncidentState.INVESTIGATING],
    IncidentState.RESOLVED: [IncidentState.IMPACT_VERIFIED, IncidentState.REOPENED],
    IncidentState.IMPACT_VERIFIED: [IncidentState.REOPENED],
    IncidentState.REOPENED: [IncidentState.ACKNOWLEDGED, IncidentState.INVESTIGATING],
}


def is_valid_transition(current_state: IncidentState, new_state: IncidentState) -> bool:
    return new_state in STATE_TRANSITIONS.get(current_state, [])


def calculate_severity(anomaly_score: float, consumption_pct_increase: float) -> IncidentSeverity:
    if anomaly_score >= 5.0 or consumption_pct_increase >= 200:
        return IncidentSeverity.CRITICAL
    elif anomaly_score >= 3.0 or consumption_pct_increase >= 100:
        return IncidentSeverity.HIGH
    elif anomaly_score >= 2.5 or consumption_pct_increase >= 50:
        return IncidentSeverity.MEDIUM
    return IncidentSeverity.LOW


def generate_water_recommendations(anomaly_data: dict) -> list[dict]:
    """Generate ranked recommendations for water anomaly."""
    return [
        {
            "rank": 1,
            "action": "Inspect visible pipes and connections for leaks",
            "rationale": "Most common cause of sudden water consumption increase",
            "effort": "low",
            "urgency": "high",
            "estimated_savings": "Could prevent continued water loss"
        },
        {
            "rank": 2,
            "action": "Check all taps, valves and fixtures",
            "rationale": "Running taps or stuck valves cause continuous flow",
            "effort": "low",
            "urgency": "high",
            "estimated_savings": "A dripping tap can waste 15-20 litres per day"
        },
        {
            "rank": 3,
            "action": "Verify meter reading accuracy",
            "rationale": "Rule out meter reset or data entry error",
            "effort": "low",
            "urgency": "medium",
            "estimated_savings": "Eliminates false positive"
        },
        {
            "rank": 4,
            "action": "Monitor consumption over the next 24 hours",
            "rationale": "Confirm if anomaly persists or was a one-time event",
            "effort": "low",
            "urgency": "medium",
            "estimated_savings": "Provides evidence for further action"
        }
    ]


def generate_electricity_recommendations(anomaly_data: dict) -> list[dict]:
    """Generate ranked recommendations for electricity anomaly."""
    return [
        {
            "rank": 1,
            "action": "Review recent changes in equipment or operations",
            "rationale": "New equipment or longer operating hours cause consumption spikes",
            "effort": "low",
            "urgency": "high",
            "estimated_savings": "Identifies root cause quickly"
        },
        {
            "rank": 2,
            "action": "Check HVAC systems and cooling equipment",
            "rationale": "HVAC is typically the largest electricity consumer",
            "effort": "medium",
            "urgency": "high",
            "estimated_savings": "AC optimization can reduce consumption by 20-30%"
        },
        {
            "rank": 3,
            "action": "Verify meter and IoT device connectivity",
            "rationale": "Reconnection after outage can cause apparent spike",
            "effort": "low",
            "urgency": "medium",
            "estimated_savings": "Eliminates false positive"
        },
        {
            "rank": 4,
            "action": "Audit lighting and idle equipment",
            "rationale": "Lights and equipment left on during off-hours increase consumption",
            "effort": "low",
            "urgency": "medium",
            "estimated_savings": "Typically 10-15% reduction potential"
        }
    ]


def create_incident_from_anomaly(
    db: Session,
    org_id: int,
    meter_type: str,  # 'water' or 'electricity'
    meter_id: int,
    meter_name: str,
    anomaly_result: dict,
    current_value: float,
    historical_mean: float,
    unit: str,
    user_id: int | None = None
) -> Incident:
    """Create incident from detected anomaly with full evidence."""
    
    # Calculate percentage increase
    pct_increase = 0.0
    if historical_mean > 0:
        pct_increase = ((current_value - historical_mean) / historical_mean) * 100
    
    anomaly_score = anomaly_result.get("anomaly_score", 0.0)
    severity = calculate_severity(anomaly_score, abs(pct_increase))
    
    if meter_type == "water":
        incident_type = IncidentType.WATER_ANOMALY if pct_increase < 300 else IncidentType.LEAK_SUSPECTED
        title = f"Unusual water consumption detected on {meter_name}"
        recommendations = generate_water_recommendations(anomaly_result)
    else:
        incident_type = IncidentType.ELECTRICITY_ANOMALY
        title = f"Unusual electricity consumption detected on {meter_name}"
        recommendations = generate_electricity_recommendations(anomaly_result)
    
    description = (
        f"Anomaly detected: {current_value:.2f} {unit} vs historical mean {historical_mean:.2f} {unit} "
        f"({pct_increase:+.1f}%). {anomaly_result.get('explanation', '')}"
    )
    
    ai_evidence = {
        "anomaly_score": anomaly_score,
        "z_score": anomaly_result.get("z_score"),
        "iqr_score": anomaly_result.get("iqr_score"),
        "method": anomaly_result.get("method"),
        "current_value": current_value,
        "historical_mean": historical_mean,
        "pct_change": round(pct_increase, 2),
        "unit": unit,
        "n_samples": anomaly_result.get("n_samples"),
        "explanation": anomaly_result.get("explanation"),
        "detection_timestamp": datetime.utcnow().isoformat()
    }
    
    incident = Incident(
        organization_id=org_id,
        title=title,
        description=description,
        incident_type=incident_type,
        severity=severity,
        state=IncidentState.NEW,
        created_by_user_id=user_id,
        detected_at=datetime.utcnow(),
        ai_evidence=ai_evidence,
        ai_recommendations={"recommendations": recommendations},
        before_metrics={
            "historical_mean": historical_mean,
            "unit": unit,
            "n_samples": anomaly_result.get("n_samples")
        },
        source_meter_type=meter_type,
        source_meter_id=meter_id,
        is_simulated=False
    )
    db.add(incident)
    db.commit()
    db.refresh(incident)
    
    # Add evidence item
    evidence = IncidentEvidence(
        incident_id=incident.id,
        evidence_type="reading",
        title=f"Anomalous {meter_type} reading",
        description=description,
        data=ai_evidence
    )
    db.add(evidence)
    
    # Add initial action
    action = IncidentAction(
        incident_id=incident.id,
        action_type="state_change",
        description=f"Incident automatically created by anomaly detection agent. {anomaly_result.get('explanation', '')}",
        new_state=IncidentState.NEW.value
    )
    db.add(action)
    db.commit()
    
    return incident


def transition_incident(
    db: Session,
    incident: Incident,
    new_state: str,
    description: str,
    user_id: int | None = None,
    after_metrics: dict | None = None
) -> Incident:
    """Transition incident to new state with validation."""
    try:
        new_state_enum = IncidentState(new_state)
        current_state_enum = IncidentState(incident.state)
    except ValueError:
        raise ValueError(f"Invalid state: {new_state}")
    
    if not is_valid_transition(current_state_enum, new_state_enum):
        raise ValueError(
            f"Cannot transition from '{incident.state.value if isinstance(incident.state, IncidentState) else incident.state}' to '{new_state}'. "
            f"Valid transitions: {[s.value for s in STATE_TRANSITIONS.get(current_state_enum, [])]}"
        )
    
    old_state = incident.state.value if isinstance(incident.state, IncidentState) else incident.state
    incident.state = new_state_enum
    incident.updated_at = datetime.utcnow()
    
    if new_state_enum == IncidentState.ACKNOWLEDGED:
        incident.acknowledged_at = datetime.utcnow()
    elif new_state_enum == IncidentState.RESOLVED:
        incident.resolved_at = datetime.utcnow()
        if after_metrics:
            incident.after_metrics = after_metrics
    elif new_state_enum == IncidentState.IMPACT_VERIFIED:
        incident.impact_verified_at = datetime.utcnow()
        if after_metrics:
            incident.after_metrics = after_metrics
    
    action = IncidentAction(
        incident_id=incident.id,
        action_type="state_change",
        description=description,
        performed_by_user_id=user_id,
        old_state=old_state,
        new_state=new_state
    )
    db.add(action)
    db.commit()
    db.refresh(incident)
    return incident
