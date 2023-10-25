from dolphin import gui
from Modules import ttk_lib

"""
save_rkg_from_player_csv

This script retrieves the inputs from the player csv and creates a player RKG file
"""

def main() -> None:
    gui.add_osd_message("Script started")
    
    # Get FrameSequence from csv
    input_sequence = ttk_lib.get_input_sequence_from_csv(ttk_lib.PlayerType.PLAYER)
    
    if (input_sequence is None or len(input_sequence) == 0):
        gui.add_osd_message("No inputs read!")
        return
    
    ttk_lib.get_metadata_and_write_to_rkg(input_sequence, ttk_lib.PlayerType.PLAYER)

if __name__ == '__main__':
    main()
