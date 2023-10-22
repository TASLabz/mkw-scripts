from dolphin import gui
from Modules import ttk_lib

"""
save_rkg_from_ghost_csv

This script retrieves the inputs from the ghost csv and creates a ghost RKG file
"""

def main() -> None:
    gui.add_osd_message("Script started")
    
    # Get FrameSequence from csv
    input_sequence = ttk_lib.getInputSequenceFromCSV(ttk_lib.PlayerType.GHOST)
    
    if (input_sequence is None or len(input_sequence) == 0):
        gui.add_osd_message("No inputs read!")
        return
    
    ttk_lib.getMetadataAndWriteToRKG(input_sequence, ttk_lib.PlayerType.GHOST)

if __name__ == '__main__':
    main()
