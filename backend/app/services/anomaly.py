"""Statistical anomaly detection for water and electricity readings."""
import numpy as np
from typing import Optional


def detect_anomaly_zscore(values: list[float], new_value: float, threshold: float = 2.5) -> tuple[bool, float, str]:
    """Z-score based anomaly detection.
    Returns: (is_anomaly, score, explanation)
    """
    if len(values) < 7:
        return False, 0.0, "Insufficient historical data for anomaly detection (need at least 7 readings)"
    
    arr = np.array(values)
    mean = np.mean(arr)
    std = np.std(arr)
    
    if std == 0:
        return False, 0.0, "No variance in historical data"
    
    z_score = abs((new_value - mean) / std)
    is_anomaly = z_score > threshold
    
    explanation = ""
    if is_anomaly:
        direction = "above" if new_value > mean else "below"
        explanation = (f"Value {new_value:.2f} is {z_score:.1f} standard deviations {direction} "
                      f"the historical mean of {mean:.2f} (std={std:.2f}). "
                      f"Threshold: {threshold} std deviations.")
    else:
        explanation = f"Value within normal range (z-score={z_score:.2f}, threshold={threshold})"
    
    return is_anomaly, round(float(z_score), 3), explanation


def detect_anomaly_iqr(values: list[float], new_value: float, multiplier: float = 1.5) -> tuple[bool, float, str]:
    """IQR-based anomaly detection."""
    if len(values) < 4:
        return False, 0.0, "Insufficient data for IQR analysis"
    
    arr = np.array(values)
    q1 = np.percentile(arr, 25)
    q3 = np.percentile(arr, 75)
    iqr = q3 - q1
    
    lower = q1 - multiplier * iqr
    upper = q3 + multiplier * iqr
    
    is_anomaly = new_value < lower or new_value > upper
    score = 0.0
    if is_anomaly:
        score = max(abs(new_value - lower), abs(new_value - upper)) / max(iqr, 1.0)
    
    explanation = ""
    if is_anomaly:
        explanation = (f"Value {new_value:.2f} is outside the IQR range [{lower:.2f}, {upper:.2f}]. "
                      f"Q1={q1:.2f}, Q3={q3:.2f}, IQR={iqr:.2f}.")
    else:
        explanation = f"Value within IQR range [{lower:.2f}, {upper:.2f}]"
    
    return is_anomaly, round(float(score), 3), explanation


def combined_anomaly_detection(
    historical_values: list[float],
    new_value: float,
    zscore_threshold: float = 2.5,
    iqr_multiplier: float = 1.5
) -> dict:
    """Run both z-score and IQR detection. Return combined result."""
    if len(historical_values) < 7:
        return {
            "is_anomaly": False,
            "anomaly_score": 0.0,
            "method": "insufficient_data",
            "explanation": f"Need at least 7 readings for anomaly detection (have {len(historical_values)})",
            "data_sufficient": False
        }
    
    z_anomaly, z_score, z_explanation = detect_anomaly_zscore(historical_values, new_value, zscore_threshold)
    iqr_anomaly, iqr_score, iqr_explanation = detect_anomaly_iqr(historical_values, new_value, iqr_multiplier)
    
    is_anomaly = z_anomaly or iqr_anomaly
    combined_score = max(z_score, iqr_score)
    
    methods_flagged = []
    if z_anomaly:
        methods_flagged.append("z-score")
    if iqr_anomaly:
        methods_flagged.append("IQR")
    
    explanation = z_explanation
    if methods_flagged:
        explanation = f"Flagged by {', '.join(methods_flagged)}: {z_explanation}"
    
    return {
        "is_anomaly": is_anomaly,
        "anomaly_score": combined_score,
        "z_score": z_score,
        "iqr_score": iqr_score,
        "method": "z-score+IQR",
        "explanation": explanation,
        "data_sufficient": True,
        "n_samples": len(historical_values)
    }
