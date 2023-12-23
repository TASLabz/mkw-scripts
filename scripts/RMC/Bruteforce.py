from dolphin import controller, event
from Modules import bruteforcer_lib as bfl
from Modules import mkw_utils as utils
from Modules.mkw_classes import RaceManager, RaceManagerPlayer, RaceState

def main():
    def ruleset(x):
        if x<250:
            return bfl.forward_rule
        return bfl.basic_rule
    
    iterset = lambda x : bfl.last_input_iterator
    
    global IptList
    IptList = bfl.InputList(ruleset, iterset)

    global ss_frequency
    ss_frequency = 60

    global distance_key
    distance_key = 0

    global delay_input
    delay_input = 1

    

if __name__ == '__main__':
    main()

def savename(frame):
    return str(frame)+'.rawsav'

        
@event.on_frameadvance
def on_frame_advance():
    frame = utils.frame_of_input()
    if RaceManager().state().value >= RaceState.COUNTDOWN.value and not utils.is_single_player():
        if utils.get_distance_ghost() <= distance_key :
            if frame%ss_frequency == 1:
                bfl.save(savename(frame))
            bfl.run_input(IptList[frame])
        else:
            modif_frame = IptList.update(frame-delay_input)
            frame_to_load = bfl.prevframe(modif_frame, ss_frequency)
            print(f"desync at {frame}, modifying input at {modif_frame}, loading {frame_to_load}")
            bfl.run_input(IptList[frame_to_load])
            bfl.load(savename(frame_to_load))
        #bfl.run_input2(bfl.forward)

        















    
