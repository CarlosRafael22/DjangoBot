import pytz
from datetime import datetime

local_tz = pytz.timezone("America/Recife")


def now():
    utc_dt = datetime.utcfromtimestamp(date).replace(tzinfo=pytz.utc)
    local_dt = local_tz.normalize(utc_dt.astimezone(local_tz)).strftime('%Y-%m-%d %H:%M:%S')
    return local_dt




