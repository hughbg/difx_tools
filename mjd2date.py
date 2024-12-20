import juliandate as jd
import sys
from datetime import datetime

julian = float(sys.argv[1])+2400000.5
d = jd.to_gregorian(float(julian))
d = datetime(*d)
print(d.strftime("%Y-%m-%d %H:%M:%S"))

