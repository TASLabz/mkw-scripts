from dolphin import event, gui, utils
import Modules.agc_lib as lib
from Modules.mkw_classes import RaceManager, RaceState
import Modules.mkw_utils as mkw_utils
import os
from math import floor

def main():
    global filename
    filename = os.path.join(utils.get_script_dir(), r'AGC_Data\ghost.data')

    global delay
    delay = 2500

    global framedatalist
    global timerdata
    global metadata

    metadata, framedatalist, timerdata = lib.file_to_framedatalist(filename)

    timerdata.add_delay(delay)

    
if __name__ == '__main__':
    main()


@event.on_frameadvance
def on_frame_advance():
    racestate = RaceManager().state().value
    frame = mkw_utils.frame_of_input()
    delayed_frame = floor(delay)+frame
    decimal_delay = delay - floor(delay)

    metadata.write(lib.get_metadata_addr(1))
    
    timerdata.write_rkg(0)
    if 0 < delayed_frame+1 < len(framedatalist) and racestate >= RaceState.COUNTDOWN.value and not mkw_utils.is_single_player():
        
        #print(timerdata)
        f1 = lib.FrameData(string = str(framedatalist[delayed_frame])) #Makes a copy so you can modify f1 without affecting the framedatalist
        f2 = framedatalist[delayed_frame+1]
        f1.interpolate(f2, 1-decimal_delay, decimal_delay)
        f1.write(lib.get_addr(1))
    

