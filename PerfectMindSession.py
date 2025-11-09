import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import pytz


class PerfectMindSession:
    """Handles authentication and session management for PerfectMind booking system"""

    def __init__(self):
        self.session = requests.Session()
        self.base_url = "https://cityofmarkham.perfectmind.com"
        self.verification_token = None
        self.session_id = None

        # Set default headers (matching browser exactly)
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-CA,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,en-GB;q=0.6,en-US;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })

    def get_verification_token(self, facility_id):
        """Get verification token from the facility page"""
        url = f"{self.base_url}/Clients/BookMe4LandingPages/Facility"
        params = {
            'facilityId': facility_id,
            'widgetId': 'f3086c1c-7fa3-47fd-9976-0e777c8a7456',
            'calendarId': '7998c433-21f7-4914-8b85-9c61d6392511',
            'arrivalDate': self._get_current_datetime(),
            'landingPageBackUrl': 'https://cityofmarkham.perfectmind.com/Clients/BookMe4FacilityList/List?widgetId=f3086c1c-7fa3-47fd-9976-0e777c8a7456&calendarId=7998c433-21f7-4914-8b85-9c61d6392511'
        }

        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract verification token
            form = soup.find('form', id='AjaxAntiForgeryForm')
            if form:
                token_input = form.find('input', {'name': '__RequestVerificationToken'})
                if token_input:
                    self.verification_token = token_input.get('value')
                    print(f"✓ Got verification token: {self.verification_token[:20]}...")
                    return True

            # Extract session ID and other cookies
            if 'PMSessionId' in self.session.cookies:
                self.session_id = self.session.cookies['PMSessionId']
                print(f"✓ Got session ID: {self.session_id}")

            # Set additional cookies that might be needed
            self.session.cookies.set('perfectmindmobilefeature', '0')
            self.session.cookies.set('mobileWidthCookie', '0')
            self.session.cookies.set('ClusterId', 'ga2-member')

            return False

        except requests.RequestException as e:
            print(f"✗ Failed to get verification token: {e}")
            return False

    def check_availability(self, facility_id, date=None, days_count=7, duration=60):
        """Check court availability for a specific facility

        Args:
            facility_id: The facility ID to check
            date: Specific date to check (format: 'YYYY-MM-DD' or None for current date)
            days_count: Number of days to check from the start date
            duration: Duration in minutes
        """
        if not self.verification_token:
            if not self.get_verification_token(facility_id):
                return None

        url = f"{self.base_url}/Clients/BookMe4LandingPages/FacilityAvailability"

        # Set headers for AJAX request (matching browser exactly)
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'en-CA,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,en-GB;q=0.6,en-US;q=0.5',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'https://cityofmarkham.perfectmind.com',
            'Priority': 'u=0, i',
            'Referer': f"{self.base_url}/Clients/BookMe4LandingPages/Facility?facilityId={facility_id}&widgetId=f3086c1c-7fa3-47fd-9976-0e777c8a7456&calendarId=7998c433-21f7-4914-8b85-9c61d6392511&arrivalDate=2025-10-05T23:05:36.734Z&landingPageBackUrl=https%3A%2F%2Fcityofmarkham.perfectmind.com%2FClients%2FBookMe4FacilityList%2FList%3FwidgetId%3Df3086c1c-7fa3-47fd-9976-0e777c8a7456%26calendarId%3D7998c433-21f7-4914-8b85-9c61d6392511",
            'Sec-Ch-Ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
        }

        # Use provided date or current datetime for API request
        if date:
            api_date = self._format_date_for_api(date)
            print(f"✓ Using specific date for API: {api_date}")
        else:
            api_date = self._get_current_datetime()
            print(f"✓ Using current datetime for API: {api_date}")
        data = {
            'facilityId': facility_id,
            'date': api_date,
            'daysCount': days_count,
            'duration': duration,
            'serviceId': '308fcf95-0bbc-4fe4-b170-7ca1ad215922',  # Tennis service ID
            'durationIds[]': [
                'a828d44f-c2c4-4efa-8c0a-5b4e867f7ded',  # 60 min
                'c431ba5d-2f05-4036-bc15-62bbe0b493ab',  # Additional duration
                'ce80014f-da18-47ca-9486-63c770e7590e',  # Additional duration
                '0af4655c-daef-42d8-8e1c-7bbc02eb49f6',  # 90 min
                '09184560-08a2-45c5-ba1e-dd0f83842624',  # 120 min
                '80f3666e-a7d1-4b1b-a891-ff6d8852290e'   # 180 min
            ],
            '__RequestVerificationToken': self.verification_token
        }

        try:
            print(
                f"Sending request to {url} with headers: {headers} and data: {data}")
            response = self.session.post(url, headers=headers, data=data)
            response.raise_for_status()

            if response.status_code == 200:
                availability_data = response.json()
                print(f"✓ Got availability data for facility {facility_id}")
                print(f"✓ Response: {availability_data}")
                return availability_data
            else:
                print(f"✗ Request failed with status code: {response.status_code}")
                return None

        except requests.RequestException as e:
            print(f"✗ Failed to check availability: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"✗ Failed to parse JSON response: {e}")
            return None

    def check_all_courts(self, courts_config):
        """Check availability for all courts"""
        results = {}

        for court in courts_config['courts']:
            court_num = court['court']
            facility_id = court['facilityId']

            print(f"\n🏟️  Checking Court {court_num} (ID: {facility_id})")
            availability = self.check_availability(facility_id)

            if availability:
                results[court_num] = {
                    'facility_id': facility_id,
                    'availability': availability
                }
            else:
                results[court_num] = {
                    'facility_id': facility_id,
                    'availability': None,
                    'error': 'Failed to get availability data'
                }

        return results

    def _get_current_datetime(self):
        """Get current datetime in the required format using Toronto time"""
        toronto_tz = pytz.timezone('America/Toronto')
        toronto_now = datetime.now(toronto_tz)
        return toronto_now.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

    def _format_date_for_api(self, date_str):
        """Format a specific date string to API format (start of day)"""
        try:
            from datetime import datetime
            input_date = datetime.strptime(date_str, '%Y-%m-%d')
            formatted_date = input_date.replace(hour=0, minute=0, second=0, microsecond=0)
            return formatted_date.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        except ValueError:
            return self._get_current_datetime()

    def get_complete_availability(self, facility_id, duration=60):
        """Get complete availability by making two API calls to cover 8 days total"""
        all_slots = []
        
        # First call: current datetime (gets next 6-7 days)
        availability_1 = self.check_availability(facility_id, duration=duration)
        if availability_1:
            slots_1 = self.parse_availability_data(availability_1)
            all_slots.extend(slots_1)
        
        # Second call: 7 days from now (gets 8th day)
        from datetime import datetime, timedelta
        toronto_tz = pytz.timezone('America/Toronto')
        future_date = datetime.now(toronto_tz) + timedelta(days=7)
        future_date_str = future_date.strftime('%Y-%m-%d')
        
        availability_2 = self.check_availability(facility_id, date=future_date_str, duration=duration)
        if availability_2:
            slots_2 = self.parse_availability_data(availability_2)
            all_slots.extend(slots_2)
        
        return all_slots

    def display_availability_table(self, slots):
        """Display availability in table format with dates as columns"""
        if not slots:
            print("No availability data to display")
            return
        
        # Group slots by date
        slots_by_date = {}
        for slot in slots:
            date = slot['date']
            if date not in slots_by_date:
                slots_by_date[date] = []
            slots_by_date[date].append(slot)
        
        # Get sorted dates
        dates = sorted(slots_by_date.keys())
        
        # Print header
        print("\n📅 Court Availability Table")
        print("=" * (12 + len(dates) * 12))
        
        # Print date headers
        header = "Time        "
        for date in dates:
            header += f"{date[-5:]:>11} "  # Show MM-DD only
        print(header)
        print("-" * len(header))
        
        # Get all unique times
        all_times = set()
        for date_slots in slots_by_date.values():
            for slot in date_slots:
                all_times.add(slot['time'])
        
        # Print availability for each time slot
        for time in sorted(all_times):
            row = f"{time:>11} "
            for date in dates:
                # Check if this time is available on this date
                available = any(slot['time'] == time for slot in slots_by_date.get(date, []))
                row += "     ✓     " if available else "     -     "
            print(row)
        
        print("\n✓ = Available, - = Not Available")

    def check_and_display_availability(self, facility_id, duration=60):
        """Check availability and display in table format"""
        availability_data = self.check_availability(facility_id, duration=duration)
        if availability_data:
            slots = self.parse_availability_data(availability_data)
            self.display_availability_table(slots)
            return slots
        return []

    def parse_availability_data(self, availability_data):
        """Parse the availability data to extract available time slots"""
        if not availability_data:
            return []

        available_slots = []

        # Parse the actual response structure
        if isinstance(availability_data, dict) and 'availabilities' in availability_data:
            days = availability_data['availabilities']

            for day in days:
                if isinstance(day, dict) and 'BookingGroups' in day:
                    # Extract date from /Date(timestamp)/ format using Toronto timezone
                    date_str = day.get('Date', '')
                    if date_str.startswith('/Date(') and date_str.endswith(')/'):
                        timestamp = int(date_str[6:-2])  # Extract timestamp
                        from datetime import datetime
                        # Convert UTC timestamp to Toronto time
                        utc_date = datetime.fromtimestamp(timestamp / 1000, tz=pytz.UTC)
                        toronto_tz = pytz.timezone('America/Toronto')
                        toronto_date = utc_date.astimezone(toronto_tz)
                        date_formatted = toronto_date.strftime('%Y-%m-%d')
                    else:
                        date_formatted = 'Unknown'

                    # Process each booking group (Morning, Afternoon, Late)
                    for group in day['BookingGroups']:
                        group_name = group.get('Name', 'Unknown')

                        # Process each available spot in the group
                        for spot in group.get('AvailableSpots', []):
                            time_info = spot.get('Time', {})
                            duration_info = spot.get('Duration', {})

                            # Format time
                            hours = time_info.get('Hours', 0)
                            minutes = time_info.get('Minutes', 0)
                            time_formatted = f"{hours:02d}:{minutes:02d}"

                            # Format duration
                            duration_hours = duration_info.get('Hours', 0)
                            duration_minutes = duration_info.get('Minutes', 0)
                            duration_formatted = f"{duration_hours * 60 + duration_minutes}min"

                            available_slots.append({
                                'date': date_formatted,
                                'time': time_formatted,
                                'duration': duration_formatted,
                                'group': group_name,
                                'title': spot.get('Title', 'Book Now!'),
                                'ticks': spot.get('Ticks'),
                                'is_disabled': spot.get('IsDisabled', False)
                            })

        return available_slots


def main():
    """Test the session management"""
    session = PerfectMindSession()

    # Load court configuration
    with open('court-info.json', 'r') as f:
        courts_config = json.load(f)

    # Check all courts
    results = session.check_all_courts(courts_config)

    # Print results
    print("\n📊 Availability Results:")
    for court_num, data in results.items():
        if data['availability']:
            print(f"Court {court_num}: ✓ Data received")
            # Parse and display available slots
            slots = session.parse_availability_data(data['availability'])
            if slots:
                print(f"  Available slots: {len(slots)}")
                for slot in slots[:3]:  # Show first 3 slots
                    print(f"    - {slot.get('date')} {slot.get('time')}")
            else:
                print("  No available slots found")
        else:
            print(f"Court {court_num}: ✗ {data.get('error', 'Unknown error')}")


if __name__ == "__main__":
    main()
