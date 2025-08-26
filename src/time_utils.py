import pytz
import datetime

def parse_date(value: str) -> datetime.datetime:
    return pytz.UTC.localize(datetime.strptime(value, "%Y%m%d%H%M"))
