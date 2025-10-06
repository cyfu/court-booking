#!/usr/bin/env python3
"""
Test script to replicate the exact browser request
"""

import requests
import json
from PerfectMindSession import PerfectMindSession


def test_with_full_session():
    """Test with full session including cookies"""
    print("🧪 Testing with Full Session (including cookies)")
    print("=" * 60)

    session = PerfectMindSession()
    facility_id = 'fb8d7c62-2760-48a9-9ecb-b89d8a6e02c2'

    # Get verification token first
    print(f"🔐 Getting verification token...")
    if session.get_verification_token(facility_id):
        print(f"✓ Got verification token: {session.verification_token[:20]}...")

        # Now make the availability request using the session
        url = f"{session.base_url}/Clients/BookMe4LandingPages/FacilityAvailability"

        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.9',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'https://cityofmarkham.perfectmind.com',
            'Referer': f"{session.base_url}/Clients/BookMe4LandingPages/Facility?facilityId={facility_id}&widgetId=f3086c1c-7fa3-47fd-9976-0e777c8a7456&calendarId=7998c433-21f7-4914-8b85-9c61d6392511&arrivalDate=2025-10-05T22:50:01.285Z&landingPageBackUrl=https%3A%2F%2Fcityofmarkham.perfectmind.com%2FClients%2FBookMe4FacilityList%2FList%3FwidgetId%3Df3086c1c-7fa3-47fd-9976-0e777c8a7456%26calendarId%3D7998c433-21f7-4914-8b85-9c61d6392511",
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'X-Requested-With': 'XMLHttpRequest',
        }

        from datetime import datetime, timedelta
        import pytz

        utc_now = datetime.now(pytz.utc)
        current_date = utc_now.strftime('%Y-%m-%dT00:00:00.000Z')

        data = {
            'facilityId': facility_id,
            'date': current_date,
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

        print(f"📅 Using date: {current_date}")
        print(f"🏟️  Facility ID: {facility_id}")

        try:
            response = session.session.post(url, headers=headers, data=data)

            print(f"📊 Response Status: {response.status_code}")

            if response.status_code == 200:
                try:
                    result = response.json()
                    print(f"✅ Success! Response keys: {list(result.keys())}")

                    if 'availabilities' in result:
                        availabilities = result['availabilities']
                        print(f"📅 Availabilities count: {len(availabilities)}")

                        if availabilities:
                            print(f"🎾 Found {len(availabilities)} available slots!")
                            for i, slot in enumerate(availabilities[:5]):
                                print(f"  {i+1}. {slot}")
                        else:
                            print(f"❌ No availabilities found")
                            print(f"🔍 This might be because:")
                            print(f"  - No slots available for the requested date range")
                            print(f"  - Wrong serviceId or durationIds")
                            print(f"  - API requires different parameters")

                    # Save response for analysis
                    with open('full_session_response.json', 'w') as f:
                        json.dump(result, f, indent=2)
                    print(f"💾 Response saved to full_session_response.json")

                except json.JSONDecodeError as e:
                    print(f"❌ JSON decode error: {e}")
                    print(f"Response text: {response.text[:500]}...")
            else:
                print(f"❌ Request failed with status: {response.status_code}")
                print(f"Response: {response.text[:500]}...")

        except Exception as e:
            print(f"❌ Request error: {e}")

    else:
        print("❌ Failed to get verification token")


def test_different_service_ids():
    """Test with different service IDs"""
    print("\n🧪 Testing Different Service IDs")
    print("=" * 40)

    session = PerfectMindSession()
    facility_id = 'fb8d7c62-2760-48a9-9ecb-b89d8a6e02c2'

    if session.get_verification_token(facility_id):
        # Test different service IDs that might be used for tennis
        service_ids = [
            '308fcf95-0bbc-4fe4-b170-7ca1ad215922',  # Original
            '',  # Empty service ID
            None,  # No service ID
        ]

        for i, service_id in enumerate(service_ids):
            print(f"\n🧪 Test {i+1}: Service ID = {service_id}")

            url = f"{session.base_url}/Clients/BookMe4LandingPages/FacilityAvailability"

            headers = {
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'X-Requested-With': 'XMLHttpRequest',
                'Referer': f"{session.base_url}/Clients/BookMe4LandingPages/Facility?facilityId={facility_id}",
            }

            from datetime import datetime
            import pytz

            utc_now = datetime.now(pytz.utc)
            current_date = utc_now.strftime('%Y-%m-%dT00:00:00.000Z')

            data = {
                'facilityId': facility_id,
                'date': current_date,
                'daysCount': 7,
                'duration': 60,
                'durationIds[]': [
                    'a828d44f-c2c4-4efa-8c0a-5b4e867f7ded',
                    '0af4655c-daef-42d8-8e1c-7bbc02eb49f6',
                    '09184560-08a2-45c5-ba1e-dd0f83842624',
                    '80f3666e-a7d1-4b1b-a891-ff6d8852290e'
                ],
                '__RequestVerificationToken': session.verification_token
            }

            if service_id:
                data['serviceId'] = service_id

            try:
                response = session.session.post(url, headers=headers, data=data)

                if response.status_code == 200:
                    result = response.json()
                    availabilities = result.get('availabilities', [])
                    print(f"  ✓ Status: {response.status_code}, Availabilities: {len(availabilities)}")

                    if availabilities:
                        print(f"  🎾 Found slots: {availabilities[0]}")
                else:
                    print(f"  ✗ Status: {response.status_code}")

            except Exception as e:
                print(f"  ✗ Error: {e}")


if __name__ == "__main__":
    test_with_full_session()
    test_different_service_ids()
