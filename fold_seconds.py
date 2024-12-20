import sys

frame_numbers = [[]]    # list of lists, each list is the frames in 1 second
frame_indexes = [[]]

file_frame_index = 0
for line in sys.stdin:
    l = line.split()
    frame_number = int(l[5])

    if frame_number == 0:
        frame_numbers.append([ (0, file_frame_index) ])
    else:
        frame_numbers[-1].append((frame_number, file_frame_index))


    file_frame_index += 1

if len(frame_numbers[0]) == 0:
    frame_numbers = frame_numbers[1:]

# Report
sec_index = 0
for sec in frame_numbers:
    if len(sec) > 0:
        num_frames_according_to_range = sec[-1][0]-sec[0][0]+1
        num_frames_present = len(sec)
        print("File frame index", sec[0][1], "-", sec[-1][1], " Frame range", sec[0][0], "-", sec[-1][0], " Num frames present", num_frames_present, " Frames missing within range", num_frames_according_to_range-num_frames_present)
