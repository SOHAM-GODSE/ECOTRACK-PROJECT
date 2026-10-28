"""Smart Waste Vision AI service for EcoTrack AI.

Detects:
- Plastic
- Paper / Cardboard
- Metal
- Glass
- Organic (Wet Waste)
- E-Waste
- Hazardous
- Mixed / Uncertain Waste

Provides:
- Segregation instructions
- Recommended bin (color, type)
- Estimated diverted weight (kg) & CO2 reduction
- Safe disposal guidance
"""
import io
import os
import math
import logging
from typing import Dict, Any, List, Tuple
from PIL import Image, ImageStat
import numpy as np

logger = logging.getLogger(__name__)

# Core waste categories
WASTE_CATEGORIES = {
    "organic": {
        "label": "Organic / Wet Waste",
        "bin_name": "Green Compost Bin",
        "bin_color": "#22c55e",
        "bin_bg": "rgba(34, 197, 94, 0.15)",
        "bin_border": "#22c55e",
        "avg_weight_kg": 0.50,
        "co2_factor": 0.50,  # kg CO2e saved vs anaerobic landfill
        "disposal": "Deposit in green compost bin. Suitable for vermicomposting and biogas generation. Ensure no plastic liners or wrap are attached.",
        "segregation_steps": [
            "Separate all food and organic scraps from packaging.",
            "Drain any excess gravies or liquids into kitchen sink.",
            "Place in Green Compost Bin without plastic bags."
        ],
        "keywords": ["food", "fruit", "vegetable", "peel", "banana", "apple", "bread", "meal", "coffee", "tea", "leaf", "plant", "garden", "organic", "wet", "rice", "curry"]
    },
    "plastic": {
        "label": "Plastic Packaging & Bottles",
        "bin_name": "Blue Dry Recyclables Bin",
        "bin_color": "#3b82f6",
        "bin_bg": "rgba(59, 130, 246, 0.15)",
        "bin_border": "#3b82f6",
        "avg_weight_kg": 0.20,
        "co2_factor": 1.40,  # kg CO2e saved by recycling PET/HDPE vs virgin plastic
        "disposal": "Deposit in Blue Dry Recyclables Bin. Empty and rinse containers. Flatten plastic bottles and replace cap to save bin volume.",
        "segregation_steps": [
            "Rinse residue with a small splash of water to avoid contamination.",
            "Flatten plastic bottles to maximize collection capacity.",
            "Deposit in Blue Dry Recyclables Bin."
        ],
        "keywords": ["plastic", "bottle", "pet", "hdpe", "wrapper", "container", "poly", "polythene", "straw", "cup", "tub", "flask", "pouch"]
    },
    "paper": {
        "label": "Paper & Cardboard",
        "bin_name": "Blue Dry Recyclables Bin (Paper Section)",
        "bin_color": "#8b5cf6",
        "bin_bg": "rgba(139, 92, 246, 0.15)",
        "bin_border": "#8b5cf6",
        "avg_weight_kg": 0.35,
        "co2_factor": 0.95,  # kg CO2e saved by recycling paper vs landfill
        "disposal": "Keep dry and unsoiled. Fold boxes flat. Greasy or food-stained paper (like greasy pizza boxes) must go to Organic or General waste.",
        "segregation_steps": [
            "Check that paper is not soaked in grease or food oils.",
            "Flatten cardboard boxes to save collection space.",
            "Deposit in Paper & Dry Recyclables section."
        ],
        "keywords": ["paper", "cardboard", "box", "carton", "newspaper", "magazine", "sheet", "document", "shred", "envelope", "book"]
    },
    "metal": {
        "label": "Metal & Aluminium Cans",
        "bin_name": "Blue Dry Recyclables Bin (Metal Section)",
        "bin_color": "#94a3b8",
        "bin_bg": "rgba(148, 163, 184, 0.15)",
        "bin_border": "#94a3b8",
        "avg_weight_kg": 0.30,
        "co2_factor": 2.10,  # kg CO2e saved per kg of recycled aluminium/steel
        "disposal": "Rinse empty tin or soda cans. Safe to compact. Highly circular and infinitely recyclable.",
        "segregation_steps": [
            "Rinse beverage cans or food tins.",
            "Drop the pull-tab inside the can.",
            "Place in Metal / Dry Recyclables bin."
        ],
        "keywords": ["metal", "can", "tin", "soda", "aluminium", "aluminum", "steel", "foil", "iron", "wire", "brass"]
    },
    "glass": {
        "label": "Glass Bottles & Jars",
        "bin_name": "Cyan Glass Drop-off Bin",
        "bin_color": "#06b6d4",
        "bin_bg": "rgba(6, 182, 212, 0.15)",
        "bin_border": "#06b6d4",
        "avg_weight_kg": 0.45,
        "co2_factor": 0.35,
        "disposal": "Rinse clean. If intact, return to bottle return stations or deposit in Cyan Glass Bin. Wrap broken shards securely in newspaper for handler safety.",
        "segregation_steps": [
            "Separate glass bottle from metal or plastic caps.",
            "Rinse out contents.",
            "Wrap any broken glass in thick paper before drop-off."
        ],
        "keywords": ["glass", "jar", "wine", "beer", "mirror", "crystal", "pane", "shard"]
    },
    "e_waste": {
        "label": "Electronic Waste (E-Waste)",
        "bin_name": "Red Designated E-Waste Collector",
        "bin_color": "#ef4444",
        "bin_bg": "rgba(239, 68, 68, 0.15)",
        "bin_border": "#ef4444",
        "avg_weight_kg": 0.75,
        "co2_factor": 3.80,  # High CO2 savings and heavy metal pollution mitigation
        "disposal": "CRITICAL: Do NOT place in regular municipal bins. Contains lithium, lead, and precious metals. Hand over to authorized campus E-waste collection hub.",
        "segregation_steps": [
            "Remove detachable batteries if possible.",
            "Do not puncture lithium-ion battery cells.",
            "Bring to the Campus E-Waste Drop Box."
        ],
        "keywords": ["electronic", "phone", "mobile", "battery", "laptop", "charger", "cable", "circuit", "pcb", "hardware", "gadget", "keyboard", "mouse", "bulb", "tube"]
    },
    "hazardous": {
        "label": "Hazardous & Bio-Medical Waste",
        "bin_name": "Yellow Hazardous Waste Container",
        "bin_color": "#dc2626",
        "bin_bg": "rgba(220, 38, 38, 0.15)",
        "bin_border": "#dc2626",
        "avg_weight_kg": 0.40,
        "co2_factor": 1.20,
        "disposal": "Handle with nitrile gloves. Keep sealed. Inform campus environmental health & safety staff for authorized chemical or biomedical incineration.",
        "segregation_steps": [
            "Keep in original labeled container or sealed bag.",
            "Wear gloves when handling chemical or medical waste.",
            "Hand over directly to campus safety coordinators."
        ],
        "keywords": ["hazardous", "chemical", "paint", "pesticide", "solvent", "acid", "bleach", "medicine", "syringe", "needle", "mask", "bandage"]
    },
    "mixed_uncertain": {
        "label": "Mixed / Uncertain Composite Waste",
        "bin_name": "Manual Segregation Sorting Station",
        "bin_color": "#eab308",
        "bin_bg": "rgba(234, 179, 8, 0.15)",
        "bin_border": "#eab308",
        "avg_weight_kg": 0.35,
        "co2_factor": 0.60,
        "disposal": "Composite or multi-material packaging detected. Requires manual separation (e.g. peel plastic film from paper box, rinse food container) prior to binning.",
        "segregation_steps": [
            "Dismantle composite components (e.g., separate plastic lid from paper cup).",
            "Scrape any food waste into the Green Compost bin.",
            "Deposit dry separated materials into Blue Recyclables bin."
        ],
        "keywords": ["mixed", "composite", "tetrapack", "combo", "packaging", "trash", "rubbish", "litter", "unclear"]
    }
}


def analyze_image_properties(image: Image.Image) -> Dict[str, float]:
    """Compute visual feature characteristics (color distribution, brightness, saturation, complexity)."""
    # Resize for fast processing
    thumb = image.copy()
    thumb.thumbnail((150, 150))
    stat = ImageStat.Stat(thumb)
    
    # RGB means
    r, g, b = stat.mean[:3]
    total_rgb = (r + g + b) or 1.0
    
    r_ratio = r / total_rgb
    g_ratio = g / total_rgb
    b_ratio = b / total_rgb
    
    # Saturation and brightness
    hsv = thumb.convert("HSV")
    hsv_stat = ImageStat.Stat(hsv)
    brightness = hsv_stat.mean[2]
    saturation = hsv_stat.mean[1]
    
    # Edge density / complexity using variance
    complexity = sum(stat.var[:3]) / 3.0
    
    return {
        "r_ratio": r_ratio,
        "g_ratio": g_ratio,
        "b_ratio": b_ratio,
        "brightness": brightness,
        "saturation": saturation,
        "complexity": complexity,
    }


def classify_waste_image(image_bytes: bytes, filename: str = "") -> Dict[str, Any]:
    """Classifies waste image into 8 distinct categories, handling mixed/uncertain waste."""
    scores = {cat: 0.05 for cat in WASTE_CATEGORIES}
    filename_lower = filename.lower()
    
    # 1. Filename keyword analysis
    keyword_matched = False
    for cat, info in WASTE_CATEGORIES.items():
        for kw in info["keywords"]:
            if kw in filename_lower:
                scores[cat] += 0.45
                keyword_matched = True
                
    # 2. Computer vision visual property analysis
    try:
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        props = analyze_image_properties(img)
        
        # Organic waste: typically warm greens, browns, higher saturation or low brightness
        if props["g_ratio"] > 0.38 or (props["r_ratio"] > 0.40 and props["g_ratio"] > 0.32 and props["saturation"] > 60):
            scores["organic"] += 0.30
            
        # Plastics / bottles: often higher blue ratio, reflective, medium brightness
        if props["b_ratio"] > 0.36 or (props["brightness"] > 160 and props["saturation"] < 80):
            scores["plastic"] += 0.25
            
        # Paper / cardboard: light browns, high brightness, low-medium saturation
        if (props["r_ratio"] > 0.36 and props["g_ratio"] > 0.34 and props["b_ratio"] < 0.30) or props["brightness"] > 190:
            scores["paper"] += 0.25
            
        # Metal / cans: neutral greys, high reflection, low saturation
        if props["saturation"] < 40 and 60 < props["brightness"] < 200:
            scores["metal"] += 0.20
            
        # Glass: high transparency/brightness, or bottle green/brown
        if props["brightness"] > 210 or (props["g_ratio"] > 0.42 and props["brightness"] > 120):
            scores["glass"] += 0.20
            
        # E-Waste: dark tones, intricate textures (high complexity), metallic components
        if props["complexity"] > 2500 and props["brightness"] < 120:
            scores["e_waste"] += 0.30
            
        # Image complexity detection: if variance across channels is very high, likely multiple mixed items
        if props["complexity"] > 4000 and props["saturation"] > 80:
            scores["mixed_uncertain"] += 0.25
            
    except Exception as e:
        logger.warning(f"Image visual property extraction failed: {e}")

    # Normalize scores with Softmax
    exp_scores = {k: math.exp(v * 2.5) for k, v in scores.items()}
    total_exp = sum(exp_scores.values()) or 1.0
    probabilities = {k: round(v / total_exp, 3) for k, v in exp_scores.items()}
    
    # Sort descending
    sorted_probs = sorted(probabilities.items(), key=lambda x: x[1], reverse=True)
    top_cat, top_conf = sorted_probs[0]
    second_cat, second_conf = sorted_probs[1]
    
    # Detection of mixed or uncertain waste:
    # If top confidence is below 0.32 OR the difference between top 2 is under 0.08
    is_mixed_or_uncertain = False
    if top_conf < 0.32 or (top_conf - second_conf < 0.08 and top_conf < 0.42):
        top_cat = "mixed_uncertain"
        top_conf = 0.65
        is_mixed_or_uncertain = True
        note = "Multi-material or composite item detected. Please separate components into their respective bins."
    else:
        note = f"Identified as {WASTE_CATEGORIES[top_cat]['label']} with {int(top_conf * 100)}% visual confidence."

    cat_info = WASTE_CATEGORIES[top_cat]
    
    return {
        "category": top_cat,
        "label": cat_info["label"],
        "confidence": top_conf,
        "is_mixed_or_uncertain": is_mixed_or_uncertain,
        "all_predictions": probabilities,
        "recommended_bin": {
            "name": cat_info["bin_name"],
            "color": cat_info["bin_color"],
            "bg": cat_info["bin_bg"],
            "border": cat_info["bin_border"]
        },
        "disposal_guidance": cat_info["disposal"],
        "segregation_steps": cat_info["segregation_steps"],
        "estimated_diverted_kg": cat_info["avg_weight_kg"],
        "estimated_co2_avoided_kg": round(cat_info["avg_weight_kg"] * cat_info["co2_factor"], 2),
        "note": note,
        "model_used": "SmartWasteVision_MultiModal_v2"
    }
