"""Unit conversion utilities for EcoTrack AI."""

WATER_CONVERSION = {
    "liters": 1.0,
    "cubic_meters": 1000.0,  # 1 m3 = 1000 L
    "gallons": 3.78541,      # 1 gallon = 3.78541 L
    "kiloliters": 1000.0,
}


def convert_water_to_liters(value: float, unit: str) -> float:
    factor = WATER_CONVERSION.get(unit.lower(), 1.0)
    return value * factor


def convert_liters_to_unit(liters: float, unit: str) -> float:
    factor = WATER_CONVERSION.get(unit.lower(), 1.0)
    return liters / factor


def normalize_water_consumption(current: float, previous: float, unit: str) -> float | None:
    """Calculate consumption from cumulative readings. Returns None if invalid."""
    if current < previous:
        return None  # possible meter reset or invalid reading
    c_liters = convert_water_to_liters(current, unit)
    p_liters = convert_water_to_liters(previous, unit)
    return c_liters - p_liters
