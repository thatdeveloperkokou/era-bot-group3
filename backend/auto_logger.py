"""
Autonomous power logging service.

Run periodically (e.g., hourly) to ensure each user's region is synced with
the expected ON/OFF state derived from NERC Q2 templates.
"""
from __future__ import annotations

import argparse
from datetime import datetime, time
from typing import List, Dict

from app import app
from database import db, User, PowerLog, RegionProfile


def _parse_time(value: str) -> time:
    hour, minute = value.split(":")
    return time(int(hour), int(minute))


def is_within_block(block: Dict[str, str], now_time: time) -> bool:
    start = _parse_time(block["start"])
    end = _parse_time(block["end"])
    if start <= end:
        return start <= now_time < end
    # Block wraps past midnight
    return now_time >= start or now_time < end


def region_should_be_on(region: RegionProfile, now_time: time) -> bool:
    template = region.schedule_template or []
    for block in template:
        if is_within_block(block, now_time):
            return True
    return False


def sync_region(region: RegionProfile, now: datetime, dry_run: bool = False) -> int:
    """Ensure every user assigned to the region has the expected ON/OFF event."""
    desired_status_on = region_should_be_on(region, now.time())
    desired_event = "on" if desired_status_on else "off"
    updated = 0
    users: List[User] = User.query.filter_by(region_id=region.id).all()
    if not users:
        return 0

    for user in users:
        last_log = (
            PowerLog.query.filter_by(user_id=user.username)
            .order_by(PowerLog.timestamp.desc())
            .first()
        )
        if last_log and last_log.event_type == desired_event:
            continue
        if dry_run:
            updated += 1
            continue
        log_entry = PowerLog(
            user_id=user.username,
            event_type=desired_event,
            timestamp=now,
            date=now.date(),
            location=user.location,
            region_id=region.id,
            auto_generated=True,
        )
        db.session.add(log_entry)
        updated += 1

    if not dry_run and updated:
        db.session.commit()
    return updated


def run_auto_logger(dry_run: bool = False) -> None:
    now = datetime.utcnow()
    with app.app_context():
        regions: List[RegionProfile] = RegionProfile.query.order_by(RegionProfile.id).all()
        total = 0
        for region in regions:
            total += sync_region(region, now, dry_run=dry_run)
        suffix = " (dry-run)" if dry_run else ""
        print(f"Auto logger processed {len(regions)} regions and queued {total} events{suffix}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Autonomous power logging cron helper")
    parser.add_argument("--dry-run", action="store_true", help="Simulate without inserting rows")
    args = parser.parse_args()
    run_auto_logger(dry_run=args.dry_run)


