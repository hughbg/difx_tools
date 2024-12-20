import baseband
import sys, datetime
import math

def print_numbers(start_time, stop_time):
    # Times are astropy.Time object

    seconds_elapsed = int(math.ceil((stop_time-start_time).value*24*60*60))

    print(">Times for $EXPR:")
    print("exper_nominal_start="+start_time.strftime("%Yy%jd%Hh%Mm%Ss"))
    print("exper_nominal_stop="+stop_time.strftime("%Yy%jd%Hh%Mm%Ss"))

    print(">Segments needed for scan:")
    # Like start=2000y001d00h00m00s
    print("start="+start_time.strftime("%Yy%jd%Hh%Mm%Ss"))
    # Like 0 sec:  585 sec:
    print(f"0 sec:  {seconds_elapsed} sec:")

    # EOP MJD. Has to be 5. 
    print(">EOP days for v2d file:")
    start_mjd = int(math.trunc(start_time.jd-2400000.5-1))    # 1 day before, MJD
    for i in range(5):
        print(start_mjd+i)

earliest_start_time = None
latest_stop_time = None

for f in sys.argv[1:]:
    print("File", f, "--------------------")

    v = baseband.open(f)

    # Update bracketing times
    if earliest_start_time is None:
        earliest_start_time = v.start_time
    else:
        if v.start_time < earliest_start_time: earliest_start_time = v.start_time 
    if latest_stop_time is None:
        latest_stop_time = v.stop_time
    else: 
        if latest_stop_time < v.stop_time: latest_stop_time = v.stop_time

    print_numbers(v.start_time, v.stop_time)
    v.close()

if len(sys.argv) > 2:
    print("Overall ---------------------------")
    print_numbers(earliest_start_time, latest_stop_time)


