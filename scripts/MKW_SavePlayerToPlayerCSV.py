from dolphin import gui
import TTK_Lib

"""
MKW_SavePlayerToPlayerCSV

This script takes the player's inputs and writes them to the player csv
"""

def main() -> None:
    gui.add_osd_message("Script started")
    
    # Convert internal RKG to input list
    input_sequence = TTK_Lib.readFullDecodedRKGData(TTK_Lib.PlayerType.PLAYER)
    
    if (input_sequence is None or len(input_sequence) == 0):
        gui.add_osd_message("No inputs read!")
        return
    
    TTK_Lib.writeToCSV(input_sequence, TTK_Lib.PlayerType.PLAYER)

if __name__ == '__main__':
    main()