#!/usr/bin/env python3
"""
Enhanced debug script to analyze API requests and responses
"""

import json
import sys
from datetime import datetime, timedelta
import pytz
from PerfectMindSession import PerfectMindSession


def debug_detailed_api():
    """Debug the API with detailed logging"""
    print("🔍 Detailed API Debug Analysis")
    print("=" * 50)

    session = PerfectMindSession()

    # Load court configuration
    with open('court-info.json', 'r') as f:
        courts_config = json.load(f)

    # Test with Court 1
    court = courts_config['courts'][0]
    facility_id = court['facilityId']

    print(f"Testing with Court {court['court']} (ID: {facility_id})")

    # Get current date info
    utc_now = datetime.now(pytz.utc)
    toronto_tz = pytz.timezone('America/Toronto')
    toronto_now = utc_now.astimezone(toronto_tz)

    print(f"\n📅 Current Time Info:")
    print(f"  UTC: {utc_now}")
    print(f"  Toronto: {toronto_now}")
    print(f"  Date string: {utc_now.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'}")

    # Get verification token
    print(f"\n🔐 Getting verification token...")
    if session.get_verification_token(facility_id):
        print("✓ Got verification token")

        # Test different date formats
        test_dates = [
            utc_now.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z',  # Current time
            utc_now.strftime('%Y-%m-%dT00:00:00.000Z'),  # Today at midnight
            (utc_now + timedelta(days=1)).strftime('%Y-%m-%dT00:00:00.000Z'),  # Tomorrow at midnight
        ]

        for i, test_date in enumerate(test_dates):
            print(f"\n🧪 Test {i+1}: Date = {test_date}")

            # Make API request
            availability_data = session.check_availability(facility_id, date=test_date)

            if availability_data:
                print(f"  ✓ Got response")
                print(f"  Response keys: {list(availability_data.keys())}")

                if 'availabilities' in availability_data:
                    availabilities = availability_data['availabilities']
                    print(f"  Availabilities count: {len(availabilities)}")

                    if availabilities:
                        print(f"  First availability: {availabilities[0]}")

                        # Parse slots
                        slots = session.parse_availability_data(availability_data)
                        print(f"  Parsed slots count: {len(slots)}")

                        if slots:
                            print(f"  First slot: {slots[0]}")
                    else:
                        print(f"  No availabilities found")
                else:
                    print(f"  No 'availabilities' key in response")

                # Save response for analysis
                filename = f"debug_response_test_{i+1}.json"
                with open(filename, 'w') as f:
                    json.dump(availability_data, f, indent=2)
                print(f"  💾 Response saved to {filename}")
            else:
                print(f"  ✗ No response")
    else:
        print("✗ Failed to get verification token")


def test_different_parameters():
    """Test different API parameters"""
    print("\n🧪 Testing Different API Parameters")
    print("=" * 50)

    session = PerfectMindSession()

    with open('court-info.json', 'r') as f:
        courts_config = json.load(f)

    court = courts_config['courts'][0]
    facility_id = court['facilityId']

    # Get token first
    if not session.get_verification_token(facility_id):
        print("✗ Failed to get verification token")
        return

    # Test different parameter combinations
    test_cases = [
        {
            'name': 'Default parameters',
            'params': {
                'facilityId': facility_id,
                'date': datetime.now(pytz.utc).strftime('%Y-%m-%dT00:00:00.000Z'),
                'daysCount': 7,
                'duration': 60,
                'serviceId': '308fcf95-0bbc-4fe4-b170-7ca1ad215922',
                'durationIds[]': [
                    'a828d44f-c2c4-4efa-8c0a-5b4e867f7ded',
                    '0af4655c-daef-42d8-8e1c-7bbc02eb49f6',
                    '09184560-08a2-45c5-ba1e-dd0f83842624',
                    '80f3666e-a7d1-4b1b-a891-ff6d8852290e'
                ]
            }
        },
        {
            'name': 'Without durationIds',
            'params': {
                'facilityId': facility_id,
                'date': datetime.now(pytz.utc).strftime('%Y-%m-%dT00:00:00.000Z'),
                'daysCount': 7,
                'duration': 60,
                'serviceId': '308fcf95-0bbc-4fe4-b170-7ca1ad215922'
            }
        },
        {
            'name': 'Without serviceId',
            'params': {
                'facilityId': facility_id,
                'date': datetime.now(pytz.utc).strftime('%Y-%m-%dT00:00:00.000Z'),
                'daysCount': 7,
                'duration': 60,
                'durationIds[]': [
                    'a828d44f-c2c4-4efa-8c0a-5b4e867f7ded',
                    '0af4655c-daef-42d8-8e1c-7bbc02eb49f6',
                    '09184560-08a2-45c5-ba1e-dd0f83842624',
                    '80f3666e-a7d1-4b1b-a891-ff6d8852290e'
                ]
            }
        }
    ]

    for i, test_case in enumerate(test_cases):
        print(f"\n🧪 Test Case {i+1}: {test_case['name']}")

        # Make custom request
        url = f"{session.base_url}/Clients/BookMe4LandingPages/FacilityAvailability"

        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': f"{session.base_url}/Clients/BookMe4LandingPages/Facility?facilityId={facility_id}",
        }

        data = test_case['params'].copy()
        data['__RequestVerificationToken'] = session.verification_token

        try:
            response = session.session.post(url, headers=headers, data=data)

            if response.status_code == 200:
                try:
                    result = response.json()
                    print(f"  ✓ Status: {response.status_code}")
                    print(f"  Response keys: {list(result.keys())}")

                    if 'availabilities' in result:
                        availabilities = result['availabilities']
                        print(f"  Availabilities: {len(availabilities)}")

                        if availabilities:
                            print(f"  First availability: {availabilities[0]}")
                        else:
                            print(f"  No availabilities found")
                    else:
                        print(f"  No 'availabilities' key")

                except json.JSONDecodeError:
                    print(f"  ✗ Invalid JSON response")
                    print(f"  Response text: {response.text[:200]}...")
            else:
                print(f"  ✗ Status: {response.status_code}")
                print(f"  Response: {response.text[:200]}...")

        except Exception as e:
            print(f"  ✗ Error: {e}")


if __name__ == "__main__":
    debug_detailed_api()
    test_different_parameters()
