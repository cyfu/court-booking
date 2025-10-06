#!/usr/bin/env python3
"""
Query API for specific date availability
"""

import json
import sys
from PerfectMindSession import PerfectMindSession


def query_specific_date():
    """Query availability for a specific date"""
    print("🏟️  Angus Glen Tennis Centre - Specific Date Query")
    print("=" * 60)

    # Get date from command line argument or use default
    if len(sys.argv) > 1:
        target_date = sys.argv[1]
    else:
        # Default to tomorrow
        from datetime import datetime, timedelta
        import pytz
        toronto_tz = pytz.timezone('America/Toronto')
        tomorrow = datetime.now(toronto_tz) + timedelta(days=1)
        target_date = tomorrow.strftime('%Y-%m-%d')

    print(f"📅 Querying availability for: {target_date}")

    # Initialize session
    session = PerfectMindSession()

    # Load court configuration
    try:
        with open('court-info.json', 'r') as f:
            courts_config = json.load(f)
    except FileNotFoundError:
        print("✗ Error: court-info.json not found!")
        return False
    except json.JSONDecodeError as e:
        print(f"✗ Error parsing court-info.json: {e}")
        return False

    print(f"🏟️  Checking {len(courts_config['courts'])} courts for {target_date}...")

    # Check all courts for the specific date
    results = {}

    for court in courts_config['courts']:
        court_num = court['court']
        facility_id = court['facilityId']

        print(f"\n🏟️  Checking Court {court_num} (ID: {facility_id})")

        # Get verification token
        if session.get_verification_token(facility_id):
            # Check availability for specific date (use days_count=7 as API requires multiple days)
            availability_data = session.check_availability(facility_id, date=target_date, days_count=7)

            if availability_data:
                # Parse the data
                slots = session.parse_availability_data(availability_data)

                # Filter slots for the target date
                target_slots = [slot for slot in slots if slot['date'] == target_date]

                results[court_num] = {
                    'facility_id': facility_id,
                    'slots': target_slots
                }

                print(f"  ✓ Found {len(target_slots)} available slots")

                # Show available slots
                if target_slots:
                    for i, slot in enumerate(target_slots):
                        print(f"    {i+1}. {slot['time']} ({slot['group']}) - {slot['duration']}")
                else:
                    print(f"    No available slots for {target_date}")
            else:
                print(f"  ✗ Failed to get availability data")
                results[court_num] = {
                    'facility_id': facility_id,
                    'slots': []
                }
        else:
            print(f"  ✗ Failed to get verification token")
            results[court_num] = {
                'facility_id': facility_id,
                'slots': []
            }

    # Display summary
    print(f"\n📊 SUMMARY FOR {target_date}:")
    print("-" * 60)

    total_slots = 0
    available_courts = []

    for court_num, data in results.items():
        slots = data['slots']
        total_slots += len(slots)

        if slots:
            available_courts.append(court_num)
            print(f"🏟️  Court {court_num}: {len(slots)} slots")
            for slot in slots[:3]:  # Show first 3
                print(f"    - {slot['time']} ({slot['group']})")
            if len(slots) > 3:
                print(f"    ... and {len(slots) - 3} more")
        else:
            print(f"🏟️  Court {court_num}: No available slots")

    print(f"\n📈 TOTAL:")
    print(f"  Date: {target_date}")
    print(f"  Courts with availability: {len(available_courts)}")
    print(f"  Total available slots: {total_slots}")

    if available_courts:
        print(f"  Available courts: {', '.join(map(str, available_courts))}")

    return total_slots > 0


def main():
    """Main function"""
    try:
        success = query_specific_date()

        if success:
            print("\n✅ Query completed successfully!")
            sys.exit(0)
        else:
            print("\n❌ No available slots found for the specified date!")
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n\n⏹️  Query cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
