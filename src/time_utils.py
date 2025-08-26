import pytz
from datetime import datetime

def parse_date(value: int) -> datetime:
    return pytz.UTC.localize(datetime.strptime(str(value), "%Y%m%d%H%M"))
