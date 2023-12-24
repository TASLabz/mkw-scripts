from dolphin import event, gui, utils
import Modules.agc_lib as lib
from Modules.mkw_classes import RaceManager, RaceState
import Modules.mkw_utils as mkw_utils
import os


def main():
    global filename
    filename = os.path.join(utils.get_script_dir(), r'AGC_Data\ghost.data')

    global framedatalist
    framedatalist = {}

    global end
    end = False

    global metadata_saved
    metadata_saved = False
    
if __name__ == '__main__':
    main()


@event.on_frameadvance
def on_frame_advance():
    global framedatalist
    global end
    global metadata_saved
    
    racestate = RaceManager().state().value
    frame = mkw_utils.frame_of_input()

    if (not metadata_saved) and racestate >= RaceState.COUNTDOWN.value:
        lib.metadata_to_file(filename, 0)
        metadata_saved = True
    
    if (not end) and RaceState.RACE.value >= racestate >= RaceState.COUNTDOWN.value:
        framedatalist[frame] = lib.get_framedata(0)
        lib.frame_to_file(filename, 0)
        
    if (not end) and racestate == RaceState.FINISHED_RACE.value:
        lib.framedatalist_to_file(filename, framedatalist, 0)
        end = True
    
    
