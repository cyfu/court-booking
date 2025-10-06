
import json
import random

from FacilityInformation import get_verification_token

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