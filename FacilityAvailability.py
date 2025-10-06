import requests


def get_court_availability():
    url = 'https://cityofmarkham.perfectmind.com/Clients/BookMe4LandingPages/FacilityAvailability'

    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,ja;q=0.7,de;q=0.6,en;q=0.5',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'cookie': '__RequestVerificationToken=91NVnjViXKYK14gUNgfCPe7jFMSfqc_hoNVyVE6czkb_lP-hn76vfAYTKkKU6w6zDqDiZ-2ARBDLvyLKzORACg9mbF81; mobileWidthCookie=0; planner=; ShowCancelledEvents_cda01e05-ae2f-4fe6-ac0a-8e647a43b334=false; _lr_uf_-wehk4y=3a5faf0e-5847-4a08-8310-8d5916cccba5; PMSessionId=w1v2tmbaxmfpedduj3wylrc4; perfectmindmobilefeature=0; ClusterId=ga2-member',
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

    data = {
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
        '__RequestVerificationToken': '74Ws_r0ZSQSQQwWBQTPXpftIMzK5pHqU9ecc2iqOLtkn_aa0LJoCGnEdpkAGV-Uo-g8emdIDHYR4K53CGUai0Oyn5GF5qNphiv2pJvkiS2IJvaOI0'
    }

    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        print("Request successful.")
        print(response.json())
    else:
        print(f"Request failed with status code: {response.status_code}")

if __name__ == "__main__":
    get_court_availability()