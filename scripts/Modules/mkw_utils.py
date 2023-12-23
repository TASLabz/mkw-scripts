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


# TODO: Time difference display helper functions
"""The time difference functions.
time_difference_[name](P1, S1, P2, S2) is a function that takes as arguments
P1,S1 : Player1's Position and Speed vec3.
P2,S2 : Player2's Position and Speed vec3
Return the time it would take for Player1 to catch Player2 (not always symmetric)

get_time_difference_[name](Player1, Player2) takes as arguments
Player1 : Player1 ID
Player2 : Player2 ID
Return the time it would take for Player1 to catch Player2 (not always symmetric)
It's the function called in draw_infodisplay.py
"""

def get_physics(player1, player2):
    """Take the Player1 and Player2 ID's, return their
        P1, S1, P2, S2 data"""
    P1, S1 = VehiclePhysics(player1).position(), delta_position(player1)
    P2, S2 = VehiclePhysics(player2).position(), delta_position(player2)
    return P1,S1,P2,S2


def get_distance_ghost_vec():
    """Give the distance (vec3) between the player and the ghost
        Player to ghost vec"""
    player_position = VehiclePhysics(0).position()
    ghost_position = VehiclePhysics(1).position()
    return (ghost_position - player_position)

def get_distance_ghost():
    """Give the distance(float) between the player and the ghost"""
    return get_distance_ghost_vec().length()

def time_difference_absolute(P1, P2, S1, S2):
    s = S1.length()
    if s != 0:
        return (P2-P1).length() / s
    return float('inf')
    
def get_time_difference_absolute(player1, player2):
    """Time difference "Absolute" (simple and bad)
    Simply takes the distance player-ghost, and divide it by raw speed (always positive)"""
    P1, S1, P2, S2 = get_physics(player1, player2)
    return time_difference_absolute(P1, P2, S1, S2)

def time_difference_relative(P1, P2, S1, S2):
    L = (P2 - P1).length()
    if L == 0:
        return 0
    s = S1*(P2-P1)/L
    if s == 0:
        return float('inf')  
    return (P2-P1).length() / s

def get_time_difference_relative(player1, player2):
    """Time difference "Relative" 
    Take distance player-ghost. Divide it by the player's speed "toward" the ghost (dot product)"""
    P1, S1, P2, S2 = get_physics(player1, player2)
    return time_difference_relative(P1, P2, S1, S2)

def time_difference_projected(P1, P2, S1, S2):
    s = S1.length()
    if s == 0:
        return float('inf')
    return (P2-P1)*S1/(s**2)

def get_time_difference_projected(player1, player2):
    """ Time difference "Projected"
    Take the distance between the player and the plane oriented by the player speed, covering the ghost.
    Then divide it by the player raw speed
    This is the 2D version because no numpy"""
    P1, S1, P2, S2 = get_physics(player1, player2)
    return time_difference_projected(P1, P2, S1, S2)


def time_to_cross(A, S, B, C):
    """If A is going at a constant speed S, how many frame will it take
        to cross the vertical plan containing B and C
        Param : A, S, B, C : (vec3),(vec3),(vec3),(vec3)
        Return t (float) """
    N = (B-C)@vec3(0,1,0) #normal vector to the plan containing B,C
    ns = N*S
    if ns != 0:
        return N*(B-A)/ns
    return float('inf')

def time_difference_crosspath(P1, P2, S1, S2):
    t1 = time_to_cross(P1, S1, P2, P2+S2)
    t2 = time_to_cross(P2, S2, P1, P1+S1)
    return t1-t2


def get_time_difference_crosspath(player1, player2):
    """Time difference "CrossPath"
    Take both XZ trajectories of the player and the ghost
    Calculate how much time it takes them to reach the crosspoint. (2D only)
    Return the difference."""
    P1, S1, P2, S2 = get_physics(player1, player2)
    return time_difference_crosspath(P1, P2, S1, S2)



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


def time_difference_tofinish(P1, P2, S1, S2):
    A,B = get_finish_line_coordinate()
    t1 = time_to_cross(P1, S1, A, B)
    t2 = time_to_cross(P2, S2, A, B)
    return t1-t2

def get_time_difference_tofinish(player1, player2):
    """Assume player and ghost are not accelerated.
    Calculate the time to the finish line for both, and takes the difference."""
    P1, S1, P2, S2 = get_physics(player1, player2)
    return time_difference_tofinish(P1, P2, S1, S2)


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
            return -t
        return -inf
    else:
        if curframe.prc>lastframe.grc:
            l =[history.get_older_frame(k).grc for k in range(history.size)]
            i = find_index(curframe.prc, l)
            t = i + (curframe.prc - l[i])/ (l[i+1] - l[i])
            return t
        return inf


def get_timediff_settings(string):
    if string == 'player':
        return 0, 1
    if string == 'ghost':
        return 1, 0
    pp, sp, pg, sg = get_physics(0,1)
    player_is_ahead = int(sp*(pg-pp)>0)
    if string == 'ahead':
        return 1-player_is_ahead, player_is_ahead
    if string == 'behind':
        return player_is_ahead, 1-player_is_ahead
    else:
        print('TimeDiff setting value not recognized. Default to "player"')
        return 0, 1
        
        
