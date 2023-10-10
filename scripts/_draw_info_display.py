from dolphin import event, gui, utils
from Modules import mkw_classes as classes, mkw_core as core
import configparser
import math
import os

def populate_default_config(file_path):
    config = configparser.ConfigParser()
    
    config['DEBUG'] = {}
    config['DEBUG']['Debug'] = "False"
    
    config['INFO DISPLAY'] = {}
    config['INFO DISPLAY']["Frame Count"] = "True"
    config['INFO DISPLAY']["Lap Splits"] = "False"
    config['INFO DISPLAY']["Speed"] = "True"
    config['INFO DISPLAY']["Internal Velocity (X, Y, Z)"] = "False"
    config['INFO DISPLAY']["Internal Velocity (XYZ)"] = "False"
    config['INFO DISPLAY']["External Velocity (X, Y, Z)"] = "False"
    config['INFO DISPLAY']["External Velocity (XYZ)"] = "True"
    config['INFO DISPLAY']["Moving Road Velocity (X, Y, Z)"] = "False"
    config['INFO DISPLAY']["Moving Road Velocity (XYZ)"] = "False"
    config['INFO DISPLAY']["Moving Water Velocity (X, Y, Z)"] = "False"
    config['INFO DISPLAY']["Moving Water Velocity (XYZ)"] = "False"
    config['INFO DISPLAY']["Charges and Boosts"] = "True"
    config['INFO DISPLAY']["Checkpoints and Completion"] = "True"
    config['INFO DISPLAY']["Airtime"] = "True"
    config['INFO DISPLAY']["Miscellaneous"] = "False"
    config['INFO DISPLAY']["Surface Properties"] = "False"
    config['INFO DISPLAY']["Position"] = "False"
    config['INFO DISPLAY']["Stick"] = "True"
    config['INFO DISPLAY']["Text Color (ARGB)"] = "0xFFFFFFFF"
    config['INFO DISPLAY']["Digits (to round to)"] = "6"
    
    with open(file_path, 'w') as f:
        config.write(f)
        
    return config

class ConfigInstance():
    def __init__(self, config : configparser.ConfigParser):
        self.debug = config['DEBUG'].getboolean('Debug')
        self.frame_count = config['INFO DISPLAY'].getboolean('Frame Count')
        self.lap_splits = config['INFO DISPLAY'].getboolean('Lap Splits')
        self.speed = config['INFO DISPLAY'].getboolean('Speed')
        self.iv = config['INFO DISPLAY'].getboolean('Internal Velocity (X, Y, Z)')
        self.iv_xyz = config['INFO DISPLAY'].getboolean('Internal Velocity (XYZ)')
        self.ev = config['INFO DISPLAY'].getboolean('External Velocity (X, Y, Z)')
        self.ev_xyz = config['INFO DISPLAY'].getboolean('External Velocity (XYZ)')
        self.mrv = config['INFO DISPLAY'].getboolean('Moving Road Velocity (X, Y, Z)')
        self.mrv_xyz = config['INFO DISPLAY'].getboolean('Moving Road Velocity (XYZ)')
        self.mwv = config['INFO DISPLAY'].getboolean('Moving Water Velocity (X, Y, Z)')
        self.mwv_xyz = config['INFO DISPLAY'].getboolean('Moving Water Velocity (XYZ)')
        self.charges = config['INFO DISPLAY'].getboolean('Charges and Boosts')
        self.cps = config['INFO DISPLAY'].getboolean('Checkpoints and Completion')
        self.air = config['INFO DISPLAY'].getboolean('Airtime')
        self.misc = config['INFO DISPLAY'].getboolean('Miscellaneous')
        self.surfaces = config['INFO DISPLAY'].getboolean('Surface Properties')
        self.position = config['INFO DISPLAY'].getboolean('Position')
        self.stick = config['INFO DISPLAY'].getboolean('Stick')
        self.color = int(config['INFO DISPLAY']['Text Color (ARGB)'], 16)
        self.digits = min(7, config['INFO DISPLAY'].getint('Digits (to round to)'))
    
def main():
    config = configparser.ConfigParser()

    file_path = os.path.join(utils.get_script_dir(), 'Modules', 'infodisplay.ini')
    config.read(file_path)

    if not config.sections():
        config = populate_default_config(file_path)
    
    global c
    c = ConfigInstance(config)

if __name__ == '__main__':
    main()

# draw information to the screen

def create_infodisplay():
    text = ""

    if c.debug:
        # test values here
        text += f"{utils.get_game_id()}\n\n"
    
    if c.frame_count:
        text += f"Frame: {core.get_frame_of_input()}\n\n"

    if c.lap_splits:
        # The actual max lap address does not update when crossing the finish line
        # for the final time to finish the race. However, for whatever reason,
        # race completion does. We use the "max" version to prevent lap times
        # from disappearing when crossing the line backwards.
        player_max_lap = math.floor(
            classes.RaceInfoPlayer.race_completion_max())
        lap_count = classes.RaceDataSettings.lap_count()

        if player_max_lap >= 2 and lap_count > 1:
            for lap in range(1, player_max_lap):
                text += "Lap {}: {}\n".format(lap, core.updateExactFinish(lap, 0))

        if player_max_lap > lap_count:
            text += "Final: {}\n".format(core.getUnroundedTime(lap_count, 0))
        text += "\n"

    if c.speed:
        speed = core.get_speed()
        engine_speed = classes.KartMove.speed()
        cap = classes.KartMove.soft_speed_limit()
        text += f"        XZ: {round(speed.xz, c.digits)}\n"
        text += f"       XYZ: {round(speed.xyz, c.digits)}\n"
        text += f"         Y: {round(speed.y, c.digits)}\n"
        text += f"    Engine: {round(engine_speed, c.digits)} / {round(cap, c.digits)}"
        text += "\n\n"

    if (c.iv or c.iv_xyz):
        iv = classes.VehiclePhysics.internal_velocity()

    if c.iv:
        text += f"      IV X: {round(iv.x,c.digits)}\n"
        text += f"      IV Y: {round(iv.y,c.digits)}\n"
        text += f"      IV Z: {round(iv.z,c.digits)}\n\n"

    if c.iv_xyz:
        text += f"    IV  XZ: {round(iv.norm_xz(),c.digits)}\n"
        text += f"    IV XYZ: {round(iv.norm_xyz(),c.digits)}\n\n"

    if (c.ev or c.ev_xyz):
        ev = classes.VehiclePhysics.external_velocity()

    if c.ev:
        text += f"      EV X: {round(ev.x,c.digits)}\n"
        text += f"      EV Y: {round(ev.y,c.digits)}\n"
        text += f"      EV Z: {round(ev.z,c.digits)}\n\n"

    if c.ev_xyz:
        text += f"    EV  XZ: {round(ev.norm_xz(),c.digits)}\n"
        text += f"    EV XYZ: {round(ev.norm_xyz(),c.digits)}\n\n"

    if (c.mrv or c.mrv_xyz):
        mrv = classes.VehiclePhysics.moving_road_velocity()

    if c.mrv:
        text += f"     MRV X: {round(mrv.x,c.digits)}\n"
        text += f"     MRV Y: {round(mrv.y,c.digits)}\n"
        text += f"     MRV Z: {round(mrv.z,c.digits)}\n\n"
    
    if c.mrv_xyz:
        text += f"   MRV  XZ: {round(mrv.norm_xz(),c.digits)}\n"
        text += f"   MRV XYZ: {round(mrv.norm_xyz(),c.digits)}\n\n"

    if (c.mwv or c.mwv_xyz):
        mwv = classes.VehiclePhysics.moving_water_velocity()

    if c.mwv:
        text += f"     MWV X: {round(mwv.x,c.digits)}\n"
        text += f"     MWV Y: {round(mwv.y,c.digits)}\n"
        text += f"     MWV Z: {round(mwv.z,c.digits)}\n\n"

    if c.mwv_xyz:
        text += f"   MWV  XZ: {round(mwv.norm_xz(),c.digits)}\n"
        text += f"   MWV XYZ: {round(mwv.norm_xyz(),c.digits)}\n\n"

    if c.charges:
        mt = classes.KartMove.mt_charge()
        smt = classes.KartMove.smt_charge()
        ssmt = classes.KartMove.ssmt_charge()
        mt_boost = classes.KartMove.mt_boost_timer()
        trick_boost = classes.KartMove.trick_timer()
        shroom_boost = classes.KartMove.mushroom_timer()
        if bool(classes.KartParam.is_bike()):
            text += f"MT Charge: {mt} | SSMT Charge: {ssmt}\n"
        else:
            text += f"MT Charge: {mt} ({smt}) | SSMT Charge: {ssmt}\n"
            
        text += f"MT: {mt_boost} | Trick: {trick_boost} | Mushroom: {shroom_boost}\n\n"

    if c.cps:
        lap_comp = classes.RaceInfoPlayer.lap_completion()
        race_comp = classes.RaceInfoPlayer.race_completion()
        cp = classes.RaceInfoPlayer.checkpoint_id()
        kcp = classes.RaceInfoPlayer.max_kcp()
        rp = classes.RaceInfoPlayer.respawn_point()
        text += f" Lap%: {round(lap_comp,c.digits)}\n"
        text += f"Race%: {round(race_comp,c.digits)}\n"
        text += f"CP: {cp} | KCP: {kcp} | RP: {rp}\n\n"

    if c.air:
        airtime = classes.KartMove.airtime()
        text += f"Airtime: {airtime}\n\n"

    if c.misc:
        wheelie_frames = classes.KartMove.wheelie_frames()
        wheelie_cd = classes.KartMove.wheelie_cooldown()
        trick_cd = classes.KartJump.cooldown()
        oob_timer = classes.KartCollide.solid_oob_timer()
        if classes.KartParam.is_bike() == 1:
            text += f"Wheelie Length: {wheelie_frames}\n"
            text += f"Wheelie CD: {wheelie_cd} | Trick CD: {trick_cd}\n"
        else:
            text += f"Trick CD: {trick_cd}\n"
        text += f"OOB: {oob_timer}\n\n"

    if c.surfaces:
        is_offroad = classes.KartCollide.surface_properties().offroad > 0
        is_trickable = classes.KartCollide.surface_properties().trickable > 0
        kcl_speed_mod = classes.KartMove.kcl_speed_factor()
        text += f"  Offroad: {is_offroad}\n"
        text += f"Trickable: {is_trickable}\n"
        text += f"KCL Speed Modifier: {round(kcl_speed_mod * 100, c.digits)}%\n\n"

    if c.position:
        pos = classes.VehiclePhysics.pos()
        text += f"X Pos: {pos.x}\n"
        text += f"Y Pos: {pos.y}\n"
        text += f"Z Pos: {pos.z}\n\n"

    # TODO: figure out why classes.RaceInfoPlayer.stick_x() and 
    #       classes.RaceInfoPlayer.stick_y() do not update
    #       (using these as placeholders until further notice)
    if c.stick:
        stick_x = core.chase_pointer(
                  classes.getRaceInfoHolder(), [0xC, 0x0, 0x48, 0x38], 'u8') - 7
        stick_y = core.chase_pointer(
                  classes.getRaceInfoHolder(), [0xC, 0x0, 0x48, 0x39], 'u8') - 7
        text += f"X: {stick_x} | Y: {stick_y}\n\n"  

    return text


@event.on_savestateload
def on_state_load(fromSlot: bool, slot: int):
    if classes.RaceInfo.stage() >= 1:
        gui.draw_text((10, 10), c.color, create_infodisplay())

@event.on_frameadvance
def on_frame_advance():
    if classes.RaceInfo.stage() >= 1:
        gui.draw_text((10, 10), c.color, create_infodisplay())
