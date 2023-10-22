from dolphin import event, gui
from Modules import ttk_lib
from Modules.mkw_utils import frame_of_input
from Modules.framesequence import FrameSequence
from Modules.mkw_classes import RaceManager, RaceState

playerInputs = FrameSequence()
ghostInputs = FrameSequence()

"""
tas_toolkit

This script reads inputs from the player and ghost csv files, and applies them in-game
The inputs are reloaded on every state load
"""

@event.on_savestateload
def onStateLoad(is_slot, slot):
    playerInputs.readFromFile()
    ghostInputs.readFromFile()

@event.on_frameadvance
def onFrameAdvance():
    global playerInputs, ghostInputs
    frame = frame_of_input()
    state = RaceManager.state().value
    inputs_ready = state in (RaceState.COUNTDOWN.value, RaceState.RACE.value)

    ghostInput = ghostInputs[frame]
    if (ghostInput and inputs_ready):
        ttk_lib.writeGhostInputs(ghostInput)
    
    playerInput = playerInputs[frame]
    if (playerInput and inputs_ready):
        ttk_lib.writePlayerInputs(playerInput)

def main() -> None:
    # Load both the player and ghost input sequences
    global playerInputs, ghostInputs
    playerInputs = ttk_lib.getInputSequenceFromCSV(ttk_lib.PlayerType.PLAYER)
    ghostInputs = ttk_lib.getInputSequenceFromCSV(ttk_lib.PlayerType.GHOST)
    
    gui.add_osd_message(
        "TTK | Player: {} | Ghost: {}".format(
            len(playerInputs) > 0, len(ghostInputs) > 0
        )
    )
    

if __name__ == '__main__':
    main()
