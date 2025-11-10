#!/usr/bin/env python3
"""
Court Availability Checker
Checks availability for all 4 tennis courts at Angus Glen Tennis Centre
"""

import json
import os
import random
import sys
import time
import logging
from datetime import datetime, timedelta
from .PerfectMindSession import PerfectMindSession
from .sms_notifier import SMSNotifier
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def format_slot_output(slot, court_num):
    """Format a slot as: date (Day) start_time-end_time court X"""
    date = slot.get('date', '')
    start_time = slot.get('time', '')
    duration_str = slot.get('duration', '0min')

    # Get weekday abbreviation (3 characters)
    weekday_abbr = ''
    try:
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        weekday_abbr = date_obj.strftime('%a')  # Mon, Tue, Wed, etc.
    except (ValueError, TypeError):
        weekday_abbr = ''

    # Extract minutes from duration string (e.g., "60min" -> 60)
    try:
        duration_minutes = int(duration_str.replace('min', ''))
    except (ValueError, AttributeError):
        duration_minutes = 60  # Default to 60 minutes

    # Calculate end time
    try:
        start_dt = datetime.strptime(start_time, '%H:%M')
        end_dt = start_dt + timedelta(minutes=duration_minutes)
        end_time = end_dt.strftime('%H:%M')
    except ValueError:
        # If time parsing fails, just use start_time
        end_time = start_time

    if weekday_abbr:
        return f"{date} {weekday_abbr} {start_time}-{end_time} court {court_num}"
    else:
        return f"{date} {start_time}-{end_time} court {court_num}"


def get_slot_key(slot: dict) -> str:
    """
    Generate a unique key for a slot

    Args:
        slot: Slot dictionary with 'date', 'time', and 'court' keys

    Returns:
        Unique key string
    """
    return f"{slot['date']}|{slot['time']}|{slot['court']}"


def find_new_slots(current_slots: list, previous_slot_keys: set) -> list:
    """
    Find new slots that were not in the previous check

    Args:
        current_slots: List of current slot dictionaries
        previous_slot_keys: Set of previous slot keys

    Returns:
        List of new slot dictionaries
    """
    new_slots = []
    for slot in current_slots:
        slot_key = get_slot_key(slot)
        if slot_key not in previous_slot_keys:
            new_slots.append(slot)
    return new_slots


def check_court_availability():
    """
    Check availability for all courts

    Returns:
        Tuple of (success: bool, slots: list)
    """
    # Initialize session with logger
    logger = logging.getLogger(__name__)
    session = PerfectMindSession(logger=logger)

    # Load court configuration
    try:
        with open('court-info.json', 'r') as f:
            courts_config = json.load(f)
    except FileNotFoundError:
        logger.error("Error: court-info.json not found!")
        return False, []
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing court-info.json: {e}")
        return False, []

    # Check all courts
    results = session.check_all_courts(courts_config)

    # Collect all available slots
    all_slots = []

    for court_num, data in results.items():
        if data['availability']:
            # Parse availability data
            slots = session.parse_availability_data(data['availability'])

            if slots:
                # Format each slot and add court number
                for slot in slots:
                    formatted = format_slot_output(slot, court_num)
                    all_slots.append({
                        'formatted': formatted,
                        'date': slot.get('date', ''),
                        'time': slot.get('time', ''),
                        'court': court_num
                    })

    # Sort by date and time
    all_slots.sort(key=lambda x: (x['date'], x['time'], x['court']))

    # Display results header
    print("\n📊 Angus Glen Tennis Court Availability:")
    print("-" * 60)

    # Display formatted output
    for slot in all_slots:
        print(slot['formatted'])

    return len(all_slots) > 0, all_slots


def is_quiet_hours(now: datetime) -> bool:
    """
    Check if current time is within quiet hours (22:30 PM - 07:30 AM)

    Args:
        now: Current datetime

    Returns:
        True if within quiet hours, False otherwise
    """
    current_time = now.time()
    quiet_start = datetime.strptime("22:30", "%H:%M").time()
    quiet_end = datetime.strptime("07:30", "%H:%M").time()

    # Quiet hours span midnight
    if current_time >= quiet_start or current_time < quiet_end:
        return True
    return False


def get_next_check_time(now: datetime, check_interval_minutes: int) -> datetime:
    """
    Calculate next check time based on:
    1. Ensure execution at :30:01 of each hour
    2. Respect check interval
    3. Skip quiet hours (22:30 - 07:30)

    Args:
        now: Current datetime
        check_interval_minutes: Check interval in minutes

    Returns:
        Next check datetime
    """
    # If in quiet hours, wait until 07:30:01
    if is_quiet_hours(now):
        next_check = now.replace(hour=7, minute=30, second=1, microsecond=0)
        # If already past 07:30 today, move to tomorrow
        if next_check <= now:
            next_check += timedelta(days=1)
        return next_check

    # Calculate next :30:01
    next_30_01 = now.replace(minute=30, second=1, microsecond=0)
    if next_30_01 <= now:
        # Already past :30:01 this hour, move to next hour
        next_30_01 += timedelta(hours=1)

    # Calculate next check based on interval
    next_interval = now + timedelta(minutes=check_interval_minutes)

    # Use the earlier of the two
    next_check = min(next_30_01, next_interval)

    # If next check falls in quiet hours, move to 07:30:01 next day
    if is_quiet_hours(next_check):
        next_check = next_check.replace(hour=7, minute=30, second=1, microsecond=0)
        if next_check <= now:
            next_check += timedelta(days=1)

    return next_check


def main():
    """Main function"""
    logger = logging.getLogger(__name__)

    # Get check interval from environment variable
    # If not set, use a random value between 10-30 minutes
    check_interval_str = os.getenv('CHECK_INTERVAL_MINUTES')
    if check_interval_str:
        check_interval_minutes = int(check_interval_str)
    else:
        check_interval_minutes = random.randint(10, 30)
        logger.info(f"CHECK_INTERVAL_MINUTES not set, using random value: {check_interval_minutes} minutes")
    logger.info(f"Check interval set to {check_interval_minutes} minutes")

    # Keep previous slots in memory for comparison
    previous_slot_keys = set()

    while True:
        try:
            now = datetime.now()

            # Skip check if in quiet hours
            if is_quiet_hours(now):
                next_check = get_next_check_time(now, check_interval_minutes)
                wait_seconds = (next_check - now).total_seconds()
                logger.info(
                    f"Quiet hours (22:30-07:30). Next check at {next_check.strftime('%Y-%m-%d %H:%M:%S')}"
                )
                time.sleep(wait_seconds)
                continue

            # Perform check
            logger.info(f"Checking court availability at {now.strftime('%Y-%m-%d %H:%M:%S')}")
            success, current_slots = check_court_availability()

            if success:
                print("\n✅ Availability check completed successfully!")
            else:
                print("\n❌ No courts available or check failed!")

            # Compare with previous slots to find new ones
            new_slots = find_new_slots(current_slots, previous_slot_keys)

            # Update previous slots in memory
            previous_slot_keys = {get_slot_key(slot) for slot in current_slots}

            # Send SMS notification only if there are new slots
            if new_slots:
                logger.info(f"Found {len(new_slots)} new slot(s), sending SMS notification...")
                sms_notifier = SMSNotifier(logger=logger)
                if sms_notifier.is_configured():
                    sms_sent = sms_notifier.send_availability_notification(current_slots)
                    if sms_sent:
                        print(f"\n📱 SMS notification sent for {len(current_slots)} time slot(s)!")
                    else:
                        print("\n⚠️  Failed to send SMS notification")
                else:
                    logger.info("SMS notifier not configured, skipping SMS notification")
            else:
                if current_slots:
                    logger.info(f"No new slots found ({len(current_slots)} existing slots)")
                else:
                    logger.info("No available slots found")

            # Calculate next check time
            next_check = get_next_check_time(datetime.now(), check_interval_minutes)
            wait_seconds = (next_check - datetime.now()).total_seconds()

            if wait_seconds > 0:
                logger.info(
                    f"Next check scheduled at {next_check.strftime('%Y-%m-%d %H:%M:%S')} "
                    f"(in {wait_seconds:.0f} seconds)"
                )
                time.sleep(wait_seconds)
            else:
                # If wait time is negative or zero, wait at least 1 second
                time.sleep(1)

        except KeyboardInterrupt:
            print("\n\n⏹️  Check cancelled by user")
            sys.exit(1)
        except Exception as e:
            logger.error(f"Unexpected error: {e}", exc_info=True)
            # Wait a bit before retrying on error
            time.sleep(60)


if __name__ == "__main__":
    main()
