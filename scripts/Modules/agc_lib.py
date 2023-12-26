from dolphin import gui, memory
from .mkw_classes import vec3
from .mkw_classes import VehiclePhysics, KartMove, RaceConfig, RaceManagerPlayer
import math

class FrameData:
    """Class to represent a set of value accessible each frame in the memory"""
    def __init__(self, addrlist = None, string = None , usedefault=False):
        self.values = [] #List of bytearray
        if string is not None:
            self.read_from_string(string)
            
        elif addrlist is not None:
            if not usedefault:
                for addr, size in addrlist:
                    self.values.append(memory.read_bytes(addr, size))          
            else:
                for addr, size in addrlist:
                    self.values.append(bytearray(size))

    def __str__(self):
        text = ''
        for array in self.values:
            for byte in array:
                text += str(byte)+','
            if len(array)>0:
                text = text[:-1]
            text += ';'
        if len(self.values)>0:
            text = text[:-1]
        return text+'\n'

    def read_from_string(self, string):
        values = string.split(';')
        for value in values:
            self.values.append(bytearray([int(s) for s in value.split(',')]))

    def interpolate(self,other, selfi, otheri):
        #Call only if self.value[0] represent a vec3
        v1 = vec3.from_bytes(self.values[0])
        v2 = vec3.from_bytes(other.values[0])
        v = (v1*selfi)+(v2*otheri)
        self.values[0] = v.to_bytes()

    def write(self, addrlist):
        for index in range(len(self.values)):
            addr = addrlist[index][0]
            val = self.values[index]
            memory.write_bytes(addr, val)

def float_to_str(f):
    ms = round((f%1)*1000)
    s = math.floor(f)%60
    m = math.floor(f)//60
    return f"{m},{s},{ms}"

def floats_to_str(fs):
    return f"{float_to_str(fs[0])};{float_to_str(fs[1])};{float_to_str(fs[2])}"

class Split:
    """Class for a lap split. Contain just a float, representing the split in s"""
    def __init__(self, f):
        self.val = f
    def __str__(self):
        return f"{self.val:.3f}"
    def __add__(self,other):
        return Split(max(0, self.val+other.val)) 

    @staticmethod
    def from_string(string):
        return Split(float(string))

    @staticmethod
    def from_time_format(m,s,ms):
        return Split(m*60+s+ms/1000)
    
    @staticmethod
    def from_bytes(b):
        data_int = b[0]*256*256+b[1]*256+b[2]
        ms = data_int%1024
        data_int = data_int//1024
        s = data_int%128
        data_int = data_int//128
        m = data_int%128
        return Split(m*60+s+ms/1000)
    
    def time_format(self):
        #return m,s,ms corresponding
        f = self.val
        ms = round((f%1)*1000)
        s = math.floor(f)%60
        m = math.floor(f)//60
        return m,s,ms
    
    def bytes_format(self):
        #return a bytearray of size 3 for rkg format
        m,s,ms = self.time_format()
        data_int = ms+s*1024+m*1024*128
        b3 = data_int%256
        data_int = data_int//256
        b2 = data_int%256
        data_int = data_int//256
        b1 = data_int%256
        return bytearray((b1,b2,b3))


class TimerData:
    """Class for the laps splits, both in RKG and Timer format
        Cumulative convention (lap2 split is stored as lap1+lap2)"""
    def __init__(self,string =None, readid=0, splits = None):
        #Call with a string OR when the race is finished
        if string is None:
            if splits is None:
                self.splits = [] #List of Split (size 3)
                timerlist = [RaceManagerPlayer.lap_finish_time(readid, lap) for lap in range(3)]
                for timer in timerlist:
                    self.splits.append(Split.from_time_format(timer.minutes(), timer.seconds(), timer.milliseconds()))
            else:
                self.splits = splits
        else:
            self.splits = []
            laps = string.split(';')
            for lap in laps:
                self.splits.append(Split.from_string(lap))

    @staticmethod
    def from_sliced_rkg(rkg_metadata):
        sliced_bytes = rkg_metadata.values[3]
        l1 = Split.from_bytes(sliced_bytes[1:4])
        l2 = Split.from_bytes(sliced_bytes[4:7])+l1
        l3 = Split.from_bytes(sliced_bytes[7:10])+l2
        return TimerData(splits = [l1,l2,l3])

    def __str__(self):
        text = 't'
        for split in self.splits:
            text += str(split)+";"
        text = text[:-1]
        return text+'\n'

    def add_delay(self, delay):
        s = -delay/59.94
        for i in range(len(self.splits)):
            self.splits[i] = Split(max(self.splits[i].val+s, 0))


    def to_bytes(self):
        #A lap split is 3 bytes, so there is 9 bytes total
        #Non cumulative format, ready to be written in a rkg
        r = bytearray()
        prev = 0
        for split in self.splits:
            r = r + Split(split.val - prev).bytes_format()
            prev = split.val
        return r
    
    def write_rkg(self):
        r = rkg_addr()
        memory.write_bytes(r+0x11, self.to_bytes())
            
                 
def metadata_to_file(filename, readid):
    #Should be called before the countdown
    metadata = FrameData(get_metadata_addr(readid))
    file = open(filename, 'w')
    if file is None :
        gui.add_osd_message("Error : could not create the data file")
    else :
        file.write(str(metadata))
        file.close()
        gui.add_osd_message(f"{filename} successfully opened")

def get_metadata(readid):
    return FrameData(get_metadata_addr(readid))

def get_rkg_metadata():
    return FrameData(get_rkg_metadata_addr())

def rkg_metadata_to_file(filename):
    rkg_metadata = get_rkg_metadata()
    file = open(filename, 'w')
    if file is None :
        gui.add_osd_message("Error : could not create the data file")
    else :
        file.write("r"+str(rkg_metadata))
        file.close()
        gui.add_osd_message(f"{filename} successfully opened")   

def frame_to_file(filename, readid):
    frame = FrameData(get_addr(readid))
    file = open(filename, 'a')
    if file is None :
        gui.add_osd_message("Error : could not create the data file")
    else :
        file.write(str(frame))
        file.close()

def get_framedata(readid):
    return FrameData(get_addr(readid))
    
def timerdata_to_file(filename, read_id):
    timerdata = TimerData(read_id)
    file = open(filename, 'a')
    if file is None :
        gui.add_osd_message("Error : could not create the data file")
    else :
        file.write(str(timerdata))
        file.close()

def get_timerdata(read_id):
    return TimerData(read_id)
        
def file_to_framedatalist(filename):
    datalist = []
    file = open(filename, 'r')
    if file is None :
        gui.add_osd_message("Error : could not load the data file")
    else:
        timerdata = None
        metadata = None
        rkg_metadata = None
        listlines = file.readlines()
        if listlines[0][0] == 'r':           
            rkg_metadata = FrameData(string = listlines[0][1:])
            timerdata = TimerData.from_sliced_rkg(rkg_metadata)
        else:
            metadata = FrameData(string = listlines[0])
            if listlines[-1][0]=='t':
                timerdata = TimerData(string = listlines.pop()[1:])
        for i in range(1, len(listlines)):
            datalist.append(FrameData(string = listlines[i]))
        file.close()
        gui.add_osd_message(f"Data successfully loaded from {filename}")
        return metadata, datalist, timerdata, rkg_metadata


def framedatalist_to_file(filename, datalist, read_id):
    metadata = get_metadata(read_id)
    timerdata = get_timerdata(read_id)
    file = open(filename, 'w')
    if file is None :
        gui.add_osd_message("Error : could not create the data file")
    else:
        file.write(str(metadata))
        for frame in range(max(datalist.keys())+1):
            if frame in datalist.keys():
                file.write(str(datalist[frame]))
            else:
                file.write(str(FrameData(get_addr(rid), usedefault=True)))
        file.write(str(timerdata))
        file.close()

def framedatalist_to_file_rkg(filename, datalist):
    metadata = get_rkg_metadata()
    file = open(filename, 'w')
    if file is None :
        gui.add_osd_message("Error : could not create the data file")
    else:
        file.write('r'+str(metadata))
        for frame in range(max(datalist.keys())+1):
            if frame in datalist.keys():
                file.write(str(datalist[frame]))
            else:
                file.write(str(FrameData(get_addr(rid), usedefault=True)))
        file.close()


def get_addr(player_id):
    a = VehiclePhysics.chain(player_id)
    b = KartMove.chain(player_id)
    return [(a+0x68, 12), #Position
            (a+0xF0, 16), #Rotation
            (a+0x74, 12), #EV
            (a+0x14C, 12), #IV
            (b+0x18, 4), #MaxEngineSpd
            (b+0x20, 4), #EngineSpd
            (b+0x9C, 4), #OutsideDriftAngle
            (b+0x5C, 12)]#Dir

def get_metadata_addr(player_id):
    a = RaceConfig.chain() + player_id*0xF0
    return [(a+0x30, 8)]#CharacterID and VehicleID

def rkg_addr():
    return memory.read_u32(RaceConfig.chain() + 0xC0C)

def get_rkg_metadata_addr():
    r = rkg_addr()
    return [(r+0x4, 3), #Skipping track ID
            (r+0x8, 4), #Skipping Compression flag
            (r+0xD, 1), #Skipping Input Data Length
            (r+0x10, 0x78)]

def is_rkg():
        s = bytearray('RKGD', 'ASCII')
        r = rkg_addr()
        return s == memory.read_bytes(r, 4)    
