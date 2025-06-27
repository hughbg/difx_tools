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
    print("Usage: vexdat2vdifdate.py vex_date [seconds offset]")
    print("Example: vexdate2vdifdate.py 2000y001d00h00m00s 585")
    print()
    print("Usually you would get the arguments from a lines in a vex file in a 'scan'. Like these: ")
    print("\tstart=2000y001d00h00m00s; mode=lba3cm-2p-2IF; source=0208-512;")
    print("\tstation=Pa:    0 sec:  585 sec:  150.958 GB:   0 :       : 1;")
    exit(1)

d = shift_time(sys.argv[1], shift)

print(d.strftime("%Y-%m-%d %H:%M:%S"))

