import baseband
import sys

v = baseband.open(sys.argv[1])
print(v.info)

