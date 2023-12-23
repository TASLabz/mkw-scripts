from dolphin import event, gui, utils, savestate, memory
import Modules.mkw_utils as mkw_utils
import sys
from Modules.mkw_classes import RaceManager, RaceManagerPlayer, RaceState, TimerManager

def main():
    global counter
    counter = 0
    global listsave
    listsave = {}
    seter()

if __name__ == '__main__':
    main()



def seter():
    addr = TimerManager().addr
    l = addr+0x48
    c = memory.read_u32(l)
    memory.write_u32(l,c+60)

"""    
@event.on_savestateload
def on_state_load(fromSlot: bool, slot: int):
"""

@event.on_frameadvance
def on_frame_advance():
    pass
    #seter()

