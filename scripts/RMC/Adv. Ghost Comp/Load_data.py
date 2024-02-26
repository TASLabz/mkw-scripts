from dolphin import event, utils
import Modules.agc_lib as lib
from Modules.mkw_classes import RaceManager, RaceState
import Modules.mkw_utils as mkw_utils
import os
from math import floor

def main():
    global filename
    filename = os.path.join(utils.get_script_dir(), r'AGC_Data\ghost.data')

    global delay
    delay = 0

    global framedatalist
    global timerdata
    global metadata
    global rkg_metadata

    metadata, framedatalist, timerdata, rkg_metadata = lib.file_to_framedatalist(filename)

    if timerdata is not None:
        timerdata.add_delay(delay)

    
if __name__ == '__main__':
    main()


@event.on_frameadvance
def on_frame_advance():
    racestate = RaceManager().state().value
    frame = mkw_utils.frame_of_input()
    delayed_frame = floor(delay)+frame
    decimal_delay = delay - floor(delay)

    if metadata is not None:
        metadata.write(lib.get_metadata_addr(1))
        
    if lib.is_rkg():   
        if rkg_metadata is not None:
            rkg_metadata.write(lib.get_rkg_metadata_addr())    
        #if not timerdata is None:
            #timerdata.write_rkg()

    in_frame_bounds = 0 < delayed_frame+1 < len(framedatalist)
    in_race = racestate >= RaceState.COUNTDOWN.value
    single_player = mkw_utils.is_single_player()

    if in_frame_bounds and in_race and not single_player:
        
        #print(timerdata)
        # Make a copy so you can modify f1 without affecting the framedatalist
        f1 = lib.FrameData(string = str(framedatalist[delayed_frame]))
        f2 = framedatalist[delayed_frame+1]
        f1.interpolate(f2, 1-decimal_delay, decimal_delay)
        f1.write(lib.get_addr(1))
    

