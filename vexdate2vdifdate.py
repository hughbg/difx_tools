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
    print("Usage: vexdat2vdifdate.py vex_date [seconds offset]")
    print("Example: vexdate2vdifdate.py 2000y001d00h00m00s 585")
    print()
    print("Usually you would get the arguments from a lines in a vex file in a 'scan'. Like these: ")
    print("\tstart=2000y001d00h00m00s; mode=lba3cm-2p-2IF; source=0208-512;")
    print("\tstation=Pa:    0 sec:  585 sec:  150.958 GB:   0 :       : 1;")
    print()
    print("Outputs ref_epoc and seconds_from_ref_epoch as integers, for use in fake VDIF")

    exit(1)

d = shift_time(sys.argv[1], shift)
input_date_as_str = d.strftime("%Y-%m-%d %H:%M:%S")
print("Input date including seconds (if any):", input_date_as_str)

ref_epoch = datetime.datetime(d.year, 1 if d.month<7 else 7, 1)
six_month_intervals = (ref_epoch.year-2000)*2+ref_epoch.month//6
print("ref_epoch (6 month intervals):", six_month_intervals, "(->", ref_epoch.strftime("%Y-%m-%d %H:%M:%S")+")")

diff = d-ref_epoch
seconds_from_ref_epoch = diff.days*24*60*60+diff.seconds
print("seconds_from_ref_epoch:", seconds_from_ref_epoch)

vdif_date = shift_time(ref_epoch, seconds_from_ref_epoch).strftime("%Y-%m-%d %H:%M:%S")
print("Check we get the date back from ref_epoch and seconds_from_ref_epoch:\n\t",
      vdif_date, "==", input_date_as_str+"?", vdif_date==input_date_as_str)



