#!/usr/bin/env python3
"""
Court Availability Checker
Checks availability for all 4 tennis courts at Angus Glen Tennis Centre
"""

import json
import sys
from PerfectMindSession import PerfectMindSession


def check_court_availability():
    """Check availability for all courts"""
    print("🏟️  Angus Glen Tennis Centre - Court Availability Checker")
    print("=" * 60)

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

    print(f"📅 Checking availability for {len(courts_config['courts'])} courts...")

    # Check all courts
    results = session.check_all_courts(courts_config)

    # Display results
    print("\n📊 AVAILABILITY RESULTS:")
    print("-" * 60)

    available_courts = []

    for court_num, data in results.items():
        print(f"\n🏟️  Court {court_num}:")

        if data['availability']:
            print("  Status: ✓ Data retrieved successfully")

            # Try to parse availability data
            slots = session.parse_availability_data(data['availability'])

            if slots:
                print(f"  Available slots: {len(slots)}")
                available_courts.append({
                    'court': court_num,
                    'facility_id': data['facility_id'],
                    'slots': slots
                })

                # Show first few available slots
                for i, slot in enumerate(slots[:3]):
                    print(f"    {i+1}. {slot.get('date', 'N/A')} at {slot.get('time', 'N/A')}")

                if len(slots) > 3:
                    print(f"    ... and {len(slots) - 3} more slots")
            else:
                print("  ⚠️  No available slots found")
        else:
            print(f"  Status: ✗ {data.get('error', 'Failed to retrieve data')}")

    # Summary
    print(f"\n📈 SUMMARY:")
    print(f"  Total courts checked: {len(courts_config['courts'])}")
    print(f"  Courts with availability: {len(available_courts)}")

    if available_courts:
        print(f"\n🎾 COURTS WITH AVAILABLE SLOTS:")
        for court_data in available_courts:
            print(f"  Court {court_data['court']}: {len(court_data['slots'])} slots")

    return len(available_courts) > 0


def main():
    """Main function"""
    try:
        success = check_court_availability()

        if success:
            print("\n✅ Availability check completed successfully!")
            sys.exit(0)
        else:
            print("\n❌ No courts available or check failed!")
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n\n⏹️  Check cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
