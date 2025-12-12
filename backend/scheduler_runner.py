#!/usr/bin/env python3
"""
Scheduler runner for auto_logger.py

This script runs continuously and executes auto_logger.py every hour.
It can be used as a cloud platform service start command to keep the scheduler running.
Note: On Render, use the Cron Job service instead (see render.yaml).
"""
from __future__ import annotations

import argparse
import sys
import time
import traceback
from datetime import datetime
from typing import Optional

# Import the auto_logger function directly
from auto_logger import run_auto_logger


def run_scheduler(
    interval_seconds: int = 3600,
    dry_run: bool = False,
    initial_delay: int = 0,
    max_iterations: Optional[int] = None,
) -> None:
    """
    Run the auto logger on a schedule.

    Args:
        interval_seconds: Time between executions in seconds (default: 3600 = 1 hour)
        dry_run: If True, run in dry-run mode (simulate without inserting rows)
        initial_delay: Delay before first execution in seconds (default: 0)
        max_iterations: Maximum number of iterations (None = infinite)
    """
    suffix = " (dry-run)" if dry_run else ""
    print(f"🕐 Scheduler started{suffix}")
    print(f"   Interval: {interval_seconds} seconds ({interval_seconds / 3600:.1f} hours)")
    if initial_delay > 0:
        print(f"   Initial delay: {initial_delay} seconds")
    if max_iterations:
        print(f"   Max iterations: {max_iterations}")
    else:
        print("   Running indefinitely...")
    print()

    iteration = 0

    # Initial delay if specified
    if initial_delay > 0:
        print(f"⏳ Waiting {initial_delay} seconds before first execution...")
        time.sleep(initial_delay)

    while True:
        iteration += 1
        execution_time = datetime.utcnow()

        try:
            print(f"[{execution_time.strftime('%Y-%m-%d %H:%M:%S')} UTC] "
                  f"Starting auto logger execution #{iteration}{suffix}")
            
            # Run the auto logger
            run_auto_logger(dry_run=dry_run)
            
            print(f"[{execution_time.strftime('%Y-%m-%d %H:%M:%S')} UTC] "
                  f"✅ Auto logger execution #{iteration} completed successfully")
            
        except KeyboardInterrupt:
            print("\n⚠️  Received interrupt signal. Shutting down scheduler...")
            break
        except Exception as e:
            print(f"[{execution_time.strftime('%Y-%m-%d %H:%M:%S')} UTC] "
                  f"❌ Error during auto logger execution #{iteration}: {str(e)}")
            traceback.print_exc()
            # Continue running even if there's an error
            print("   Continuing scheduler...")

        # Check if we've reached max iterations
        if max_iterations and iteration >= max_iterations:
            print(f"\n✅ Reached maximum iterations ({max_iterations}). Stopping scheduler.")
            break

        # Wait for the next execution
        if iteration < max_iterations if max_iterations else True:
            next_execution = execution_time.timestamp() + interval_seconds
            next_time = datetime.fromtimestamp(next_execution)
            print(f"⏰ Next execution scheduled for: {next_time.strftime('%Y-%m-%d %H:%M:%S')} UTC")
            print(f"   Sleeping for {interval_seconds} seconds...\n")
            time.sleep(interval_seconds)

    print("👋 Scheduler stopped.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Scheduler runner for auto_logger.py - runs continuously and executes every hour"
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=3600,
        help="Interval between executions in seconds (default: 3600 = 1 hour)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run in dry-run mode (simulate without inserting rows)",
    )
    parser.add_argument(
        "--initial-delay",
        type=int,
        default=0,
        help="Delay before first execution in seconds (default: 0)",
    )
    parser.add_argument(
        "--max-iterations",
        type=int,
        default=None,
        help="Maximum number of iterations (default: None = infinite)",
    )

    args = parser.parse_args()

    try:
        run_scheduler(
            interval_seconds=args.interval,
            dry_run=args.dry_run,
            initial_delay=args.initial_delay,
            max_iterations=args.max_iterations,
        )
    except KeyboardInterrupt:
        print("\n👋 Scheduler interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Fatal error: {str(e)}")
        traceback.print_exc()
        sys.exit(1)

