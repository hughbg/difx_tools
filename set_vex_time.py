
from datetime import datetime, timedelta
import sys, math

# Functions ripped off from juliandate PyPi package

def __day_pct(h, m, sec, ms):
    s = sec + (ms / 1_000_000)
    return ((h * 3600 + m * 60 + s) / 86400) - 0.5

def from_gregorian(Y, M, D, H=0, m=0, sec=0, ms=0):
    """Return a Julian day for a Gregorian calendar date."""
    return (
        int((1461 * (Y + 4800 + int((M - 14) / 12))) / 4)
        + int((367 * (M - 2 - 12 * int((M - 14) / 12))) / 12)
        - int((3 * int((Y + 4900 + int((M - 14) / 12)) / 100)) / 4)
        + D
        - 32075
    ) + __day_pct(H, m, sec, ms)

# ---------------------------------------------



if len(sys.argv) > 2:
    print("Invalid args"); exit(1)
elif len(sys.argv) == 2:
    if sys.argv[1] == "-time_only":
        time_only = True
    else:
        print("Invalid args"); exit(1)
else:
    time_only = False

# Line from vheader like this:
#s = "seconds_from_ref_epoch 14067900 ref_epoch 48 data_frame_number 0 data_frame_length 8032 num_channels 2 bits_per_sample 2 thread_id 0"

# Just get the first line from vheader with data frame info

SEARCH_LIMIT_LINES = 10
counter = 0
for line in sys.stdin:  
    tokens = line.split()
    if tokens[0] == "seconds_from_ref_epoch":
        seconds_from_ref_epoch = int(tokens[1])
        ref_epoch = int(tokens[3])
        break

    counter += 1
    if counter >= SEARCH_LIMIT_LINES: break

if counter >= SEARCH_LIMIT_LINES:
    print("ERROR: Did not find VDIF frame info within first", SEARCH_LIMIT_LINES, "lines")
    exit()

# Time calculations

# Don't use timedelta for this bit because of leap years
# Start at 2000-01-01 00:00:00

num_full_years = ref_epoch//2
extra_6_months = ref_epoch%2
year = 2000+num_full_years
if extra_6_months == 1: month = "07"
else: month = "01"


vtime = datetime.strptime(str(year)+"-"+month+"-01 00:00:00", "%Y-%m-%d %H:%M:%S")

# Add seconds since then
vtime += timedelta(seconds=seconds_from_ref_epoch)

if time_only:
    print(vtime)
    exit()

START_TIME_DELTA = 30     # 5 minutes. Start difx this many seconds from now.
CORRELATION_TIME_SPAN = 60  # seconds

start_time = vtime+timedelta(seconds=START_TIME_DELTA)
stop_time = start_time+timedelta(seconds=CORRELATION_TIME_SPAN)

now = datetime.now()
print("Start difx running by:",  (now+timedelta(seconds=START_TIME_DELTA)).strftime("%H:%M:%S"))
print()

print(">Times for $EXPR:")
print("exper_nominal_start="+start_time.strftime("%Yy%jd%Hh%Mm%Ss"))
print("exper_nominal_stop="+stop_time.strftime("%Yy%jd%Hh%Mm%Ss"))

print(">Text segments needed for scan:")
# Like start=2000y001d00h00m00s
print("start="+start_time.strftime("%Yy%jd%Hh%Mm%Ss"))
# Like 0 sec:  585 sec:
print(f"0 sec:  {CORRELATION_TIME_SPAN} sec:")

# EOP MJD. Has to be 5. 
print(">EOP days for v2d file:")

( year, month, day, hour, minute, second, junk1, junk2, junk3 ) = start_time.timetuple()
start_mjd = int(from_gregorian(year, month, day, hour, minute, second)-2400000.5-1)  # 1 day before, MJD

for i in range(5):
    print(start_mjd+i)

# Edit the vex/v2d files -----------------
print("\nCreating files")
with open("from-stream-template.vex") as f:
    vex_lines = f.readlines()

for i in range(len(vex_lines)):
    vex_lines[i] = vex_lines[i].replace("_EXPR_NOMINAL_START_", start_time.strftime("%Yy%jd%Hh%Mm%Ss"))
    vex_lines[i] = vex_lines[i].replace("_EXPR_NOMINAL_STOP_", stop_time.strftime("%Yy%jd%Hh%Mm%Ss"))
    vex_lines[i] = vex_lines[i].replace("_START_SCAN_", start_time.strftime("%Yy%jd%Hh%Mm%Ss"))
    vex_lines[i] = vex_lines[i].replace("_SCAN_SECONDS_", str(CORRELATION_TIME_SPAN))

with open("from-stream.vex", "w") as f:
    f.writelines(vex_lines)

with open("from-stream-template.v2d") as f:
    v2d_lines = f.readlines()

for i in range(len(v2d_lines)):
    for j in range(5):
        v2d_lines[i] = v2d_lines[i].replace("_EOP"+str(j)+"_", str(start_mjd+j))
    
with open("from-stream.v2d", "w") as f:
    f.writelines(v2d_lines)
