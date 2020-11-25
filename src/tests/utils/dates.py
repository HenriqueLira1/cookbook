from datetime import datetime

UTC_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"


def get_date_time_now():
    date_time = datetime.now()
    date_time = date_time.strftime(UTC_FORMAT)
    return date_time
