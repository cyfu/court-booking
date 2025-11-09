#!/usr/bin/env python3
"""
Court Availability Checker
Checks availability for all 4 tennis courts at Angus Glen Tennis Centre
"""

import json
import sys
import logging
from datetime import datetime, timedelta
from PerfectMindSession import PerfectMindSession

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


def check_court_availability():
    """Check availability for all courts"""
    # Initialize session with logger
    logger = logging.getLogger(__name__)
    session = PerfectMindSession(logger=logger)

    # Load court configuration
    try:
        with open('court-info.json', 'r') as f:
            courts_config = json.load(f)
    except FileNotFoundError:
        logger.error("Error: court-info.json not found!")
        return False
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing court-info.json: {e}")
        return False

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

    return len(all_slots) > 0


def main():
    """Main function"""
    try:
        success = check_court_availability()

        if success:
            print("\n✅ Availability check completed successfully!")
        else:
            print("\n❌ No courts available or check failed!")

        sys.exit(0 if success else 1)

    except KeyboardInterrupt:
        print("\n\n⏹️  Check cancelled by user")
        sys.exit(1)
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
