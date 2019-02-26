import re
import datetime
from math import sin, cos, sqrt, atan2, radians

def calc_dist(long_orig, lat_orig, long_dest, lat_dest):
    '''Calculate distance between 2 longitude latitude coordinates'''

    R = 6373.0  # approximate radius of earth in km
    c = 0.0

    try:
        lat1 = radians(float(lat_orig))
        lon1 = radians(float(long_orig))
        lat2 = radians(float(lat_dest))
        lon2 = radians(float(long_dest))

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
    except ValueError:
        pass

    return R * c

def get_weekday_from_datetime(dt_str):
    p = re.compile('[-T:]')
    origin_date = datetime.datetime(*map(int, p.split(dt_str)))
    return origin_date.weekday()