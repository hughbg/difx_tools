import sys
from datetime import datetime, timedelta

if len(sys.argv) != 3:
    print("Usage: vdifdate2date.py ref_epoch seconds_from_ref_epoch")
    print("Example: vdifdate2date. py 0 585")
    print()
    print("The arguments are integers that would be in those fields in a VDIF header")
    print()
    print("Outputs: a date in readable format and in vex format")
    exit(1)

ref_epoch = int(sys.argv[1])
s_from_ref_epoch = int(sys.argv[2])
                     
num_full_years = ref_epoch//2
extra_6_months = ref_epoch%2
year = 2000+num_full_years
if extra_6_months == 1: month = "07"
else: month = "01"


vtime = datetime.strptime(str(year)+"-"+month+"-01 00:00:00", "%Y-%m-%d %H:%M:%S")

# Add seconds since then
vtime += timedelta(seconds=s_from_ref_epoch)

print(vtime, "\t", datetime.strftime(vtime, '%Yy%jd%Hh%Mm%Ss'))
