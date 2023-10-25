from dolphin import gui
from Modules import ttk_lib

"""
save_player_to_rkg

This script takes the player's inputs and writes them to a csv file and an rkg file.
"""

def main() -> None:
    gui.add_osd_message("Script started")
    
    # Convert internal RKG to input list
    input_sequence = ttk_lib.read_full_decoded_rkg_data(ttk_lib.PlayerType.PLAYER)
    
    if (input_sequence is None or len(input_sequence) == 0):
        gui.add_osd_message("No inputs read!")
        return
    
    ttk_lib.write_to_csv(input_sequence, ttk_lib.PlayerType.PLAYER)
    ttk_lib.getMetadataAndWriteToRKG(input_sequence, ttk_lib.PlayerType.PLAYER)

if __name__ == '__main__':
    main()
