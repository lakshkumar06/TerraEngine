"""
Utility functions for crop-to-region matching algorithm.
"""

import re
from typing import List, Dict, Tuple


def parse_ph_range(ph_str: str) -> Tuple[float, float]:
    """Parse pH range string like '6.2–6.8' or '5.0–7.0'."""
    if not ph_str or ph_str.lower() == 'unknown':
        return None, None
    
    # Handle different formats
    ph_str = ph_str.strip()
    
    # Look for range pattern like "6.2–6.8" or "6.2-6.8"
    range_match = re.search(r'(\d+\.?\d*)\s*[–-]\s*(\d+\.?\d*)', ph_str)
    if range_match:
        return float(range_match.group(1)), float(range_match.group(2))
    
    # Look for single value
    single_match = re.search(r'(\d+\.?\d*)', ph_str)
    if single_match:
        value = float(single_match.group(1))
        return value - 0.5, value + 0.5
    
    return None, None


def parse_latitude(lat_str: str) -> float:
    """Parse latitude string like '4.5895°S' or '68°N'."""
    if not lat_str:
        return None
    
    lat_str = lat_str.strip()
    
    # Handle format like "4.5895°S" or "68°N"
    match = re.search(r'(\d+\.?\d*)°\s*([NS])', lat_str)
    if match:
        value = float(match.group(1))
        direction = match.group(2)
        return -value if direction == 'S' else value
    
    # Handle simple numeric format
    numeric_match = re.search(r'(-?\d+\.?\d*)', lat_str)
    if numeric_match:
        return float(numeric_match.group(1))
    
    return None


def match_crop_to_regions(crop, regions: List[Dict], top_n: int = 3) -> List[Dict]:
    """
    Match a crop to regions based on compatibility factors.
    
    Args:
        crop: MarsCrop model instance
        regions: List of MarsRegion model instances
        top_n: Number of top matches to return
    
    Returns:
        List of dictionaries with region name and score
    """
    scores = []
    
    # Parse crop requirements
    crop_ph_min, crop_ph_max = parse_ph_range(crop.preferred_ph_range)
    crop_soil_texture = (crop.terrain_soil_texture or '').lower()
    crop_temp_range = (crop.temperature_range_c or '').lower()
    crop_moisture = (crop.moisture_regime or '').lower()
    
    for region in regions:
        score = 0
        reasons = []
        
        # 1. pH compatibility
        if region.ph and crop_ph_min is not None and crop_ph_max is not None:
            region_ph = parse_latitude(region.ph)  # Reusing parser for simplicity
            if region_ph is None:
                # Try to extract numeric pH value
                ph_match = re.search(r'(\d+\.?\d*)', region.ph)
                if ph_match:
                    region_ph = float(ph_match.group(1))
            
            if region_ph is not None:
                if crop_ph_min <= region_ph <= crop_ph_max:
                    score += 3
                    reasons.append(f"pH compatible ({region_ph:.1f})")
                else:
                    score -= 1
                    reasons.append(f"pH mismatch ({region_ph:.1f})")
        else:
            reasons.append("pH data unavailable")
        
        # 2. Soil texture compatibility
        region_terrain = (region.terrain_type or '').lower()
        if region_terrain and crop_soil_texture:
            # Check for compatible soil types
            if 'loam' in crop_soil_texture and 'loam' in region_terrain:
                score += 2
                reasons.append("Loam soil match")
            elif 'sandy' in crop_soil_texture and 'sandy' in region_terrain:
                score += 2
                reasons.append("Sandy soil match")
            elif 'well-drained' in crop_soil_texture and 'drained' in region_terrain:
                score += 1
                reasons.append("Drainage compatibility")
        
        # 3. Temperature feasibility based on latitude
        region_lat = parse_latitude(region.latitude_deg)
        if region_lat is not None:
            # Equatorial regions (good for most crops)
            if -15 <= region_lat <= 15:
                score += 2
                reasons.append("Equatorial climate")
            # Mid-latitude regions
            elif -40 <= region_lat <= 40:
                score += 1
                reasons.append("Moderate climate")
            # Polar regions (challenging)
            else:
                score -= 1
                reasons.append("Polar climate")
        
        # 4. Perchlorate penalty
        if region.perchlorate_wt_pct:
            try:
                perchlorate = float(region.perchlorate_wt_pct)
                if perchlorate > 0.5:
                    score -= 3
                    reasons.append(f"High perchlorate ({perchlorate}%)")
                elif perchlorate > 0.3:
                    score -= 1
                    reasons.append(f"Moderate perchlorate ({perchlorate}%)")
                else:
                    score += 1
                    reasons.append(f"Low perchlorate ({perchlorate}%)")
            except (ValueError, TypeError):
                reasons.append("Perchlorate data unclear")
        
        # 5. Water availability bonus
        if region.water_release_wt_pct:
            try:
                water = float(region.water_release_wt_pct)
                if water > 1.5:
                    score += 2
                    reasons.append(f"Good water availability ({water}%)")
                elif water > 1.0:
                    score += 1
                    reasons.append(f"Moderate water ({water}%)")
            except (ValueError, TypeError):
                pass
        
        # 6. Special considerations
        region_notes = (region.notes or '').lower()
        if 'ice' in region_notes and 'moisture' in crop_moisture:
            score += 1
            reasons.append("Water ice potential")
        
        if 'dust' in region_notes:
            score -= 1
            reasons.append("Dust challenges")
        
        scores.append({
            'region': region.region,
            'score': score,
            'reasons': reasons,
            'latitude': region_lat,
            'perchlorate': region.perchlorate_wt_pct,
            'ph': region.ph,
            'terrain': region.terrain_type
        })
    
    # Sort by score (descending) and return top_n
    sorted_scores = sorted(scores, key=lambda x: x['score'], reverse=True)
    return sorted_scores[:top_n]
