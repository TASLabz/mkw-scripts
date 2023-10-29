from . import mkw_translations

# when running undo_state_backup.py, creates up to backup_amount
# backup files for your race inputs while you are TASing
backup_amount = 10

# csvs that player and ghost inputs will be written to must be tucked
# inside a function because we want to support the course changing
def text_file_path(path_name: str) -> str:
    course = mkw_translations.course_slot_abbreviation()
    text_file_paths = {
        "Player": "MKW_Inputs/MKW_Player_Inputs_" + course + ".csv",
        "Ghost": "MKW_Inputs/MKW_Ghost_Inputs_" + course + ".csv",
        "Backup": "MKW_Inputs/Backups/" + course + "_" + "backup##.csv"
    }
    
    return text_file_paths[path_name]

# rkgs that player and ghost inputs will be written to
course = mkw_translations.course_slot_abbreviation()
rkg_file_path = {
    "Player": "MKW_Inputs/MKW_Player_Inputs_" + course + ".rkg",
    "Ghost": "MKW_Inputs/MKW_Ghost_Inputs_" + course + ".rkg"
}
