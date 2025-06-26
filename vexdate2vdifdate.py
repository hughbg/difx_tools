import sys
import datetime


def parse_date_time(dt):
    return datetime.datetime.strptime(dt, '%Yy%jd%Hh%Mm%Ss')


def shift_time(time_rep, seconds):
    if isinstance(time_rep, str):
        dt = parse_date_time(time_rep)
    else:
        dt = time_rep
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
input_date_as_str = d.strftime("%Y-%m-%d %H:%M:%S")
print("Input date including seconds (if any):", input_date_as_str)

ref_epoch = datetime.datetime(d.year, 1 if d.month<6 else 6, 1)
six_month_intervals = (ref_epoch.year-2000)*2+ref_epoch.month//6
print("ref_epoch (6 month intervals):", six_month_intervals, "=", ref_epoch.strftime("%Y-%m-%d %H:%M:%S"))

diff = d-ref_epoch
seconds_from_ref_epoch = diff.days*24*60*60+diff.seconds
print("seconds_from_ref_epoch:", seconds_from_ref_epoch)

vdif_date = shift_time(ref_epoch, seconds_from_ref_epoch).strftime("%Y-%m-%d %H:%M:%S")
print("Check we get the date back from ref_epoch and seconds_from_ref_epoch:\n\t",
      vdif_date, "==", input_date_as_str+"?", vdif_date==input_date_as_str)



