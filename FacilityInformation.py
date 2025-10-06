from datetime import datetime, timedelta
import requests
import json
import pytz
import random
from bs4 import BeautifulSoup
from get_court_availability import get_court_availability, extract_verification_token

def set_arrival_date():
    # Get the current date and time in UTC
    utc_now = datetime.now(pytz.utc)
    print(f"Current time in UTC: {utc_now}")  # Output: e.g., 2023-12-18 22:45:50.432000+00:00    
    utc_now += timedelta(days=1)   # Add 1 day to the current date
    print(f"One Day after current time in UTC: {utc_now}")  # Output: e.g., 2023-12-18 22:45:50.432000+00:00    

    # Create a timezone object for a specific timezone
    tz = pytz.timezone('America/Toronto')

    # Convert the current UTC time to the specified timezone
    local_now = utc_now.astimezone(tz)
    print(f"Current time in Toronto: {local_now}")  # Output: e.g., 2023-12-18 17:45:50.432000-05:00

    # Convert it to a string in the specified format
    utc_now_str = utc_now.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    return utc_now_str

def get_verification_token(facility, court):
    # Define the headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Content-Type': 'application/json',
    }

    # Prepare the parameters
    params = {
        'widgetId': facility['widgetId'],
        'calendarId': facility['calendarId'],
        'arrivalDate': set_arrival_date(),  #data['arrivalDate'],
        'facilityId': court['facilityId']
    }

    # Send the GET request
    response = requests.get(facility['url'], headers=headers, params=params)

    # Check the status code and print the response
    if response.status_code == 200:
        print(f"Court {court['court']}: ")
        with open(f"{court['court']}.html", 'w') as f:
            f.write(response.text)
        soup = BeautifulSoup(response.text, "html.parser")
        # print(get_court_availability(soup))
        return extract_verification_token(soup)
    else:
        print(f"Request for court {court['court']} failed with status code {response.status_code}")
        return None 

if __name__ == "__main__":
    # Open the court config file
    with open('court-info.json', 'r') as f:
        # Load the JSON data
        facility = json.load(f)


    random.shuffle(facility['courts'])
    for court in facility['courts']:
        verification_token = get_verification_token(facility, court)

        if verification_token:
            print(f"Verification token for court {court['court']}: {verification_token}")
        else:
            print(f"Failed to get verification token for court {court['court']}")           