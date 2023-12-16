from dolphin import memory, utils, event

from .mkw_classes import mat34, quatf, vec3, ExactTimer, eulerAngle
from .mkw_classes import VehicleDynamics, VehiclePhysics, RaceManagerPlayer, KartObjectManager, RaceManager, RaceState

import math

# These are helper functions that don't quite fit in common.py
# This file also contains getter functions for a few global variables.

# NOTE (xi): wait for get_game_id() to be put in dolphin.memory before clearing
#  these commented-out lines:


class FrameData:
    def __init__(self):
        #Default values
        self.prc = 0 #PlayerRaceCompletion
        self.grc = 0 #GhostRaceCompletion
        self.euler = eulerAngle()
        self.movangle = eulerAngle()

        #Value for current frame (if available)
        if RaceManager().state().value >= RaceState.COUNTDOWN.value:
            self.prc = RaceManagerPlayer(0).race_completion()
            self.euler = get_facing_angle(0)
            self.movangle = get_moving_angle(0)
            if not is_single_player():
                self.grc = RaceManagerPlayer(1).race_completion()
            
class History:
    def __init__(self, size):
        self.size = size
        self.array = []
        self.index = 0
        for _ in range(size):
            self.array.append(FrameData())

    def update(self):
        """Add a new frameData to the array, and move the index"""
        self.index = (self.index+1)%self.size
        self.array[self.index] = FrameData()

    def get_older_frame(self,i):
        """Return the FrameData i frame older"""
        assert i<self.size
        return self.array[(self.index-i)%self.size]

    
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

def is_single_player():
    return KartObjectManager().player_count() == 1

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
def quaternion_to_euler_angle(q):
    """Param : quatf
        Return : eulerAngle """
    x1, x2 = 2*q.x*q.w-2*q.y*q.z, 1-2*q.x*q.x-2*q.z*q.z
    y1, y2 = 2*q.y*q.w-2*q.x*q.z, 1-2*q.y*q.y-2*q.z*q.z
    z = 2*q.x*q.y + 2*q.z*q.w
    roll = 180/math.pi * math.asin(z)
    pitch = -180/math.pi * math.atan2(x1, x2)
    yaw = -180/math.pi * math.atan2(y1, y2)
    return eulerAngle(pitch, yaw, roll)

def get_facing_angle(player):
    """Param : int player_id
        Return : eulerAngle , correspond to facing angles"""
    quaternion = VehiclePhysics(player).main_rotation()
    return quaternion_to_euler_angle(quaternion)

def speed_to_euler_angle(speed):
    """Param : vec3 speed
        Return : eulerAngle"""
    s = speed
    pitch = 180/math.pi * math.atan2(s.z, s.y) #unsure and unused
    yaw = -180/math.pi * math.atan2(s.x, s.z)
    roll = -180/math.pi * math.atan2(s.y, s.x)#unsure and unused
    return eulerAngle(pitch, yaw, roll)

def get_moving_angle(player):
    """Param : int player_id
        Return : eulerAngle , correspond to moving angles"""
    speed = delta_position(player)
    return speed_to_euler_angle(speed)

def get_yaw_from_speed(speed):
    """Param : vec3 speed
        Return float yaw"""
    return (-180/math.pi * math.atan2(speed.y, speed.x))%360

# TODO: Time difference display helper functions

def get_distance_ghost_vec():
    """Give the distance (vec3) between the player and the ghost
        Player to ghost vec"""
    player_position = VehiclePhysics(0).position()
    ghost_position = VehiclePhysics(1).position()
    return (ghost_position - player_position)

def get_distance_ghost():
    """Give the distance(float) between the player and the ghost"""
    return get_distance_ghost_vec().length()

def get_time_difference_absolute():
    """Time difference "Absolute" (simple and bad)
    Simply takes the distance player-ghost, and divide it by raw speed (always positive)
    Return (float, float) t1, t2 : t1 is the time the player would take to catch the ghost
                                t2 is the time the ghost would take to catch the player"""
    player_speed = delta_position(0).length()
    ghost_speed = delta_position(1).length()
    distance = get_distance_ghost()
    t1 = float('inf')
    t2 = t1
    if player_speed != 0:
        t1 = distance/player_speed
    if ghost_speed != 0:
        t2 = distance/ghost_speed
    return t1, t2

def get_time_difference_relative():
    """Time difference "Relative" 
    Take distance player-ghost. Divide it by the player's speed "toward" the ghost (dot product)
    Return (float, float) t1, t2 : t1 is the time the player would take to catch the ghost
                                t2 is the time the ghost would take to catch the player"""
    player_speed_vec = delta_position(0)
    ghost_speed_vec = delta_position(1)
    distance_vec = get_distance_ghost_vec()
    distance = distance_vec.length()
    t1 = float('inf')
    t2 = t1
    if distance != 0:
        player_relative_speed = player_speed_vec * distance_vec * (1/distance)
        if player_relative_speed != 0:
            t1 = distance/player_relative_speed
        ghost_relative_speed = ghost_speed_vec * distance_vec * (-1/distance)
        if ghost_relative_speed != 0:
            t2 = distance/ghost_relative_speed
        return t1, t2
    return 0, 0


def get_time_difference_projected():
    """ Time difference "Projected"
    Take the distance between the player and the plane oriented by the player speed, covering the ghost.
    Then divide it by the player raw speed
    This is the 2D version because no numpy"""
    distance_p_g = get_distance_ghost_vec()
    player_speed = delta_position(0)
    ghost_speed = delta_position(1)
    t1 = float('inf')
    t2 = t1
    if player_speed.length() != 0:
        t1 = distance_p_g * player_speed * (1/player_speed.length()**2)
    if ghost_speed.length() != 0:
        t2 = distance_p_g * ghost_speed * (-1/ghost_speed.length()**2)
    return t1, t2



class Line:
    """2D lines
        ax + bz + c = 0"""
    def __init__(self, pointA, pointB):
        self.a = pointB.z - pointA.z
        self.b = pointA.x - pointB.x
        self.c = -(self.b*pointA.z + self.a*pointA.x)

    def intersect(self,other):
        """2 Lines intersecting, return point of intersection, (x,y)"""
        det = self.a*other.b-other.a*self.b
        x = float('inf')
        y = x
        if det!=0:
            x = (other.c*self.b - self.c*other.b)/det
            y = (self.c*other.a - other.c*self.a)/det
        return x,y

def get_time_difference_crosspath():
    """Time difference "CrossPath"
    Take both XZ trajectories of the player and the ghost
    Calculate how much time it takes them to reach the crosspoint. (2D only)
    Return the difference."""
    player_pos = VehiclePhysics(0).position()
    ghost_pos = VehiclePhysics(1).position()
    player_speed = delta_position(0)
    player_speed.y = 0
    ghost_speed = delta_position(1)
    ghost_speed.y = 0
    LinePlayer = Line(player_pos, player_pos+player_speed)
    LineGhost = Line(ghost_pos, ghost_pos+ghost_speed)
    x,z = LinePlayer.intersect(LineGhost)
    intersectpoint = vec3(x, 0, z)
    t_player = float('inf')
    t_ghost = t_player
    if player_speed.length_xz() != 0 :
        t_player = (intersectpoint - player_pos)*player_speed / (player_speed.length_xz()**2)
    if ghost_speed.length_xz() != 0 :
        t_ghost = (intersectpoint - ghost_pos)*ghost_speed / (ghost_speed.length_xz()**2)
    return t_player-t_ghost, t_ghost-t_player



def get_finish_line_coordinate():
    """pointA is the position of the left side of the finish line (vec3)
        point B ---------------------right------------------------------
        both have 0 as their Y coordinate."""
    game_id = utils.get_game_id()
    address = {"RMCE01": 0x809B8F28, "RMCP01": 0x809BD6E8,
               "RMCJ01": 0x809BC748, "RMCK01": 0x809ABD28}
    kmp_ref = chase_pointer(address[game_id], [0x4, 0x0], 'u32')
    offset = memory.read_u32(kmp_ref+0x24)
    pointA = vec3(memory.read_f32(kmp_ref+0x4C+offset+0x8+0x0), 0, memory.read_f32(kmp_ref+0x4C+offset+0x8+0x4))
    pointB = vec3(memory.read_f32(kmp_ref+0x4C+offset+0x8+0x8), 0, memory.read_f32(kmp_ref+0x4C+offset+0x8+0xC))
    return pointA, pointB


def time_to_cross(point, speed, line):
    """Return how fast a point going at speed cross the line"""
    velocity_line = Line(point, point+speed)
    x,z = line.intersect(velocity_line)
    speedxz = vec3(speed.x, 0, speed.z)
    crosspoint = vec3(x,0,z)
    t = float('inf')
    if speed.length_xz() != 0:
        t = (crosspoint - point)*speedxz/(speedxz.length() **2)
    return t

def time_to_finish(player):
    pos = VehiclePhysics(player).position()
    speed = delta_position(player)
    pointA, pointB = get_finish_line_coordinate()
    finish_line = Line(pointA, pointB)
    return time_to_cross(pos, speed, finish_line)
    
def get_time_difference_tofinish():
    """Assume player and ghost are not accelerated.
    Calculate the time to the finish line for both, and takes the difference."""
    t_player = time_to_finish(0)
    t_ghost = time_to_finish(1)
    return t_player-t_ghost, t_ghost-t_player


def find_index(value, value_list):
    """Find the index i so value_list[i]>=value>value_list[i+1]
        We suppose value_list[i+1] < value_list[i]
            and value_list[0]>= value>=value_list[-1]"""
    n = len(value_list)
    if n == 1 :
        return 0
    h = n//2
    if value <= value_list[h]:
        return h+find_index(value, value_list[h:])
    return find_index(value, value_list[:h])
    
def get_time_difference_racecompletion(history):
    """Use RaceCompletionData History to calculate the frame difference
        The function assume that RaceCompletion is increasing every frames"""
    curframe = history.get_older_frame(0)
    lastframe = history.get_older_frame(-1)
    inf = float('inf')
    if curframe.prc>=curframe.grc:
        if curframe.grc>lastframe.prc:
            l = [history.get_older_frame(k).prc for k in range(history.size)]
            i = find_index(curframe.grc, l)
            t = i + (curframe.grc - l[i])/ (l[i+1] - l[i])
            return -t, t
        return -inf, inf
    else:
        if curframe.prc>lastframe.grc:
            l =[history.get_older_frame(k).grc for k in range(history.size)]
            i = find_index(curframe.prc, l)
            t = i + (curframe.prc - l[i])/ (l[i+1] - l[i])
            return t, -t
        return inf, -inf
