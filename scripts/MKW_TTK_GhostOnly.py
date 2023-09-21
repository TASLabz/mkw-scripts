from dolphin import event, gui
from Modules import TTK_Lib, mkw_classes as classes, mkw_core as core
from Modules.framesequence import FrameSequence

ghostInputs = FrameSequence()

"""
MKW_TTK_GhostOnly

This script reads inputs from the ghost csv files, and applies it live in-game
The inputs are reloaded on every state load
"""

@event.on_savestateload
def onStateLoad(is_slot, slot):
    ghostInputs.readFromFile()

@event.on_frameadvance
def onFrameAdvance():
    global ghostInputs
    frame = core.get_frame_of_input()
    
    ghostInput = ghostInputs[frame]
    if (ghostInput and classes.RaceInfo.stage() >= 1):
        TTK_Lib.writeGhostInputs(ghostInput)
    else:
        TTK_Lib.stopWriteGhostInputs()

def main() -> None:
    # Load both the player and ghost input sequences
    global ghostInputs
    ghostInputs = TTK_Lib.getInputSequenceFromCSV(TTK_Lib.PlayerType.GHOST)
    
    gui.add_osd_message(
        "TTK | Player: {} | Ghost: {}".format(
            False, len(ghostInputs) > 0
        )
    )
    

if __name__ == '__main__':
    main()
