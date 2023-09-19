from dolphin import controller, event, gui, memory, utils
import TTK_Lib
import mkw_classes as classes
import mkw_core as core
from framesequence import FrameSequence

playerInputs = FrameSequence()
ghostInputs = FrameSequence()

"""
MKW_TTK

This script reads inputs from the player and ghost csv files, and applies them live in-game
The inputs are reloaded on every state load
"""

@event.on_savestateload
def onStateLoad(is_slot, slot):
    playerInputs.readFromFile()
    ghostInputs.readFromFile()

@event.on_frameadvance
def onFrameAdvance():
    global playerInputs, ghostInputs
    frame = core.get_frame_of_input()
    
    ghostInput = ghostInputs[frame]
    if (ghostInput and classes.RaceInfo.stage() >= 1):
        TTK_Lib.writeGhostInputs(ghostInput)
    else:
        TTK_Lib.stopWriteGhostInputs()
    
    playerInput = playerInputs[frame]
    if (playerInput and classes.RaceInfo.stage() >= 1):
        controller.set_gc_buttons(0, playerInput.get_controller_inputs())

def main() -> None:
    # Load both the player and ghost input sequences
    global playerInputs, ghostInputs
    playerInputs = TTK_Lib.getInputSequenceFromCSV(TTK_Lib.PlayerType.PLAYER)
    ghostInputs = TTK_Lib.getInputSequenceFromCSV(TTK_Lib.PlayerType.GHOST)
    
    gui.add_osd_message("TTK | Player: {} | Ghost: {}".format(len(playerInputs) > 0, len(ghostInputs) > 0))
    

if __name__ == '__main__':
    main()