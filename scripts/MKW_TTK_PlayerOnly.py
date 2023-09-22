from dolphin import controller, event, gui
from Modules import TTK_Lib, mkw_classes as classes, mkw_core as core
from Modules.framesequence import FrameSequence

playerInputs = FrameSequence()

"""
MKW_TTK_PlayerOnly

This script reads inputs from the player csv files, and applies it live in-game
The inputs are reloaded on every state load
"""

@event.on_savestateload
def onStateLoad(is_slot, slot):
    playerInputs.readFromFile()

@event.on_frameadvance
def onFrameAdvance():
    global playerInputs
    frame = core.get_frame_of_input()
    
    playerInput = playerInputs[frame]
    if (playerInput and classes.RaceInfo.stage() >= 1):
        controller.set_gc_buttons(0, playerInput.get_controller_inputs())

def main() -> None:
    # Load both the player and ghost input sequences
    global playerInputs
    playerInputs = TTK_Lib.getInputSequenceFromCSV(TTK_Lib.PlayerType.PLAYER)
    
    gui.add_osd_message(
        "TTK | Player: {} | Ghost: {}".format(
            len(playerInputs) > 0, False
        )
    )
    

if __name__ == '__main__':
    main()
