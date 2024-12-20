# Specify everything, make it obvious

sample_rate = 32    # megasamples per sec
bits_per_sample = 2
num_channels = 4
file_size = 320004096      # both bytes
header_size = 4096
bits_per_byte = 8

# Start calculating

data_size = file_size-header_size

# Number of bits for one sample for all channels
bits_one_sample = bits_per_sample*num_channels

# Number of bits per second
bits_one_second = sample_rate*1e6*bits_one_sample

# Number of bytes per second
bytes_one_second = bits_one_second/bits_per_byte

# Number of seconds in file
print("Number of seconds in file", data_size/bytes_one_second)


