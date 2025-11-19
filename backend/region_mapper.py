"""
Utility helpers to map free-form user locations to DisCo/region IDs.
"""
from __future__ import annotations

from typing import Optional, List, Tuple

from region_profiles_data import REGION_PROFILE_SEED_DATA


def _build_lookup_table() -> List[Tuple[str, str]]:
    lookups: List[Tuple[str, str]] = []
    for region in REGION_PROFILE_SEED_DATA:
        region_id = region["id"]
        for keyword in region.get("keywords", []):
            lookups.append((keyword.lower(), region_id))
        for state in region.get("states", []):
            lookups.append((state.lower(), region_id))
    # sort by length descending to match more specific keywords first
    lookups.sort(key=lambda item: len(item[0]), reverse=True)
    return lookups


LOOKUP_TABLE = _build_lookup_table()


def infer_region_from_location(location: Optional[str]) -> Optional[str]:
    """
    Very lightweight heuristic to match a user's saved address to a region profile.
    Returns the region_id string (e.g., "ikeja") or None when no match exists.
    """
    if not location:
        return None
    location_lower = location.lower()
    for keyword, region_id in LOOKUP_TABLE:
        if keyword in location_lower:
            return region_id
    return None


