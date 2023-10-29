from dolphin import event, gui
from Modules import ttk_lib
from Modules.mkw_utils import frame_of_input
from Modules.framesequence import FrameSequence
from Modules.mkw_classes import RaceManager, RaceState

ghost_inputs = FrameSequence()

"""
tas_toolkit_ghost_only

This script reads inputs from the ghost csv files, and applies it live in-game
The inputs are reloaded on every state load
"""

@event.on_savestateload
def on_state_load(is_slot, slot):
    ghost_inputs.read_from_file()

@event.on_frameadvance
def on_frame_advance():
    global ghost_inputs
    frame = frame_of_input()
    state = RaceManager.state().value
    inputs_ready = state in (RaceState.COUNTDOWN.value, RaceState.RACE.value)
    
    ghostInput = ghost_inputs[frame]
    if (ghostInput and inputs_ready):
        ttk_lib.write_ghost_inputs(ghostInput)

def main() -> None:
    # Load both the player and ghost input sequences
    global ghost_inputs
    ghost_inputs = ttk_lib.get_input_sequence_from_csv(ttk_lib.PlayerType.GHOST)
    
    gui.add_osd_message(
        "TTK | Player: {} | Ghost: {}".format(
            False, len(ghost_inputs) > 0
        )
    )
    

if __name__ == '__main__':
    main()
