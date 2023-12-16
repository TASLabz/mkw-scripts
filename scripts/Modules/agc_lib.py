from dolphin import gui
from .mkw_classes import quatf, vec3
import Modules.mkw_utils as mkw_utils
from .mkw_classes import VehiclePhysics, KartMove

def data_to_csv(data, csvfilename):
    """Parameter :  dictionnary data
                    string csvfilename
        data[i] should be another dictionnary with the key :
        "Pos" (vec3) ; "Qua" (quatf) ; "IV" (vec3) ; "EV" (vec3);
        "BaseSpd" (float) ; "MaxSpd" (float) ; "Angle" (float) ;
        "Dire" (vec3) ; "Dive" (float).
        data["charaID"] and data["vehicleID"] should be intergers."""
    
    file = open(csvfilename, 'w')
    if file is None :
        gui.add_osd_message("Error : could not create the csv file")
    else :
        #Write the first line with CharaID and VehicleID
        file.write(f"{data['CharaID']},{data['VehicleID']}\n")

        #Write the other lines with data[i]
        for i in range(len(data.keys())-2):
            pos = data[i]["Pos"]
            qua = data[i]["Qua"]
            iv = data[i]["IV"]
            ev = data[i]["EV"]
            spd1 = data[i]["BaseSpd"]
            spd2 = data[i]["MaxSpd"]
            angle = data[i]["Angle"]
            dire = data[i]["Dire"]
            dive = data[i]["Dive"]

            writeline = ''
            writeline += f"{pos.x},{pos.y},{pos.z},"
            writeline += f"{qua.x},{qua.y},{qua.z},{qua.w},"
            writeline += f"{iv.x},{iv.y},{iv.z},"
            writeline += f"{ev.x},{ev.y},{ev.z},"
            writeline += f"{spd1},"
            writeline += f"{spd2},"
            writeline += f"{angle},"
            writeline += f"{dire.x},{dire.y},{dire.z},"
            writeline += f"{dive}\n"
            file.write(writeline)


        file.close()
        gui.add_osd_message(f"Data successfully stored to {csvfilename}")

def csv_to_data(csvfilename):
    """Invert data_to_csv"""
    data = {}
    file = open(csvfilename, 'r')
    if file is None :
        gui.add_osd_message("Error : could not load the csv file")
    else:
        listlines = file.readlines()
        #Read the first line for CharaID and VehicleID
        values = listlines[0].split(",")
        data["CharaID"] = values[0]
        data["VehicleID"] = values[1]

        #Read the other lines for data[i]
        for i in range(1, len(listlines)):
            data[i-1] = {}
            values_string = listlines[i].split(",")
            values = [float(string) for string in values_string]
            data[i-1]["Pos"] = vec3(values[0], values[1], values[2])
            data[i-1]["Qua"] = quatf(values[3], values[4], values[5], values[6])
            data[i-1]["IV"] = vec3(values[7], values[8], values[9])
            data[i-1]["EV"] = vec3(values[10], values[11], values[12])
            data[i-1]["BaseSpd"] = values[13]
            data[i-1]["MaxSpd"] = values[14]
            data[i-1]["Angle"] = values[15]
            data[i-1]["Dire"] = vec3(values[16], values[17], values[18])
            data[i-1]["Dive"] = values[19]

        file.close()
        gui.add_osd_message(f"Data successfully loaded from {csvfilename}")
        return data
            
def init_data():
    """Return a data dic, with default values
        for each frame before the current frame"""
    data = {}
    default_frame_data = {}
    default_frame_data["Pos"] = vec3(0,0,0)
    default_frame_data["Qua"] = quatf(0,0,0,0)
    default_frame_data["IV"] = vec3(0,0,0)
    default_frame_data["EV"] = vec3(0,0,0)
    default_frame_data["BaseSpd"] = 0
    default_frame_data["MaxSpd"] = 0
    default_frame_data["Angle"] = 0
    default_frame_data["Dire"] = vec3(0,0,0)
    default_frame_data["Dive"] = 0
    frame = mkw_utils.frame_of_input()
    for i in range(frame):
        data[i] = default_frame_data
    return data


def update_data(data):
    """Update data to the currentn frame"""
    frame = mkw_utils.frame_of_input()
    currframe_data = {}
    currframe_data["Pos"] = VehiclePhysics(0).position()
    currframe_data["Qua"] = VehiclePhysics(0).main_rotation()
    currframe_data["IV"] = VehiclePhysics(0).internal_velocity()
    currframe_data["EV"] = VehiclePhysics(0).external_velocity()
    currframe_data["BaseSpd"] = KartMove(0).speed()
    currframe_data["MaxSpd"] = KartMove(0).soft_speed_limit()
    currframe_data["Angle"] = KartMove(0).outside_drift_angle()
    currframe_data["Dire"] = KartMove(0).dir()
    currframe_data["Dive"] = KartMove(0).diving_rotation()
    data[frame] = currframe_data
    

    
