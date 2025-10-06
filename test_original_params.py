#!/usr/bin/env python3
"""
Test script using the original parameters from FacilityAvailability.py
"""

import requests
import json
from PerfectMindSession import PerfectMindSession


def test_original_parameters():
    """Test using the original parameters from FacilityAvailability.py"""
    print("🧪 Testing Original Parameters from FacilityAvailability.py")
    print("=" * 60)

    # Use the exact parameters from your original code
    url = 'https://cityofmarkham.perfectmind.com/Clients/BookMe4LandingPages/FacilityAvailability'

    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,ja;q=0.7,de;q=0.6,en;q=0.5',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://cityofmarkham.perfectmind.com',
        'priority': 'u=0, i',
        'referer': 'https://cityofmarkham.perfectmind.com/Clients/BookMe4LandingPages/Facility?facilityId=fb8d7c62-2760-48a9-9ecb-b89d8a6e02c2&widgetId=f3086c1c-7fa3-47fd-9976-0e777c8a7456&calendarId=7998c433-21f7-4914-8b85-9c61d6392511&arrivalDate=2024-09-10T03:11:11.707Z&landingPageBackUrl=https%3A%2F%2Fcityofmarkham.perfectmind.com%2FClients%2FBookMe4FacilityList%2FList%3FwidgetId%3Df3086c1c-7fa3-47fd-9976-0e777c8a7456%26calendarId%3D7998c433-21f7-4914-8b85-9c61d6392511',
        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
        'x-newrelic-id': 'VQYHUF5UDRAFUFdUAAMEU1Y=',
        'x-requested-with': 'XMLHttpRequest'
    }

    # First, get a fresh verification token
    session = PerfectMindSession()
    facility_id = 'fb8d7c62-2760-48a9-9ecb-b89d8a6e02c2'

    print(f"🔐 Getting fresh verification token...")
    if session.get_verification_token(facility_id):
        print(f"✓ Got verification token: {session.verification_token[:20]}...")

        # Test with original date (2024-09-12)
        data_original = {
            'facilityId': 'fb8d7c62-2760-48a9-9ecb-b89d8a6e02c2',
            'date': '2024-09-12T00:00:00.000Z',
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

        print(f"\n🧪 Testing with original date (2024-09-12)...")
        response = requests.post(url, headers=headers, data=data_original)

        if response.status_code == 200:
            result = response.json()
            print(f"✓ Status: {response.status_code}")
            print(f"Response keys: {list(result.keys())}")

            if 'availabilities' in result:
                availabilities = result['availabilities']
                print(f"Availabilities count: {len(availabilities)}")

                if availabilities:
                    print(f"✅ Found {len(availabilities)} available slots!")
                    for i, slot in enumerate(availabilities[:3]):
                        print(f"  {i+1}. {slot}")
                else:
                    print(f"❌ No availabilities found")

            # Save response
            with open('original_params_response.json', 'w') as f:
                json.dump(result, f, indent=2)
            print(f"💾 Response saved to original_params_response.json")
        else:
            print(f"✗ Status: {response.status_code}")
            print(f"Response: {response.text[:200]}...")

        # Now test with current date
        print(f"\n🧪 Testing with current date...")
        from datetime import datetime, timedelta
        import pytz

        utc_now = datetime.now(pytz.utc)
        current_date = utc_now.strftime('%Y-%m-%dT00:00:00.000Z')

        data_current = data_original.copy()
        data_current['date'] = current_date

        print(f"Using date: {current_date}")

        response2 = requests.post(url, headers=headers, data=data_current)

        if response2.status_code == 200:
            result2 = response2.json()
            print(f"✓ Status: {response2.status_code}")

            if 'availabilities' in result2:
                availabilities2 = result2['availabilities']
                print(f"Availabilities count: {len(availabilities2)}")

                if availabilities2:
                    print(f"✅ Found {len(availabilities2)} available slots!")
                    for i, slot in enumerate(availabilities2[:3]):
                        print(f"  {i+1}. {slot}")
                else:
                    print(f"❌ No availabilities found")

            # Save response
            with open('current_params_response.json', 'w') as f:
                json.dump(result2, f, indent=2)
            print(f"💾 Response saved to current_params_response.json")
        else:
            print(f"✗ Status: {response2.status_code}")
            print(f"Response: {response2.text[:200]}...")

    else:
        print("✗ Failed to get verification token")


if __name__ == "__main__":
    test_original_parameters()
