import mkw_translations as trans

# uses R button instead of B button to drift when enabled
useRbutton = True

# modifies input ranges defined in framesequence.py to match the symmetrical full input range code for keyboard TASers
useKeyboardRanges = False

# when running MKW_UndoStateBackup.py, creates up to backupAmount backup files for your race inputs while you are TASing
backupAmount = 10

# csvs that player and ghost inputs will be written to
# must be tucked inside a function because we want to support the course changing
def textFilePath(pathName: str) -> str:
    textFilePaths = {
        "Player": "MKW_Inputs/MKW_Player_Inputs_" + trans.course_slot_abbreviation() + ".csv",
        "Ghost": "MKW_Inputs/MKW_Ghost_Inputs_" + trans.course_slot_abbreviation() + ".csv",
        "Backup": "MKW_Inputs/Backups/" + trans.course_slot_abbreviation() + "_" + "backup##.csv"
    }
    
    return textFilePaths[pathName]

# rkgs that player and ghost inputs will be written to
rkgFilePath = {
    "rkgFilePathPlayer": "MKW_Inputs\\MKW_Player_Inputs_" + trans.course_slot_abbreviation() + ".rkg",
	"rkgFilePathGhost": "MKW_Inputs\\MKW_Ghost_Inputs_" + trans.course_slot_abbreviation() + ".rkg",
}