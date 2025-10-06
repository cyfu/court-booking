#!/usr/bin/env python3
"""
Test different date ranges and parameters to find available slots
"""

import requests
import json
from datetime import datetime, timedelta
import pytz
from PerfectMindSession import PerfectMindSession


def test_date_ranges():
    """Test different date ranges"""
    print("🧪 Testing Different Date Ranges")
    print("=" * 50)

    session = PerfectMindSession()
    facility_id = 'fb8d7c62-2760-48a9-9ecb-b89d8a6e02c2'

    if session.get_verification_token(facility_id):
        url = f"{session.base_url}/Clients/BookMe4LandingPages/FacilityAvailability"

        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': f"{session.base_url}/Clients/BookMe4LandingPages/Facility?facilityId={facility_id}",
        }

        # Test different date ranges
        utc_now = datetime.now(pytz.utc)
        toronto_tz = pytz.timezone('America/Toronto')
        toronto_now = utc_now.astimezone(toronto_tz)

        test_dates = [
            # Today
            utc_now.strftime('%Y-%m-%dT00:00:00.000Z'),
            # Tomorrow
            (utc_now + timedelta(days=1)).strftime('%Y-%m-%dT00:00:00.000Z'),
            # Day after tomorrow
            (utc_now + timedelta(days=2)).strftime('%Y-%m-%dT00:00:00.000Z'),
            # Next week
            (utc_now + timedelta(days=7)).strftime('%Y-%m-%dT00:00:00.000Z'),
            # Specific date from screenshot (Oct 5, 2025)
            '2025-10-05T00:00:00.000Z',
            # Oct 6, 2025
            '2025-10-06T00:00:00.000Z',
        ]

        for i, test_date in enumerate(test_dates):
            print(f"\n🧪 Test {i+1}: Date = {test_date}")

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
                        for j, slot in enumerate(availabilities[:3]):
                            print(f"    {j+1}. {slot}")

                        # Save this successful response
                        with open(f'successful_response_{i+1}.json', 'w') as f:
                            json.dump(result, f, indent=2)
                        print(f"  💾 Saved to successful_response_{i+1}.json")
                    else:
                        print(f"  ❌ No availabilities")
                else:
                    print(f"  ✗ Status: {response.status_code}")

            except Exception as e:
                print(f"  ✗ Error: {e}")


def test_different_durations():
    """Test different duration settings"""
    print("\n🧪 Testing Different Duration Settings")
    print("=" * 50)

    session = PerfectMindSession()
    facility_id = 'fb8d7c62-2760-48a9-9ecb-b89d8a6e02c2'

    if session.get_verification_token(facility_id):
        url = f"{session.base_url}/Clients/BookMe4LandingPages/FacilityAvailability"

        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': f"{session.base_url}/Clients/BookMe4LandingPages/Facility?facilityId={facility_id}",
        }

        # Test different durations
        durations = [30, 60, 90, 120]

        utc_now = datetime.now(pytz.utc)
        test_date = utc_now.strftime('%Y-%m-%dT00:00:00.000Z')

        for duration in durations:
            print(f"\n🧪 Testing duration: {duration} minutes")

            data = {
                'facilityId': facility_id,
                'date': test_date,
                'daysCount': 7,
                'duration': duration,
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
                    print(f"  ✓ Availabilities: {len(availabilities)}")

                    if availabilities:
                        print(f"  🎾 Found slots for {duration}min duration!")
                        for slot in availabilities[:2]:
                            print(f"    - {slot}")
                else:
                    print(f"  ✗ Status: {response.status_code}")

            except Exception as e:
                print(f"  ✗ Error: {e}")


def test_without_duration_ids():
    """Test without durationIds array"""
    print("\n🧪 Testing Without DurationIds Array")
    print("=" * 50)

    session = PerfectMindSession()
    facility_id = 'fb8d7c62-2760-48a9-9ecb-b89d8a6e02c2'

    if session.get_verification_token(facility_id):
        url = f"{session.base_url}/Clients/BookMe4LandingPages/FacilityAvailability"

        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': f"{session.base_url}/Clients/BookMe4LandingPages/Facility?facilityId={facility_id}",
        }

        utc_now = datetime.now(pytz.utc)
        test_date = utc_now.strftime('%Y-%m-%dT00:00:00.000Z')

        # Test without durationIds array
        data = {
            'facilityId': facility_id,
            'date': test_date,
            'daysCount': 7,
            'duration': 60,
            'serviceId': '308fcf95-0bbc-4fe4-b170-7ca1ad215922',
            '__RequestVerificationToken': session.verification_token
        }

        print(f"Testing without durationIds array...")

        try:
            response = session.session.post(url, headers=headers, data=data)

            if response.status_code == 200:
                result = response.json()
                availabilities = result.get('availabilities', [])
                print(f"✓ Status: {response.status_code}, Availabilities: {len(availabilities)}")

                if availabilities:
                    print(f"🎾 Found {len(availabilities)} slots!")
                    for slot in availabilities[:3]:
                        print(f"  - {slot}")
                else:
                    print(f"❌ No availabilities")
            else:
                print(f"✗ Status: {response.status_code}")

        except Exception as e:
            print(f"✗ Error: {e}")


if __name__ == "__main__":
    test_date_ranges()
    test_different_durations()
    test_without_duration_ids()
