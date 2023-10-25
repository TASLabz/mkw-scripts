from dolphin import event, gui
from Modules import ttk_lib
from Modules.mkw_utils import frame_of_input
from Modules.framesequence import FrameSequence
from Modules.mkw_classes import RaceManager, RaceState

player_inputs = FrameSequence()

"""
tas_toolkit_player_only

This script reads inputs from the player csv files, and applies it live in-game
The inputs are reloaded on every state load
"""

@event.on_savestateload
def on_state_load(is_slot, slot):
    player_inputs.read_from_file()

@event.on_frameadvance
def on_frame_advance():
    global player_inputs
    frame = frame_of_input()
    state = RaceManager.state().value
    inputs_ready = state in (RaceState.COUNTDOWN.value, RaceState.RACE.value)
    
    player_input = player_inputs[frame]
    if (player_input and inputs_ready):
        ttk_lib.write_player_inputs(player_input)

def main() -> None:
    # Load both the player and ghost input sequences
    global player_inputs
    player_inputs = ttk_lib.get_input_sequence_from_csv(ttk_lib.PlayerType.PLAYER)
    
    gui.add_osd_message(
        "TTK | Player: {} | Ghost: {}".format(
            len(player_inputs) > 0, False
        )
    )
    

if __name__ == '__main__':
    main()
