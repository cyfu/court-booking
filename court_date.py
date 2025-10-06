import datetime

# Given timestamp in milliseconds
timestamp_ms = 1726444800000

# Convert milliseconds to seconds
timestamp_s = timestamp_ms / 1000

# Convert to a datetime object
date_time = datetime.datetime.fromtimestamp(timestamp_s)

# Format the date to a human-readable format
human_readable_date = date_time.strftime('%Y-%m-%d %H:%M:%S')

print(human_readable_date)
