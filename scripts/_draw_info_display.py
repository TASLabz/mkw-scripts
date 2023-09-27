from dolphin import event, gui, utils
from Modules import mkw_classes as classes, mkw_core as core
import configparser
import math
import os

config = configparser.ConfigParser()

config.read(os.path.join(utils.get_script_dir(), 'Modules', 'infodisplay.ini'))

debug = config['DEBUG'].getboolean('Debug')

frame_count = config['INFO DISPLAY'].getboolean('Frame Count')

lap_splits = config['INFO DISPLAY'].getboolean('Lap Splits')

speed = config['INFO DISPLAY'].getboolean('Speed')

internal_velocity = config['INFO DISPLAY'
                    ].getboolean('Internal Velocity (X, Y, Z)')
internal_velocity_xyz = config['INFO DISPLAY'
                        ].getboolean('Internal Velocity (XYZ)')

external_velocity = config['INFO DISPLAY'
                    ].getboolean('External Velocity (X, Y, Z)')
external_velocity_xyz = config['INFO DISPLAY'
                        ].getboolean('External Velocity (XYZ)')

moving_road_velocity = config['INFO DISPLAY'
                       ].getboolean('Moving Road Velocity (X, Y, Z)')
moving_road_velocity_xyz = config['INFO DISPLAY'
                           ].getboolean('Moving Road Velocity (XYZ)')

moving_water_velocity = config['INFO DISPLAY'
                        ].getboolean('Moving Water Velocity (X, Y, Z)')
moving_water_velocity_xyz = config['INFO DISPLAY'
                            ].getboolean('Moving Water Velocity (XYZ)')

charges_and_boosts = config['INFO DISPLAY'
                     ].getboolean('Charges and Boosts')
checkpoints_and_completion = config['INFO DISPLAY'
                             ].getboolean('Checkpoints and Completion')
miscellaneous = config['INFO DISPLAY'
                ].getboolean('Miscellaneous')

surface_properties = config['INFO DISPLAY'
                     ].getboolean('Surface Properties')

position = config['INFO DISPLAY'].getboolean('Position')

stick = config['INFO DISPLAY'].getboolean('Stick')

color = int(config['INFO DISPLAY']['Text Color'], 16)

digits = config['INFO DISPLAY'].getint('Digits (to round to)')

# draw information to the screen


def create_infodisplay():
    text = ""

    if debug:
        # test values here
        text += f"{utils.get_game_id()}\n\n"
    
    if frame_count:
        text += f"Frame: {core.get_frame_of_input()}\n\n"

    if lap_splits:
        # The actual max lap address does not update when crossing the finish line
        # for the final time to finish the race. However, for whatever reason,
        # race completion does. We use the "max" version to prevent lap times
        # from disappearing when crossing the line backwards.
        player_max_lap = math.floor(
            classes.RaceInfoPlayer.race_completion_max())
        lap_count = classes.RaceDataSettings.lap_count()

        if player_max_lap >= 2 and lap_count > 1:
            for lap in range(1, player_max_lap):
                text += "Lap {:d}: {:02d}:{:012.9f}\n".format(
                    lap, core.updateExactFinish(lap, 0)[0],
                    core.updateExactFinish(lap, 0)[1])

        if player_max_lap > lap_count:
            text += "Final: {:02d}:{:012.9f}\n".format(
                core.getUnroundedTime(lap_count, 0)[0],
                core.getUnroundedTime(lap_count, 0)[1])
        text += "\n"

    if speed:
        xz = core.get_speed().xz
        y = core.get_speed().y
        xyz = core.get_speed().xyz
        engine_speed = classes.KartMove.speed()
        cap = classes.KartMove.soft_speed_limit()
        text += f"        XZ: {round(xz, digits)}\n"
        text += f"       XYZ: {round(xyz, digits)}\n"
        text += f"         Y: {round(y, digits)}\n"
        text += f"    Engine: {round(engine_speed, digits)} / {round(cap, digits)}\n\n"

    if internal_velocity:
        iv_x = classes.VehiclePhysics.internal_velocity().x
        iv_y = classes.VehiclePhysics.internal_velocity().y
        iv_z = classes.VehiclePhysics.internal_velocity().z
        text += f"      IV X: {round(iv_x, digits)}\n"
        text += f"      IV Y: {round(iv_y, digits)}\n"
        text += f"      IV Z: {round(iv_z, digits)}\n\n"

    if internal_velocity_xyz:
        iv_xyz = math.sqrt(classes.VehiclePhysics.internal_velocity().x ** 2
               + classes.VehiclePhysics.internal_velocity().y ** 2 
               + classes.VehiclePhysics.internal_velocity().z ** 2)
        text += f"    IV XYZ: {round(iv_xyz, digits)}\n\n"

    if external_velocity:
        ev_x = classes.VehiclePhysics.external_velocity().x
        ev_y = classes.VehiclePhysics.external_velocity().y
        ev_z = classes.VehiclePhysics.external_velocity().z
        text += f"      EV X: {round(ev_x, digits)}\n"
        text += f"      EV Y: {round(ev_y, digits)}\n"
        text += f"      EV Z: {round(ev_z, digits)}\n\n"

    if external_velocity_xyz:
        ev_xyz = math.sqrt(classes.VehiclePhysics.external_velocity().x ** 2
               + classes.VehiclePhysics.external_velocity().y ** 2
               + classes.VehiclePhysics.external_velocity().z ** 2)
        text += f"    EV XYZ: {round(ev_xyz, digits)}\n\n"

    if moving_road_velocity:
        mrv_x = classes.VehiclePhysics.moving_road_velocity().x
        mrv_y = classes.VehiclePhysics.moving_road_velocity().y
        mrv_z = classes.VehiclePhysics.moving_road_velocity().z
        text += f"     MRV X: {round(mrv_x, digits)}\n"
        text += f"     MRV Y: {round(mrv_y, digits)}\n"
        text += f"     MRV Z: {round(mrv_z, digits)}\n\n"
    
    if moving_road_velocity_xyz:
        mrv_xyz = math.sqrt(classes.VehiclePhysics.moving_road_velocity().x ** 2
                + classes.VehiclePhysics.moving_road_velocity().y ** 2
                + classes.VehiclePhysics.moving_road_velocity().z ** 2)
        text += f"   MRV XYZ: {round(mrv_xyz, digits)}\n\n"

    if moving_water_velocity:
        mwv_x = classes.VehiclePhysics.moving_water_velocity().x
        mwv_y = classes.VehiclePhysics.moving_water_velocity().y
        mwv_z = classes.VehiclePhysics.moving_water_velocity().z
        text += f"     MWV X: {round(mwv_x, digits)}\n"
        text += f"     MWV Y: {round(mwv_y, digits)}\n"
        text += f"     MWV Z: {round(mwv_z, digits)}\n\n"

    if moving_water_velocity_xyz:
        mwv_xyz = math.sqrt(classes.VehiclePhysics.moving_water_velocity().x ** 2
                + classes.VehiclePhysics.moving_water_velocity().y ** 2
                + classes.VehiclePhysics.moving_water_velocity().z ** 2)
        text += f"   MWV XYZ: {round(mwv_xyz, digits)}\n\n"

    if charges_and_boosts:
        mt = classes.KartMove.mt_charge()
        smt = classes.KartMove.smt_charge()
        ssmt = classes.KartMove.ssmt_charge()
        mt_boost = classes.KartMove.mt_boost_timer()
        trick_boost = classes.KartMove.trick_timer()
        shroom_boost = classes.KartMove.mushroom_timer()
        if classes.KartParam.is_bike() == 0:
            text += f"MT Charge: {mt} ({smt}) | SSMT Charge: {ssmt}\n"
        else:
            text += f"MT Charge: {mt} | SSMT Charge: {smt}\n"
        text += f"MT: {mt_boost} | Trick: {trick_boost} | Mushroom: {shroom_boost}\n\n"

    if checkpoints_and_completion:
        lap_comp = classes.RaceInfoPlayer.lap_completion()
        race_comp = classes.RaceInfoPlayer.race_completion()
        cp = classes.RaceInfoPlayer.checkpoint_id()
        kcp = classes.RaceInfoPlayer.max_kcp()
        rp = classes.RaceInfoPlayer.respawn_point()
        text += f" Lap%: {round(lap_comp, digits)}\n"
        text += f"Race%: {round(race_comp, digits)}\n"
        text += f"CP: {cp} | KCP: {kcp} | RP: {rp}\n\n"

    if miscellaneous:
        wheelie_frames = classes.KartMove.wheelie_frames()
        wheelie_cd = classes.KartMove.wheelie_cooldown()
        trick_cd = classes.KartJump.cooldown()
        airtime = classes.KartMove.airtime()
        oob_timer = classes.KartCollide.solid_oob_timer()
        if classes.KartParam.is_bike() == 1:
            text += f"Wheelie Length: {wheelie_frames}\n"
            text += f"Wheelie CD: {wheelie_cd} | Trick CD: {trick_cd}\n"
        else:
            text += f"Trick CD: {trick_cd}\n"
        text += f"Airtime: {airtime} | OOB: {oob_timer}\n\n"

    if surface_properties:
        is_offroad = classes.KartCollide.surface_properties().offroad > 0
        is_trickable = classes.KartCollide.surface_properties().trickable > 0
        kcl_speed_mod = classes.KartMove.kcl_speed_factor()
        text += f"  Offroad: {is_offroad}\n"
        text += f"Trickable: {is_trickable}\n"
        text += f"KCL Speed Modifier: {round(kcl_speed_mod * 100, digits)}%\n\n"

    if position:
        pos_x = classes.VehiclePhysics.pos().x
        pos_y = classes.VehiclePhysics.pos().y
        pos_z = classes.VehiclePhysics.pos().z
        text += f"X Pos: {pos_x}\n"
        text += f"Y Pos: {pos_y}\n"
        text += f"Z Pos: {pos_z}\n\n"

    # TODO: figure out why classes.RaceInfoPlayer.stick_x() and 
    #       classes.RaceInfoPlayer.stick_y() do not update
    #       (using these as placeholders until further notice)
    if stick:
        stick_x = core.chase_pointer(
                  classes.getRaceInfoHolder(), [0xC, 0x0, 0x48, 0x38], 'u8') - 7
        stick_y = core.chase_pointer(
                  classes.getRaceInfoHolder(), [0xC, 0x0, 0x48, 0x39], 'u8') - 7
        text += f"X: {stick_x} | Y: {stick_y}\n\n"  

    return text


@event.on_frameadvance
def on_frame_advance():
    if classes.RaceInfo.stage() >= 1:
        gui.draw_text((10, 10), color, create_infodisplay())
