#!/usr/bin/env python3
"""
Test all courts and different API approaches
"""

import requests
import json
from datetime import datetime, timedelta
import pytz
from PerfectMindSession import PerfectMindSession


def test_all_courts():
    """Test all 4 courts"""
    print("🧪 Testing All 4 Courts")
    print("=" * 50)

    session = PerfectMindSession()

    # Load court configuration
    with open('court-info.json', 'r') as f:
        courts_config = json.load(f)

    url = f"{session.base_url}/Clients/BookMe4LandingPages/FacilityAvailability"

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
    }

    utc_now = datetime.now(pytz.utc)
    test_date = utc_now.strftime('%Y-%m-%dT00:00:00.000Z')

    for court in courts_config['courts']:
        court_num = court['court']
        facility_id = court['facilityId']

        print(f"\n🏟️  Testing Court {court_num} (ID: {facility_id})")

        # Get verification token for this court
        if session.get_verification_token(facility_id):
            print(f"  ✓ Got verification token")

            headers['Referer'] = f"{session.base_url}/Clients/BookMe4LandingPages/Facility?facilityId={facility_id}"

            data = {
                'facilityId': facility_id,
                'date': test_date,
                'daysCount': 7,
                'duration': 60,
                'serviceId': '308fcf95-0bbc-4fe4-b170-7ca1ad215922',
                'durationIds[]': [
                    'a828d44f-c2c4-4efa-8c0a-5b4e867f7ded',
                    '0af4655c-daef-42d8-8e1c-7bbc02eb49f6',
                    '09184560-08a2-45c5-ba1e-dd0f83842624',
                    '80f3666e-a7d1-4b1b-a891-ff6d8852290e'
                ],
                '__RequestVerificationToken': session.verification_token
            }

            try:
                response = session.session.post(url, headers=headers, data=data)

                if response.status_code == 200:
                    result = response.json()
                    availabilities = result.get('availabilities', [])
                    print(f"  ✓ Status: {response.status_code}, Availabilities: {len(availabilities)}")

                    if availabilities:
                        print(f"  🎾 Found {len(availabilities)} slots!")
                        for slot in availabilities[:3]:
                            print(f"    - {slot}")

                        # Save successful response
                        with open(f'court_{court_num}_success.json', 'w') as f:
                            json.dump(result, f, indent=2)
                        print(f"  💾 Saved to court_{court_num}_success.json")
                    else:
                        print(f"  ❌ No availabilities")
                else:
                    print(f"  ✗ Status: {response.status_code}")
                    print(f"  Response: {response.text[:200]}...")

            except Exception as e:
                print(f"  ✗ Error: {e}")
        else:
            print(f"  ✗ Failed to get verification token")


def test_different_api_endpoints():
    """Test different API endpoints"""
    print("\n🧪 Testing Different API Endpoints")
    print("=" * 50)

    session = PerfectMindSession()
    facility_id = 'fb8d7c62-2760-48a9-9ecb-b89d8a6e02c2'

    if session.get_verification_token(facility_id):
        # Test different possible endpoints
        endpoints = [
            '/Clients/BookMe4LandingPages/FacilityAvailability',
            '/Clients/BookMe4LandingPages/GetAvailability',
            '/Clients/BookMe4LandingPages/Availability',
            '/Clients/BookMe4LandingPages/CheckAvailability',
        ]

        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': f"{session.base_url}/Clients/BookMe4LandingPages/Facility?facilityId={facility_id}",
        }

        utc_now = datetime.now(pytz.utc)
        test_date = utc_now.strftime('%Y-%m-%dT00:00:00.000Z')

        data = {
            'facilityId': facility_id,
            'date': test_date,
            'daysCount': 7,
            'duration': 60,
            'serviceId': '308fcf95-0bbc-4fe4-b170-7ca1ad215922',
            'durationIds[]': [
                'a828d44f-c2c4-4efa-8c0a-5b4e867f7ded',
                '0af4655c-daef-42d8-8e1c-7bbc02eb49f6',
                '09184560-08a2-45c5-ba1e-dd0f83842624',
                '80f3666e-a7d1-4b1b-a891-ff6d8852290e'
            ],
            '__RequestVerificationToken': session.verification_token
        }

        for endpoint in endpoints:
            print(f"\n🧪 Testing endpoint: {endpoint}")

            try:
                url = f"{session.base_url}{endpoint}"
                response = session.session.post(url, headers=headers, data=data)

                print(f"  Status: {response.status_code}")

                if response.status_code == 200:
                    try:
                        result = response.json()
                        print(f"  ✓ JSON response received")
                        print(f"  Keys: {list(result.keys())}")

                        if 'availabilities' in result:
                            availabilities = result['availabilities']
                            print(f"  Availabilities: {len(availabilities)}")

                            if availabilities:
                                print(f"  🎾 Found slots!")
                                for slot in availabilities[:2]:
                                    print(f"    - {slot}")
                        else:
                            print(f"  No 'availabilities' key")

                    except json.JSONDecodeError:
                        print(f"  ✗ Invalid JSON response")
                        print(f"  Response: {response.text[:200]}...")
                else:
                    print(f"  ✗ Request failed")

            except Exception as e:
                print(f"  ✗ Error: {e}")


def test_get_request():
    """Test using GET request instead of POST"""
    print("\n🧪 Testing GET Request")
    print("=" * 30)

    session = PerfectMindSession()
    facility_id = 'fb8d7c62-2760-48a9-9ecb-b89d8a6e02c2'

    if session.get_verification_token(facility_id):
        url = f"{session.base_url}/Clients/BookMe4LandingPages/FacilityAvailability"

        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': f"{session.base_url}/Clients/BookMe4LandingPages/Facility?facilityId={facility_id}",
        }

        utc_now = datetime.now(pytz.utc)
        test_date = utc_now.strftime('%Y-%m-%dT00:00:00.000Z')

        params = {
            'facilityId': facility_id,
            'date': test_date,
            'daysCount': 7,
            'duration': 60,
            'serviceId': '308fcf95-0bbc-4fe4-b170-7ca1ad215922',
            '__RequestVerificationToken': session.verification_token
        }

        try:
            response = session.session.get(url, headers=headers, params=params)

            print(f"Status: {response.status_code}")

            if response.status_code == 200:
                try:
                    result = response.json()
                    print(f"✓ JSON response received")
                    print(f"Keys: {list(result.keys())}")

                    if 'availabilities' in result:
                        availabilities = result['availabilities']
                        print(f"Availabilities: {len(availabilities)}")

                        if availabilities:
                            print(f"🎾 Found slots!")
                            for slot in availabilities[:2]:
                                print(f"  - {slot}")
                    else:
                        print(f"No 'availabilities' key")

                except json.JSONDecodeError:
                    print(f"✗ Invalid JSON response")
                    print(f"Response: {response.text[:200]}...")
            else:
                print(f"✗ Request failed")

        except Exception as e:
            print(f"✗ Error: {e}")


if __name__ == "__main__":
    test_all_courts()
    test_different_api_endpoints()
    test_get_request()
