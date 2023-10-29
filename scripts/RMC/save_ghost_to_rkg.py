from dolphin import gui
from Modules import ttk_lib

"""
save_ghost_to_rkg

Takes the current ghost's inputs and writes them to a csv file and an rkg file.
"""

def main() -> None:
    gui.add_osd_message("Script started")
    
    # Convert internal RKG to input list
    input_sequence = ttk_lib.read_full_decoded_rkg_data(ttk_lib.PlayerType.GHOST)
    
    if (input_sequence is None or len(input_sequence) == 0):
        gui.add_osd_message("No inputs read!")
        return
    
    ttk_lib.write_to_csv(input_sequence, ttk_lib.PlayerType.GHOST)
    ttk_lib.get_metadata_and_write_to_rkg(input_sequence, ttk_lib.PlayerType.GHOST)

if __name__ == '__main__':
    main()
