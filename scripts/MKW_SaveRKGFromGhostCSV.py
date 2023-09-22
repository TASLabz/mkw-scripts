from dolphin import gui
from Modules import TTK_Lib

"""
MKW_SaveRKGFromGhostCSV

This script retrieves the inputs from the ghost csv and creates a ghost RKG file
"""

def main() -> None:
    gui.add_osd_message("Script started")
    
    # Get FrameSequence from csv
    input_sequence = TTK_Lib.getInputSequenceFromCSV(TTK_Lib.PlayerType.GHOST)
    
    if (input_sequence is None or len(input_sequence) == 0):
        gui.add_osd_message("No inputs read!")
        return
    
    TTK_Lib.getMetadataAndWriteToRKG(input_sequence, TTK_Lib.PlayerType.GHOST)

if __name__ == '__main__':
    main()
