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
elif len(sys.argv) == 2:
    shift = 0
else:
    print("Usage: vexdat2vdifdate.py vex_date [seconds]")
    print("Example: vexdate2vdifdate.py 2012y289d00h00m00s 5851")
    exit(1)

d = shift_time(sys.argv[1], shift)

print(d.strftime("%Y-%m-%d %H:%M:%S"))

