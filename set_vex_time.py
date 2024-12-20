from datetime import datetime, timedelta
import sys

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


# Don't use timedelta for this bit because of leap years
# Start at 2000-01-01 00:00:00

num_full_years = ref_epoch//2
extra_6_months = ref_epoch%2
year = 2000+num_full_years
if extra_6_months == 1: month = "07"
else: month = "01"


vtime = datetime.strptime(str(year)+"-"+month+"-01 00:00:00", "%Y-%m-%d %H:%M:%S")

# Add seconds since then
vtime += +timedelta(seconds=seconds_from_ref_epoch)

print(vtime)

