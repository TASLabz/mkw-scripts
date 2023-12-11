from dolphin import memory, utils

from .mkw_classes import mat34, quatf, vec3, ExactTimer
from .mkw_classes import VehicleDynamics, VehiclePhysics, RaceManagerPlayer

import math

# These are helper functions that don't quite fit in common.py
# This file also contains getter functions for a few global variables.

# NOTE (xi): wait for get_game_id() to be put in dolphin.memory before clearing
#  these commented-out lines:

def chase_pointer(base_address, offsets, data_type):
    """This is a helper function to allow multiple ptr dereferences in
       quick succession. base_address is dereferenced first, and then
       offsets are applied. Then, the appropriate function based off data_type
       is called with the resulting dereferences + the final offset."""
    current_address = memory.read_u32(base_address)
    for offset in offsets:
        value_address = current_address + offset
        current_address = memory.read_u32(current_address + offset)
    data_types = {
        'u8': memory.read_u8,
        'u16': memory.read_u16,
        'u32': memory.read_u32,
        'u64': memory.read_u64,
        's8': memory.read_s8,
        's16': memory.read_s16,
        's32': memory.read_s32,
        's64': memory.read_s64,
        'f32': memory.read_f32,
        'f64': memory.read_f64,
        'vec3': vec3.read,
        'mat34': mat34.read,
        'quatf': quatf.read,
    }
    return data_types[data_type](value_address)


def frame_of_input():
    id = utils.get_game_id()
    address = {"RMCE01": 0x809BF0B8, "RMCP01": 0x809C38C0,
               "RMCJ01": 0x809C2920, "RMCK01": 0x809B1F00}
    return memory.read_u32(address[id])

def delta_position(playerIdx=0):
    dynamics_ref = VehicleDynamics(playerIdx)
    physics_ref = VehiclePhysics(addr=dynamics_ref.vehicle_physics())

    return physics_ref.position() - dynamics_ref.position()

# Next 3 functions are used for exact finish display

def get_igt(lap, player):
    if player == 0:
        address = 0x800001B0
    elif player == 1:
        address = 0x800001F8
    else:
        return ExactTimer(0, 0, 0)
    
    race_manager_player_inst = RaceManagerPlayer(player)
    timer_inst = race_manager_player_inst.lap_finish_time(lap-1)
    mins = timer_inst.minutes()
    secs = timer_inst.seconds()
    mils = memory.read_f32(address + (lap-1)*0x4) / 1000 % 1
    return ExactTimer(mins, secs, mils)

def update_exact_finish(lap, player):
    currentLapTime = get_igt(lap, player)
    if lap > 1:
        pastLapTime = get_igt(lap-1, player)
    else:
        pastLapTime = ExactTimer(0, 0, 0.0)

    return currentLapTime - pastLapTime

def get_unrounded_time(lap, player):
    t = ExactTimer(0, 0, 0)
    for i in range(lap):
        t += update_exact_finish(i + 1, player)
    return t

# TODO: Rotation display helper functions
def calculate_euler_angle(q):
    """Param : quatf
        Return : vec3 """
    x1, x2 = 2*q.x*q.w-2*q.y*q.z, 1-2*q.x*q.x-2*q.z*q.z
    y1, y2 = 2*q.y*q.w-2*q.x*q.z, 1-2*q.y*q.y-2*q.z*q.z
    z = 2*q.x*q.y + 2*q.z*q.w
    roll = 180/math.pi * math.asin(z)
    pitch = 180/math.pi * math.atan2(x1, x2)
    yaw = 180/math.pi * math.atan2(y1, y2)
    return vec3(pitch%360, yaw%360, roll%360)

def get_facing_angle(player):
    """Param : int player_id
        Return : vec3 , correspond to facing angles"""
    quaternion = VehiclePhysics(player).main_rotation()
    return calculate_euler_angle(quaternion)
    
def get_moving_angle(player):
    """Param : int player_id
        Return : vec3 , correspond to moving angles"""
    s = delta_position(player)
    roll = 180/math.pi * math.atan2(s.z, s.y)
    pitch = 180/math.pi * math.atan2(s.x, s.z)
    yaw = 180/math.pi * math.atan2(s.y, s.x)
    return vec3(roll%360, pitch%360, yaw%360)

# TODO: Time difference display helper functions
