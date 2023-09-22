from Modules import mkw_translations as trans

# when running MKW_UndoStateBackup.py, creates up to backupAmount
# backup files for your race inputs while you are TASing
backupAmount = 10

# csvs that player and ghost inputs will be written to must be tucked
# inside a function because we want to support the course changing
def textFilePath(pathName: str) -> str:
    course = trans.course_slot_abbreviation()
    textFilePaths = {
        "Player": "MKW_Inputs/MKW_Player_Inputs_" + course + ".csv",
        "Ghost": "MKW_Inputs/MKW_Ghost_Inputs_" + course + ".csv",
        "Backup": "MKW_Inputs/Backups/" + course + "_" + "backup##.csv"
    }
    
    return textFilePaths[pathName]

# rkgs that player and ghost inputs will be written to
course = trans.course_slot_abbreviation()
rkgFilePath = {
    "Player": "MKW_Inputs/MKW_Player_Inputs_" + course + ".rkg",
    "Ghost": "MKW_Inputs/MKW_Ghost_Inputs_" + course + ".rkg"
}
