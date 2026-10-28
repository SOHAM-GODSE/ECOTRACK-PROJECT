"""Time-series forecasting for water and electricity consumption."""
import numpy as np
from datetime import datetime, timedelta
from typing import Optional


def linear_forecast(values: list[float], dates: list[datetime], forecast_days: int = 7) -> dict:
    """Simple linear regression forecast."""
    if len(values) < 7:
        return {
            "available": False,
            "reason": f"Need at least 7 data points for forecasting (have {len(values)})",
            "forecast": []
        }
    
    n = len(values)
    x = np.arange(n)
    y = np.array(values)
    
    # Linear regression
    x_mean = np.mean(x)
    y_mean = np.mean(y)
    
    numerator = np.sum((x - x_mean) * (y - y_mean))
    denominator = np.sum((x - x_mean) ** 2)
    
    if denominator == 0:
        slope = 0
    else:
        slope = numerator / denominator
    intercept = y_mean - slope * x_mean
    
    # Residuals for confidence interval
    residuals = y - (slope * x + intercept)
    std_residual = np.std(residuals)
    
    # Generate forecast
    last_date = dates[-1] if dates else datetime.utcnow()
    forecast_points = []
    
    for i in range(1, forecast_days + 1):
        future_x = n + i - 1
        predicted = slope * future_x + intercept
        predicted = max(0, predicted)  # non-negative
        
        forecast_points.append({
            "date": (last_date + timedelta(days=i)).isoformat(),
            "predicted": round(float(predicted), 2),
            "lower_bound": round(float(max(0, predicted - 1.96 * std_residual)), 2),
            "upper_bound": round(float(predicted + 1.96 * std_residual), 2)
        })
    
    # Model quality
    y_pred_train = slope * x + intercept
    ss_res = np.sum((y - y_pred_train) ** 2)
    ss_tot = np.sum((y - y_mean) ** 2)
    r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
    
    trend_direction = "increasing" if slope > 0.05 else "decreasing" if slope < -0.05 else "stable"
    
    return {
        "available": True,
        "model": "linear_regression",
        "n_training_points": n,
        "slope": round(float(slope), 4),
        "intercept": round(float(intercept), 4),
        "r_squared": round(float(r_squared), 4),
        "trend": trend_direction,
        "std_residual": round(float(std_residual), 4),
        "forecast": forecast_points,
        "note": f"Linear regression model (R²={r_squared:.3f}). {'Good fit.' if r_squared > 0.7 else 'Moderate fit - use with caution.' if r_squared > 0.4 else 'Poor fit - forecast unreliable.'}"
    }


def compute_baseline_stats(values: list[float]) -> dict:
    """Compute statistical baseline for expected range."""
    if not values:
        return {"available": False}
    arr = np.array(values)
    return {
        "available": True,
        "mean": round(float(np.mean(arr)), 3),
        "median": round(float(np.median(arr)), 3),
        "std": round(float(np.std(arr)), 3),
        "min": round(float(np.min(arr)), 3),
        "max": round(float(np.max(arr)), 3),
        "p25": round(float(np.percentile(arr, 25)), 3),
        "p75": round(float(np.percentile(arr, 75)), 3),
        "expected_range_low": round(float(np.mean(arr) - 2 * np.std(arr)), 3),
        "expected_range_high": round(float(np.mean(arr) + 2 * np.std(arr)), 3),
        "n_samples": len(values)
    }
