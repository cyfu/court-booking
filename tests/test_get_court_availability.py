from get_court_availability import *
import pytest

# Define a fixture
@pytest.fixture
def soup():
    with open("tests/fixtures/scheduler.html", "r") as f:
        soup = BeautifulSoup(f, "html.parser")
    return soup

def test_convert_datetime_AM():
    dt = convert_datetime(2023, 'Dec 22', '1:00 AM')
    assert isinstance(dt, datetime)
    assert dt.year == 2023
    assert dt.month == 12
    assert dt.day == 22
    assert dt.hour == 1


def test_convert_datetime_PM():
    dt = convert_datetime(2023, 'Dec 22', '1:30 PM')
    assert isinstance(dt, datetime)
    assert dt.year == 2023
    assert dt.month == 12
    assert dt.day == 22
    assert dt.hour == 13
    assert dt.minute == 30

def test_get_court_availability(soup):
    availability_dict = get_court_availability(soup)
    assert len(availability_dict) == 2
    assert availability_dict[0]['date'] == 'Dec 22'
    assert availability_dict[0]['time'] == '1:00 AM'
    assert availability_dict[1]['date'] == 'Dec 23'
    assert availability_dict[1]['time'] == '7:00 AM'
