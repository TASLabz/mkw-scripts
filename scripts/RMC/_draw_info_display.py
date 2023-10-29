from dolphin import event, gui, utils
import configparser
import math
import os

from Modules.mkw_classes.common import SurfaceProperties

import Modules.mkw_utils as mkw_utils
from Modules.mkw_classes import RaceManager, RaceManagerPlayer, RaceState
from Modules.mkw_classes import RaceConfig, RaceConfigScenario, RaceConfigSettings
from Modules.mkw_classes import KartObject, KartMove, KartSettings, KartBody
from Modules.mkw_classes import VehicleDynamics, VehiclePhysics, KartBoost, KartJump
from Modules.mkw_classes import KartState, KartCollide, KartInput, RaceInputState

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

    file_path = os.path.join(utils.get_script_dir(), 'modules', 'infodisplay.ini')
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
        text += f"Frame: {mkw_utils.frame_of_input()}\n\n"
    
    race_mgr_player = RaceManagerPlayer()
    race_scenario = RaceConfigScenario(addr=RaceConfig.race_scenario())
    race_settings = RaceConfigSettings(race_scenario.settings())
    kart_object = KartObject()
    kart_state = KartState(addr=kart_object.kart_state())
    kart_move = KartMove(addr=kart_object.kart_move())
    kart_body = KartBody(addr=kart_object.kart_body())
    vehicle_dynamics = VehicleDynamics(addr=kart_body.vehicle_dynamics())
    vehicle_physics = VehiclePhysics(addr=vehicle_dynamics.vehicle_physics())


    if c.lap_splits:
        # The actual max lap address does not update when crossing the finish line
        # for the final time to finish the race. However, for whatever reason,
        # race completion does. We use the "max" version to prevent lap times
        # from disappearing when crossing the line backwards.
        player_max_lap = math.floor(race_mgr_player.race_completion_max())
        lap_count = race_settings.lap_count()

        if player_max_lap >= 2 and lap_count > 1:
            for lap in range(1, player_max_lap):
                text += "Lap {}: {}\n".format(lap, mkw_utils.update_exact_finish(lap, 0))

        if player_max_lap > lap_count:
            text += "Final: {}\n".format(mkw_utils.get_unrounded_time(lap_count, 0))
        text += "\n"

    if c.speed:
        speed = mkw_utils.delta_position(playerIdx=0)
        engine_speed = kart_move.speed()
        cap = kart_move.soft_speed_limit()
        text += f"        XZ: {round(speed.length_xz(), c.digits)}\n"
        text += f"       XYZ: {round(speed.length(), c.digits)}\n"
        text += f"         Y: {round(speed.y, c.digits)}\n"
        text += f"    Engine: {round(engine_speed, c.digits)} / {round(cap, c.digits)}"
        text += "\n\n"

    if (c.iv or c.iv_xyz):
        iv = vehicle_physics.internal_velocity()

    if c.iv:
        text += f"      IV X: {round(iv.x,c.digits)}\n"
        text += f"      IV Y: {round(iv.y,c.digits)}\n"
        text += f"      IV Z: {round(iv.z,c.digits)}\n\n"

    if c.iv_xyz:
        text += f"    IV  XZ: {round(iv.length_xz(),c.digits)}\n"
        text += f"    IV XYZ: {round(iv.length(),c.digits)}\n\n"

    if (c.ev or c.ev_xyz):
        ev = vehicle_physics.external_velocity()

    if c.ev:
        text += f"      EV X: {round(ev.x,c.digits)}\n"
        text += f"      EV Y: {round(ev.y,c.digits)}\n"
        text += f"      EV Z: {round(ev.z,c.digits)}\n\n"

    if c.ev_xyz:
        text += f"    EV  XZ: {round(ev.length_xz(),c.digits)}\n"
        text += f"    EV XYZ: {round(ev.length(),c.digits)}\n\n"

    if (c.mrv or c.mrv_xyz):
        mrv = vehicle_physics.moving_road_velocity()

    if c.mrv:
        text += f"     MRV X: {round(mrv.x,c.digits)}\n"
        text += f"     MRV Y: {round(mrv.y,c.digits)}\n"
        text += f"     MRV Z: {round(mrv.z,c.digits)}\n\n"
    
    if c.mrv_xyz:
        text += f"   MRV  XZ: {round(mrv.length_xz(),c.digits)}\n"
        text += f"   MRV XYZ: {round(mrv.length(),c.digits)}\n\n"

    if (c.mwv or c.mwv_xyz):
        mwv = vehicle_physics.moving_water_velocity()

    if c.mwv:
        text += f"     MWV X: {round(mwv.x,c.digits)}\n"
        text += f"     MWV Y: {round(mwv.y,c.digits)}\n"
        text += f"     MWV Z: {round(mwv.z,c.digits)}\n\n"

    if c.mwv_xyz:
        text += f"   MWV  XZ: {round(mwv.length_xz(),c.digits)}\n"
        text += f"   MWV XYZ: {round(mwv.length(),c.digits)}\n\n"

    if c.charges or c.misc:
        kart_settings = KartSettings(addr=kart_object.kart_settings())

    if c.charges:
        kart_boost = KartBoost(addr=kart_move.kart_boost())
        
        mt = kart_move.mt_charge()
        smt = kart_move.smt_charge()
        ssmt = kart_move.ssmt_charge()
        mt_boost = kart_move.mt_boost_timer()
        trick_boost = kart_boost.trick_and_zipper_timer()
        shroom_boost = kart_move.mushroom_timer()
        if kart_settings.is_bike():
            text += f"MT Charge: {mt} | SSMT Charge: {ssmt}\n"
        else:
            text += f"MT Charge: {mt} ({smt}) | SSMT Charge: {ssmt}\n"
            
        text += f"MT: {mt_boost} | Trick: {trick_boost} | Mushroom: {shroom_boost}\n\n"

    if c.cps:
        lap_comp = race_mgr_player.lap_completion()
        race_comp = race_mgr_player.race_completion()
        cp = race_mgr_player.checkpoint_id()
        kcp = race_mgr_player.max_kcp()
        rp = race_mgr_player.respawn()
        text += f" Lap%: {round(lap_comp,c.digits)}\n"
        text += f"Race%: {round(race_comp,c.digits)}\n"
        text += f"CP: {cp} | KCP: {kcp} | RP: {rp}\n\n"

    if c.air:
        airtime = kart_move.airtime()
        text += f"Airtime: {airtime}\n\n"

    if c.misc or c.surfaces:
        kart_collide = KartCollide(addr=kart_object.kart_collide())

    if c.misc:
        kart_jump = KartJump(addr=kart_move.kart_jump())
        trick_cd = kart_jump.cooldown()
        hwg_timer = kart_state.hwg_timer()
        oob_timer = kart_collide.solid_oob_timer()
        respawn_timer = kart_collide.time_before_respawn()
        offroad_inv = kart_move.offroad_invincibility()
        if kart_move.is_bike:
            text += f"Wheelie Length: {kart_move.wheelie_frames()}\n"
            text += f"Wheelie CD: {kart_move.wheelie_cooldown()} | "
        text += f"Trick CD: {trick_cd}\n"
        text += f"HWG: {hwg_timer} | OOB: {oob_timer}\n"
        text += f"Respawn: {respawn_timer}\n"
        text += f"Offroad: {offroad_inv}\n\n"

    if c.surfaces:
        surface_properties = kart_collide.surface_properties()
        is_offroad = (surface_properties.value & SurfaceProperties.OFFROAD) > 0
        is_trickable = (surface_properties.value & SurfaceProperties.TRICKABLE) > 0
        kcl_speed_mod = kart_move.kcl_speed_factor()
        text += f"  Offroad: {is_offroad}\n"
        text += f"Trickable: {is_trickable}\n"
        text += f"KCL Speed Modifier: {round(kcl_speed_mod * 100, c.digits)}%\n\n"

    if c.position:
        pos = vehicle_physics.position()
        text += f"X Pos: {pos.x}\n"
        text += f"Y Pos: {pos.y}\n"
        text += f"Z Pos: {pos.z}\n\n"

    # TODO: figure out why classes.RaceInfoPlayer.stick_x() and 
    #       classes.RaceInfoPlayer.stick_y() do not update
    #       (using these as placeholders until further notice)
    if c.stick:
        kart_input = KartInput(addr=race_mgr_player.kart_input())
        current_input_state = RaceInputState(addr=kart_input.current_input_state())

        stick_x = current_input_state.raw_stick_x() - 7
        stick_y = current_input_state.raw_stick_y() - 7
        text += f"X: {stick_x} | Y: {stick_y}\n\n"  

    return text


@event.on_savestateload
def on_state_load(fromSlot: bool, slot: int):
    race_mgr = RaceManager()
    if race_mgr.state().value >= RaceState.COUNTDOWN.value:
        gui.draw_text((10, 10), c.color, create_infodisplay())

@event.on_frameadvance
def on_frame_advance():
    race_mgr = RaceManager()
    if race_mgr.state().value >= RaceState.COUNTDOWN.value:
        gui.draw_text((10, 10), c.color, create_infodisplay())
