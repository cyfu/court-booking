from bs4 import BeautifulSoup, Tag
from datetime import datetime
import calendar



def find_scheduler_wrapper(soup):
    """Finds and returns the div with class 'scheduler-wrapper' from the soup object.

    Args:
        soup: A BeautifulSoup object representing the HTML content.

    Returns:
        A BeautifulSoup object of the div with class 'scheduler-wrapper', or None if not found.
    """
    return soup.find("div", class_="scheduler-wrapper")

def find_scheduler(soup):
    """Finds and returns the div with id 'scheduler' and class 'k-scheduler' from the soup object.

    Args:
        soup: A BeautifulSoup object representing the HTML content.

    Returns:
        A BeautifulSoup object of the div with id 'scheduler' and class 'k-scheduler', or None if not found.
    """
    return soup.find("div", id="scheduler", class_="k-scheduler")

def find_scheduler_table(soup):
    """Finds and returns the table with role 'presentation' and class 'k-scheduler-table' from the soup object.

    Args:
        soup: A BeautifulSoup object representing the HTML content.

    Returns:
        A BeautifulSoup object of the table with class 'k-scheduler-table', or None if not found.
    """
    return soup.find("table", attrs={
                      "role": "presentation", "class": "k-scheduler-layout k-scheduler-undefinedview"})


def get_dates(soup):
    div = soup.find("div", class_="k-scheduler-header-wrap")
    ths = div.find_all("th")

    schedule_dates = [th.text.replace(
        "\n                                            ", " ")[3:] for th in ths]

    print(schedule_dates)
    return schedule_dates


def get_times(soup):
    div = soup.find("div", class_="k-scheduler-times")
    table = div.find("table", attrs={"role":"presentation", "class":"k-scheduler-table"})
    ths = table.find_all("th")

    schedule_times = [th.find("span").text for th in ths]

    print(schedule_times)
    return schedule_times


def get_available_time(soup):
    div = soup.find("div", class_="k-scheduler-content")
    table = div.find("table", attrs={"role":"presentation", "class":"k-scheduler-table"})
    rows = table.find_all("tr")

    availability_dict = []

    for row_index, row in enumerate(rows):
        cols = row.find_all("td")

        for col_index, col in enumerate(cols):
            if col.text.strip() != "":
                availability_dict.append({
                    "date": col_index,
                    "time": row_index,
                    "available": col.text.strip()
                })

    print(availability_dict)
    return availability_dict


def convert_datetime(year, dateStr, timeStr):
    """Converts a list of dates into a list of date objects.

    Args:
      year: The year of the date.
      dateStr: A date in the format "MonDec 18".
      timeStr: A time in the format "12:00 PM" or "2:00 PM.

    Returns:
      A datetime objects.
    """

    date_parts = dateStr.split(" ")
    monthStr = date_parts[0]
    dayStr = date_parts[1]

    # Convert month from string to number
    month = list(calendar.month_abbr).index(monthStr)

    # Combine date and time into a string
    date_time_str = f'{year}-{month}-{dayStr} {timeStr}'

    # Convert string to datetime object
    dt = datetime.strptime(date_time_str, '%Y-%m-%d %I:%M %p')

    return dt


def get_court_availability(soup):
    # Ensure 'soup' is defined and passed correctly
    if soup is None:
        raise ValueError("The 'soup' parameter cannot be None.")

    # Find the table element with the specified attributes
    table = find_scheduler_table(find_scheduler(find_scheduler_wrapper(soup)))
    # Assuming 'soup' is your BeautifulSoup object and 'table' is the extracted table element
    tr_list = [tr for tr in table.find("tbody").children if isinstance(tr, Tag) and tr.name == 'tr']
    table_header= tr_list[0]
    table_data = tr_list[1]

    schedule_dates = get_dates(table_header)
    schedule_times = get_times(table_data)
    availability_dict = get_available_time(table_data)

    for available in availability_dict:
        available['date'] = schedule_dates[available['date']]
        available['time'] = schedule_times[available['time']]
        print(f"{available['available']} {available['date']} {available['time']}")

    return availability_dict

def extract_verification_token(soup):
    # Find the form with the specified ID
    form = soup.find('form', id='AjaxAntiForgeryForm')
    if form:
        # Find the input element with the name '__RequestVerificationToken'
        token_input = form.find('input', {'name': '__RequestVerificationToken'})
        if token_input:
            return token_input.get('value')
    return None

