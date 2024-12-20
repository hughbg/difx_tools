import sys, datetime
import matplotlib.pyplot as plt
import numpy as np

Vex = {}
vex_content = open(sys.argv[1]).readlines()

def parse_date_time(dt):
    return datetime.datetime.strptime(dt, '%Yy%jd%Hh%Mm%Ss')


# Utility function
def shift_time(time_str, seconds):
    dt = parse_date_time(time_str)
    tdelta = datetime.timedelta(seconds=seconds)
    print(dt+tdelta)




def parse_line(l):
    """
    x = 1
    x=1
    x= 1; x = 2
    ref x = 1
    """
    
    # May be multiple statements
    statements = l.strip().split(";")

    name_val_pairs = []
    
    for stment in statements:
        if len(stment) > 0:

            if stment[:3] == "ref":
                stment = stment[3:]

            name_val_pairs.append([ s.strip() for s in stment.split("=") ])

    return name_val_pairs


def read_def(ind, END):


    name = vex_content[ind].strip()[:-1].split()[1]
    #print(END[3:-1], name)
    new_def = {}

    ind += 1
    while ind < len(vex_content) and vex_content[ind][:-1].strip() != END:
        line = vex_content[ind].strip()[:-1]

        # Get rid of trailing comment
        i = line.find("*")
        if i > -1: line = line[:i]

        if len(line) > 0:
            
            statements = parse_line(line)

            for stment in statements:

                if stment[0] in new_def:
                    new_def[stment[0]] = new_def[stment[0]]+" | "+stment[1]
                else:
                    new_def[stment[0]] = stment[1]

        ind += 1

    return ind, name, new_def

def read_block(ind):
    
    def dict_store(key, val):
        if key in Vex[name]:
            assert not isinstance(val, dict), "Something wrong"
            Vex[name][key] = Vex[name][key]+" | "+val
        else:
            Vex[name][key] = val
            
    # A block usually has defs in it but the global block has a ref

    name = vex_content[ind].strip()[:-1]
    #print("block", name)
    Vex[name] = {}

    ind += 1
    while ind < len(vex_content) and vex_content[ind][0] != "$":
        line = vex_content[ind].strip()[:-1]

        # Get rid of trailing comment
        i = line.find("*")
        if i > -1: line = line[:i]
        
            
        if len(line) > 0:

            if line[:3] == "def":
                ind, def_name, new_def = read_def(ind, "enddef;")
                Vex[name][def_name] = new_def
            elif line[:4] == "scan":
                ind, def_name, new_def = read_def(ind, "endscan;")
                Vex[name][def_name] = new_def
            else:
                statements = parse_line(line)

                for st in statements:
                    Vex[name][st[0]] = st[1]


        ind += 1

    return ind

def unpack_block_assignment(block, name):
    """
    e.g.
    ref $IF = LO@7800MHzDPolNoTone:At:Mp;
    ref $IF = LO@7000MHzDPolNoTone:Cd;
    
    They go into one $IF entry with vals separated by |
    The vals are pointers to function defs so replace them with the function.
    Return whole lot in dict.
    """
    def strip_qual(s):
        s = s.split(":")[0]
        return s.strip()
    
    new_dict = {}
    
    names = [ strip_qual(n) for n in name.split("|") ]
    for name in names:
        assert name in Vex[block], name + " not in block "+block
        new_dict[name] = Vex[block][name]

    return new_dict

def timings(find_time=None):
    
    def parse_date_time(dt):
        return datetime.datetime.strptime(dt, '%Yy%jd%Hh%Mm%Ss') 
        

    stations = Vex["$STATION"].copy()
    for key in stations:
        # Each station has a list of tuples that indicate a time interval from time 0
        # time 0 is the start_time specified in scan No0001
        stations[key] = []

    if find_time is not None:
        print("Searching for entered time", parse_date_time(find_time))

    start_i = 1e39
    finish_i = -1
    for key in Vex["$SCHED"]:
        counter = int(key[2:].replace("0", ""))
        start_i = min(start_i, counter)
        finish_i = max(finish_i, counter)

    # start_i is the number of the scan that is the first scan in order of number.
    # Usually 1. But if scans start with number 5 it will be 5. Am assuming the scans
    # are numbered so they are ordered by time.
        
    for i in range(start_i, finish_i+1):
        scan = "No"+f'{i:04}'
        dt = parse_date_time(Vex["$SCHED"][scan]["start"])
        
        # scan_start is the number of seconds from start_time which is start of the first scan
        # scan_start is in seconds, and is the beginning of another scan
        if i == start_i:
            start_time = dt               # the start time of the whole observing run
            if find_time is not None:
                find_time = (parse_date_time(find_time)-start_time).seconds
            scan_start = 0
            the_very_end = 0
        else:
            scan_start = (dt-start_time).seconds
            
        stations_info = [ p.strip() for p in Vex["$SCHED"][scan]["station"].split("|") ]
        for s in stations_info:
            params = [ p.strip() for p in s.split(":") ]

            which_station = params[0]
            data_good_start = int(params[1].split()[0])
            data_good_finish = int(params[2].split()[0])
            
            stations[which_station].append((scan_start+data_good_start, scan_start+data_good_finish))
            
            the_very_end = max(the_very_end, scan_start+data_good_finish)

            if find_time is not None:
                if scan_start+data_good_start <= find_time and find_time <= scan_start+data_good_finish != 0:

                    print("Scan", scan, "| Station", which_station, "| Start", dt,
                          "| Good", dt+datetime.timedelta(seconds=data_good_start), "->", dt+datetime.timedelta(seconds=data_good_finish))


            
    
    plt.figure(figsize=(16, 4))

    for i, s in enumerate(stations):
        data = np.zeros(the_very_end)
        for etimes in stations[s]:
            data[etimes[0]:etimes[1]] = 4-i/2

        data = np.ma.masked_equal(data, 0)

        
        plt.plot(np.arange(len(data))/3600, data, lw=0.6, label=s)

    exp_def = Vex["$GLOBAL"]["$EXPER"]
    nominal_start = parse_date_time(Vex["$EXPER"][exp_def]["exper_nominal_start"])-start_time;
    nominal_stop = parse_date_time(Vex["$EXPER"][exp_def]["exper_nominal_stop"])-start_time;

    plt.axvline(nominal_start.seconds/3600, color="gray",lw=0.4)
    plt.axvline(nominal_stop.seconds/3600, color="gray",lw=0.4)

    plt.title("Observation times for all telescopes (good data)")
    plt.xlabel("Time from start of first scan [hr]")
    plt.yticks([])
    plt.legend()
    plt.xlim(-1000/3600, the_very_end*1.1/3600)
    #plt.show()
                         

def station_freq_info(station):

    def if_info(ifl, ifd):
        print("    Intermediate frequency:")
        for key in Vex["$IF"][ifd]:
            if_defs = Vex["$IF"][ifd][key].split("|")

            for ifs in if_defs:
                params = [ p.strip() for p in ifs.split(":") ]

                if params[0] == ifl:
                    print("        Polarization:", "right" if params[2] == "R" else "left")
                    print("        Total effective local oscillator:", params[3])
                    print("        Net sideband:", "upper" if params[4] == "U" else "lower")

    def channel_info(ch, sr):
        ch = [ s.strip() for s in ch.strip().split(":") if len(s) > 0 ]
        print("  Channel")
        print("    RF sky freq at 0Hz in the baseband output:", ch[0])
        print("    Net sideband of this baseband channel:", "upper" if ch[1] == "U" else "lower")
        print("    Baseband channel bandwidth:", ch[2])
        print("    Sample rate:", sr)
        
        # Find the $BBC and $IF that apply to this station

        bbc_def = if_def = ""
        for key in Vex["$MODE"]:
            for key1 in Vex["$MODE"][key]:            
                if key1 == "$BBC":
                    for bbc_defs in Vex["$MODE"][key][key1].split("|"):
                        stations = bbc_defs.strip().split(":")[1:]
                        if station in stations:
                            bbc_def = bbc_defs.strip().split(":")[0]
                if key1 == "$IF":
                    for if_defs in Vex["$MODE"][key][key1].split("|"):
                        stations = if_defs.strip().split(":")[1:]
                        if station in stations:
                            if_def = if_defs.split(":")[0].strip()
                            


        # find what IF the BBC in this channel links to what IF
        
        for bbc_assign in Vex["$BBC"][bbc_def]:
            for statement in Vex["$BBC"][bbc_def][bbc_assign].split("|"):
                params = [ s.strip() for s in statement.strip().split(":") if len(s) > 0 ]
                if ch[4] == params[0]:
                    if_link = params[2]
                    if_info(if_link, if_def)

        
        
    
    # station is 2-letter code
    for key in Vex["$STATION"]:
        if key == station:
            for key1 in Vex["$STATION"][key]:
                if key1 == "$SITE":
                    station_name = Vex["$STATION"][key]["$SITE"]
                    
    print(station_name)
    
    station_freq_def = ""
    for key in Vex["$MODE"]:
        for key1 in Vex["$MODE"][key]:
            if key1 == "$FREQ":
                for freq_defs in Vex["$MODE"][key][key1].split("|"):
                    stations = freq_defs.strip().split(":")[1:]
                    if station in stations:
                        station_freq_def = freq_defs.strip().split(":")[0]
                        
    # Now we have freq info
    assert len(station_freq_def) > 0
    
    for key in Vex["$FREQ"]:
        if key == station_freq_def:
            for key1 in Vex["$FREQ"][station_freq_def]:
                if key1 == "sample_rate":
                    sample_rate = Vex["$FREQ"][station_freq_def][key1]
                elif key1 == "chan_def":
                    channels = Vex["$FREQ"][station_freq_def][key1].split("|")
                    for ch in channels:
                        channel_info(ch, sample_rate)
                
                
                

def find_name(v, name, prefix=''):
    # Walk the values
    if isinstance(v, dict):
        for k, v2 in v.items():
            p2 = prefix+("" if len(prefix)==0 else ".")+k
            if k == name:
                print(p2+"="+("<dict>" if isinstance(v2, dict) else str(v2)))
                
            if k[0] == "$" and isinstance(v2, str):

                # This is where a block name is assigned to. There could be multiple assignments.     
                v2 = unpack_block_assignment(k, v2)
                
            find_name(v2, name, p2)
    else:
        # v is a string
        if v == name:
            print(prefix+"="+name)


index = 0



while index < len(vex_content):

    if vex_content[index][0] == "$":
        index = read_block(index)

    if index < len(vex_content) and vex_content[index][0] != "$":
        index += 1

for site in [ "At" ]: #, "At", "Mp", "Ho", "Cd", "Hh" ]:
    station_freq_info(site)


timings(find_time="2008y161d01h28m50s")

