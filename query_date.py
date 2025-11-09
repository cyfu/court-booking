#!/usr/bin/env python3
"""
Simple script to query availability for a specific date
Usage: python query_date.py YYYY-MM-DD
Example: python query_date.py 2025-10-07
"""

import sys
from PerfectMindSession import PerfectMindSession
import json


def query_date(date_str):
    """Query availability for a specific date"""
    print(f"🏟️  Querying availability for: {date_str}")
    print("=" * 50)

    session = PerfectMindSession()

    # Load court configuration
    with open('court-info.json', 'r') as f:
        courts_config = json.load(f)

    # Get Court 1 for testing
    court_1 = next(court for court in courts_config['courts'] if court['court'] == 1)
    facility_id = court_1['facilityId']

    # Get verification token
    if session.get_verification_token(facility_id):
        # Check availability (API always returns 7 days from current date)
        availability_data = session.check_availability(facility_id, days_count=7)

        if availability_data:
            # Parse the data
            slots = session.parse_availability_data(availability_data)

            # Filter slots for the target date
            target_slots = [slot for slot in slots if slot['date'] == date_str]

            print(f"📅 Available slots for {date_str}:")

            if target_slots:
                for i, slot in enumerate(target_slots):
                    print(f"  {i+1}. {slot['time']} ({slot['group']}) - {slot['duration']}")
                print(f"\n✅ Found {len(target_slots)} available slots")
            else:
                print(f"  No available slots found for {date_str}")

                # Show what dates are available
                dates = set(slot['date'] for slot in slots)
                print(f"\n📅 Available dates: {', '.join(sorted(dates))}")
        else:
            print("❌ Failed to get availability data")
    else:
        print("❌ Failed to get verification token")


def main():
    """Main function"""
    if len(sys.argv) != 2:
        print("Usage: python query_date.py YYYY-MM-DD")
        print("Example: python query_date.py 2025-10-07")
        sys.exit(1)

    date_str = sys.argv[1]

    # Validate date format
    try:
        from datetime import datetime
        datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        print("❌ Invalid date format. Use YYYY-MM-DD")
        sys.exit(1)

    query_date(date_str)


if __name__ == "__main__":
    main()
