#!/usr/bin/env python3
"""
Debug specific date query
"""

import json
from PerfectMindSession import PerfectMindSession


def debug_specific_date():
    """Debug specific date query"""
    print("🔍 Debugging Specific Date Query")
    print("=" * 50)

    session = PerfectMindSession()

    # Load court configuration
    with open('court-info.json', 'r') as f:
        courts_config = json.load(f)

    # Get Court 1
    court_1 = next(court for court in courts_config['courts'] if court['court'] == 1)
    facility_id = court_1['facilityId']

    target_date = "2025-10-05"
    print(f"Target date: {target_date}")

    # Get verification token
    if session.get_verification_token(facility_id):
        print("✓ Got verification token")

        # Test different approaches
        print(f"\n--- Testing different approaches ---")

        # Approach 1: Single day query
        print(f"1. Single day query (days_count=1):")
        availability_data = session.check_availability(facility_id, date=target_date, days_count=1)

        if availability_data:
            print(f"  Raw response keys: {list(availability_data.keys())}")
            if 'availabilities' in availability_data:
                days = availability_data['availabilities']
                print(f"  Number of days returned: {len(days)}")

                for i, day in enumerate(days):
                    date_str = day.get('Date', '')
                    print(f"    Day {i+1}: {date_str}")

                    if 'BookingGroups' in day:
                        total_spots = sum(len(group.get('AvailableSpots', [])) for group in day['BookingGroups'])
                        print(f"      Total spots: {total_spots}")

        # Approach 2: Multiple days query
        print(f"\n2. Multiple days query (days_count=7):")
        availability_data = session.check_availability(facility_id, date=target_date, days_count=7)

        if availability_data:
            print(f"  Raw response keys: {list(availability_data.keys())}")
            if 'availabilities' in availability_data:
                days = availability_data['availabilities']
                print(f"  Number of days returned: {len(days)}")

                for i, day in enumerate(days):
                    date_str = day.get('Date', '')
                    print(f"    Day {i+1}: {date_str}")

                    if 'BookingGroups' in day:
                        total_spots = sum(len(group.get('AvailableSpots', [])) for group in day['BookingGroups'])
                        print(f"      Total spots: {total_spots}")

        # Approach 3: Parse and filter
        print(f"\n3. Parse and filter for target date:")
        availability_data = session.check_availability(facility_id, date=target_date, days_count=7)

        if availability_data:
            slots = session.parse_availability_data(availability_data)
            target_slots = [slot for slot in slots if slot['date'] == target_date]

            print(f"  Total parsed slots: {len(slots)}")
            print(f"  Slots for {target_date}: {len(target_slots)}")

            if target_slots:
                for slot in target_slots[:5]:
                    print(f"    - {slot['time']} ({slot['group']})")
            else:
                print(f"    No slots found for {target_date}")

                # Show what dates we do have
                dates = set(slot['date'] for slot in slots)
                print(f"    Available dates: {sorted(dates)}")
    else:
        print("❌ Failed to get verification token")


if __name__ == "__main__":
    debug_specific_date()
