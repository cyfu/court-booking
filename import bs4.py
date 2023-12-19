import bs4
import datetime

with open("schedule.html", "r") as f:
    soup = bs4.BeautifulSoup(f, "html.parser")


def get_dates(soup):
    div = soup.find("div", class_="k-scheduler-header-wrap")
    ths = div.find_all("th")

    schedule_dates = [th.text for th in ths]

    print(schedule_dates)
    return schedule_dates

def get_time(soup):
    div = soup.find("div", class_="k-scheduler-times")
    ths = div.find_all("th")

    schedule_times = [th.find("span").text for th in ths]

    print(schedule_times)
    return schedule_times

def get_court_availability(soup):
    table = soup.find("table", {"class": "k-scheduler-table"})
    rows = table.find_all("tr")

    availability_dict = []

    for row_index, row in enumerate(rows):
        cols = row.find_all("td")

        for col_index, col in enumerate(cols):
            if col.text.strip() != "":
                availability_dict.append({
                    "time": row_index,
                    "date": col_index,
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

  dates_list = []
  date_parts = dateStr.split(" ")
  month = date_parts[1][0:3]
  day = date_parts[1][3:]
  datetime.datetime(year, int(month), int(day), )

  return dates_list

for available in availability_dict:
  dateStr = schedule_dates[available['date']]
  timeStr = schedule_times[available['time']]
  print(f"{available['available']} {dateStr} {timeStr}")
