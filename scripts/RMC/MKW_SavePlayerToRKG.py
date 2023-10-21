from dolphin import gui
from Modules import TTK_Lib

"""
MKW_SavePlayerToRKG

This script takes the player's inputs and writes them to a csv file and an rkg file.
"""

def main() -> None:
    gui.add_osd_message("Script started")
    
    # Convert internal RKG to input list
    input_sequence = TTK_Lib.readFullDecodedRKGData(TTK_Lib.PlayerType.PLAYER)
    
    if (input_sequence is None or len(input_sequence) == 0):
        gui.add_osd_message("No inputs read!")
        return
    
    TTK_Lib.writeToCSV(input_sequence, TTK_Lib.PlayerType.PLAYER)
    TTK_Lib.getMetadataAndWriteToRKG(input_sequence, TTK_Lib.PlayerType.PLAYER)

if __name__ == '__main__':
    main()
