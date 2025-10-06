#!/usr/bin/env python3
"""
Debug script to analyze the actual response structure from PerfectMind API
"""

import json
import sys
from PerfectMindSession import PerfectMindSession


def debug_api_response():
    """Debug the API response structure"""
    print("🔍 Debugging PerfectMind API Response")
    print("=" * 50)

    session = PerfectMindSession()

    # Load court configuration
    with open('court-info.json', 'r') as f:
        courts_config = json.load(f)

    # Test with just the first court
    court = courts_config['courts'][0]
    facility_id = court['facilityId']

    print(f"Testing with Court {court['court']} (ID: {facility_id})")

    # Get verification token first
    if session.get_verification_token(facility_id):
        print("✓ Got verification token")

        # Check availability
        availability_data = session.check_availability(facility_id)

        if availability_data:
            print("\n📊 Raw API Response:")
            print("-" * 30)
            print(json.dumps(availability_data, indent=2))

            # Save to file for analysis
            with open('debug_response.json', 'w') as f:
                json.dump(availability_data, f, indent=2)
            print("\n💾 Response saved to debug_response.json")

            # Try to analyze the structure
            print("\n🔍 Response Analysis:")
            print(f"  Type: {type(availability_data)}")

            if isinstance(availability_data, dict):
                print(f"  Keys: {list(availability_data.keys())}")

                # Look for common patterns
                for key, value in availability_data.items():
                    print(f"  {key}: {type(value)}")
                    if isinstance(value, list) and len(value) > 0:
                        print(f"    List length: {len(value)}")
                        if len(value) > 0:
                            print(f"    First item type: {type(value[0])}")
                            if isinstance(value[0], dict):
                                print(f"    First item keys: {list(value[0].keys())}")

            elif isinstance(availability_data, list):
                print(f"  List length: {len(availability_data)}")
                if len(availability_data) > 0:
                    print(f"  First item type: {type(availability_data[0])}")
                    if isinstance(availability_data[0], dict):
                        print(f"  First item keys: {list(availability_data[0].keys())}")
        else:
            print("✗ Failed to get availability data")
    else:
        print("✗ Failed to get verification token")


if __name__ == "__main__":
    debug_api_response()
