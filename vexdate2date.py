import sys
import datetime


def parse_date_time(dt):
    return datetime.datetime.strptime(dt, '%Yy%jd%Hh%Mm%Ss')


def shift_time(time_str, seconds):
    dt = parse_date_time(time_str)
    tdelta = datetime.timedelta(seconds=seconds)
    return dt+tdelta


if len(sys.argv) == 3:
    shift = float(sys.argv[2])
else:
    shift = 0

d = shift_time(sys.argv[1], shift)

print(d.strftime("%Y-%m-%d %H:%M:%S"))

