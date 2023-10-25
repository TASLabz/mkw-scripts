from dolphin import gui
from Modules import ttk_lib

"""
save_ghost_to_player_csv

This script takes the current ghost's inputs and write them to the player csv
"""

def main() -> None:
    gui.add_osd_message("Script started")
    
    # Convert internal RKG to input list
    input_sequence = ttk_lib.read_full_decoded_rkg_data(ttk_lib.PlayerType.GHOST)
    
    if (input_sequence is None or len(input_sequence) == 0):
        gui.add_osd_message("No inputs read!")
        return
    
    ttk_lib.write_to_csv(input_sequence, ttk_lib.PlayerType.PLAYER)

if __name__ == '__main__':
    main()
