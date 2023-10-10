from dolphin import event, gui
from Modules import TTK_Lib
from Modules.mkw_utils import frame_of_input
from Modules.framesequence import FrameSequence
from Modules.mkw_classes import RaceManager, RaceState

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
    frame = frame_of_input()
    in_race = RaceManager.state().value >= RaceState.COUNTDOWN.value
    
    ghostInput = ghostInputs[frame]
    if (ghostInput and in_race):
        TTK_Lib.writeGhostInputs(ghostInput)

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
