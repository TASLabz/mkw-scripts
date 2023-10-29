from dolphin import event, gui
from Modules import ttk_lib
from Modules.mkw_utils import frame_of_input
from Modules.framesequence import FrameSequence
from Modules.mkw_classes import RaceManager, RaceState

player_inputs = FrameSequence()
ghost_inputs = FrameSequence()

"""
tas_toolkit

This script reads inputs from the player and ghost csv files, and applies them in-game
The inputs are reloaded on every state load
"""

@event.on_savestateload
def on_state_load(is_slot, slot):
    player_inputs.read_from_file()
    ghost_inputs.read_from_file()

@event.on_frameadvance
def on_frame_advance():
    global player_inputs, ghost_inputs
    frame = frame_of_input()
    state = RaceManager.state().value
    inputs_ready = state in (RaceState.COUNTDOWN.value, RaceState.RACE.value)

    ghost_input = ghost_inputs[frame]
    if (ghost_input and inputs_ready):
        ttk_lib.write_ghost_inputs(ghost_input)
    
    player_input = player_inputs[frame]
    if (player_input and inputs_ready):
        ttk_lib.write_player_inputs(player_input)

def main() -> None:
    # Load both the player and ghost input sequences
    global player_inputs, ghost_inputs
    player_inputs = ttk_lib.get_input_sequence_from_csv(ttk_lib.PlayerType.PLAYER)
    ghost_inputs = ttk_lib.get_input_sequence_from_csv(ttk_lib.PlayerType.GHOST)
    
    gui.add_osd_message(
        "TTK | Player: {} | Ghost: {}".format(
            len(player_inputs) > 0, len(ghost_inputs) > 0
        )
    )
    

if __name__ == '__main__':
    main()
