from datetime import datetime, date
import pytz

def type_handler(x):
    if isinstance(x, (date, datetime)):
        x = pytz.utc.localize(x)
        # TODO if desired timezone set use this line:
        # x = x.astimezone(tz)
        return x.isoformat()
    elif isinstance(x, bytearray):
        return x.decode('utf-8')
    raise TypeError("Unknown type")