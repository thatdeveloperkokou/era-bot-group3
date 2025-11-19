"""
Populate/refresh the region_profiles table using NERC Q2 2025 data.

Usage:
    python backend/region_profiles_seed.py
"""
from __future__ import annotations

from app import app
from database import db, RegionProfile
from region_profiles_data import REGION_PROFILE_SEED_DATA


def upsert_region_profiles():
    with app.app_context():
        for payload in REGION_PROFILE_SEED_DATA:
            profile = RegionProfile.query.get(payload["id"])
            if not profile:
                profile = RegionProfile(id=payload["id"])
            for key, value in payload.items():
                if key == "id":
                    continue
                setattr(profile, key, value)
            db.session.add(profile)
        db.session.commit()
        print(f"✅ Upserted {len(REGION_PROFILE_SEED_DATA)} region profiles")


if __name__ == "__main__":
    upsert_region_profiles()


