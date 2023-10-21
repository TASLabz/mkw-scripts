from dolphin import event, gui
from Modules import TTK_Lib
from Modules.mkw_utils import frame_of_input
from Modules.framesequence import FrameSequence
from Modules.mkw_classes import RaceManager, RaceState

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
    frame = frame_of_input()
    state = RaceManager.state().value
    inputs_ready = state in (RaceState.COUNTDOWN.value, RaceState.RACE.value)
    
    playerInput = playerInputs[frame]
    if (playerInput and inputs_ready):
        TTK_Lib.writePlayerInputs(playerInput)

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
