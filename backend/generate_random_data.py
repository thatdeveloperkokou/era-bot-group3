"""
Random data generator for power logs.

Generates random power on/off events for users to populate the database with sample data.
"""
from __future__ import annotations

import random
from datetime import datetime, timedelta
from typing import List

from app import app
from database import db, User, PowerLog


def generate_random_power_logs(
    days_back: int = 7,
    min_events_per_day: int = 2,
    max_events_per_day: int = 8,
    dry_run: bool = False
) -> int:
    """
    Generate random power logs for all users.
    
    Args:
        days_back: Number of days to generate data for (default: 7)
        min_events_per_day: Minimum events per day (default: 2)
        max_events_per_day: Maximum events per day (default: 8)
        dry_run: If True, simulate without inserting rows
    
    Returns:
        Number of logs generated
    """
    now = datetime.utcnow()
    total_generated = 0
    
    with app.app_context():
        users: List[User] = User.query.all()
        
        if not users:
            print("⚠️  No users found. Create users first.")
            return 0
        
        print(f"🔄 Generating random power logs for {len(users)} users...")
        print(f"   Days: {days_back}, Events per day: {min_events_per_day}-{max_events_per_day}")
        
        for user in users:
            # Get the last log for this user to determine starting state
            last_log = (
                PowerLog.query.filter_by(user_id=user.username)
                .order_by(PowerLog.timestamp.desc())
                .first()
            )
            
            # Start with random state if no previous logs
            current_state = "on" if not last_log else last_log.event_type
            if not last_log:
                # Randomly choose initial state
                current_state = random.choice(["on", "off"])
            
            # Generate logs for the past N days
            for day_offset in range(days_back, -1, -1):
                target_date = (now - timedelta(days=day_offset)).date()
                
                # Skip if we already have logs for this date
                existing_logs = PowerLog.query.filter_by(
                    user_id=user.username,
                    date=target_date
                ).count()
                
                if existing_logs > 0 and day_offset < days_back:
                    # Already have logs for this date, skip
                    continue
                
                # Random number of events for this day
                num_events = random.randint(min_events_per_day, max_events_per_day)
                
                # Generate events throughout the day
                for event_num in range(num_events):
                    # Random time during the day (between 6 AM and 11 PM)
                    hour = random.randint(6, 23)
                    minute = random.randint(0, 59)
                    
                    timestamp = datetime.combine(target_date, datetime.min.time().replace(hour=hour, minute=minute))
                    
                    # Toggle state for each event
                    current_state = "off" if current_state == "on" else "on"
                    
                    # Check if this exact log already exists
                    existing = PowerLog.query.filter_by(
                        user_id=user.username,
                        event_type=current_state,
                        timestamp=timestamp
                    ).first()
                    
                    if existing:
                        continue
                    
                    if not dry_run:
                        log_entry = PowerLog(
                            user_id=user.username,
                            event_type=current_state,
                            timestamp=timestamp,
                            date=target_date,
                            location=user.location,
                            region_id=user.region_id,
                            auto_generated=True,
                        )
                        db.session.add(log_entry)
                    
                    total_generated += 1
        
        if not dry_run and total_generated > 0:
            db.session.commit()
        
        suffix = " (dry-run)" if dry_run else ""
        print(f"✅ Generated {total_generated} random power log events{suffix}")
        return total_generated


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate random power logs for all users")
    parser.add_argument(
        "--days",
        type=int,
        default=7,
        help="Number of days to generate data for (default: 7)"
    )
    parser.add_argument(
        "--min-events",
        type=int,
        default=2,
        help="Minimum events per day (default: 2)"
    )
    parser.add_argument(
        "--max-events",
        type=int,
        default=8,
        help="Maximum events per day (default: 8)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate without inserting rows"
    )
    
    args = parser.parse_args()
    
    generate_random_power_logs(
        days_back=args.days,
        min_events_per_day=args.min_events,
        max_events_per_day=args.max_events,
        dry_run=args.dry_run
    )

