import sys

vex_content = open(sys.argv[1]).readlines()
blocks = sys.argv[2].split()

for block in blocks:
    index = 0

    while index < len(vex_content):

        if vex_content[index].strip() == "$"+block+";":
            vex_content[index] = "\n"
            index += 1
            while index < len(vex_content) and vex_content[index][0] != "$":
                vex_content[index] = "\n"
                index += 1

        else:
            index += 1

for line in vex_content:
    print(line[:-1])
