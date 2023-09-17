# NOTE (xi): unfinished, vabold is taking the duty of rewriting this
# currently only for the use of testing other scripts that rely on this module

from dolphin import memory, utils
from dataclasses import dataclass
# will be removed soon
import mkw_core as core
  
# general structure / pointer reading
def chase_pointer(base_address, offsets, data_type):
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
        'vec3': read_vec3,
        'mat34': read_mat34,
        'quatf': read_quatf,
        'jump_pad': read_jump_pad_properties,
        'trick': read_trick_properties,
        'surface': read_surface_properties,
        'hitbox': read_hitbox_properties,
        'wheel': read_wheel_properties
    }
    return data_types[data_type](value_address)

@dataclass
class vec3:
  x: float = 0.0
  y: float = 0.0
  z: float = 0.0
  
def read_vec3(ptr):
  x = memory.read_f32(ptr + 0x0)
  y = memory.read_f32(ptr + 0x4)
  z = memory.read_f32(ptr + 0x8)

  return vec3(x, y, z)
  
@dataclass
class mat34:
  e00: float = 0.0
  e01: float = 0.0
  e02: float = 0.0
  e03: float = 0.0
  e10: float = 0.0
  e11: float = 0.0
  e12: float = 0.0
  e13: float = 0.0
  e20: float = 0.0
  e21: float = 0.0
  e22: float = 0.0
  e23: float = 0.0
  
def read_mat34(ptr):
  e00 = memory.read_f32(ptr + 0x0)
  e01 = memory.read_f32(ptr + 0x4)
  e02 = memory.read_f32(ptr + 0x8)
  e03 = memory.read_f32(ptr + 0xC)
  e10 = memory.read_f32(ptr + 0x10)
  e11 = memory.read_f32(ptr + 0x14)
  e12 = memory.read_f32(ptr + 0x18)
  e13 = memory.read_f32(ptr + 0x1C)
  e20 = memory.read_f32(ptr + 0x20)
  e21 = memory.read_f32(ptr + 0x24)
  e22 = memory.read_f32(ptr + 0x28)
  e23 = memory.read_f32(ptr + 0x2C)

  return mat34(e00, e01, e02, e03, e10, e11, e12, e13, e20, e21, e22, e23)
  
@dataclass
class quatf:
  x: float = 0.0
  y: float = 0.0
  z: float = 0.0
  w: float = 0.0
  
def read_quatf(ptr):
  x = memory.read_f32(ptr + 0x0)
  y = memory.read_f32(ptr + 0x4)
  z = memory.read_f32(ptr + 0x8)
  w = memory.read_f32(ptr + 0xC)
  
  return vec3(x, y, z, w)
  
@dataclass
class jump_pad_properties:
  min_speed:    float = 0.0
  max_speed:    float = 0.0
  vel_y:        float = 0.0
  
def read_jump_pad_properties(ptr):
  min_speed = memory.read_f32(ptr + 0x0)
  max_speed = memory.read_f32(ptr + 0x4)
  vel_y     = memory.read_f32(ptr + 0x8)

  return jump_pad_properties(min_speed, max_speed, vel_y)
  
@dataclass
class trick_properties:
  initial_angle_diff:   float = 0.0
  angle_diff_min:       float = 0.0
  angle_diff_mul_min:   float = 0.0
  angle_diff_mul_dec:   float = 0.0
  
def read_trick_properties(ptr):
  initial_angle_diff    = memory.read_f32(ptr + 0x0)
  angle_diff_min        = memory.read_f32(ptr + 0x4)
  angle_diff_mul_min    = memory.read_f32(ptr + 0x8)
  angle_diff_mul_dec    = memory.read_f32(ptr + 0xC)

  return trick_properties(initial_angle_diff, angle_diff_min, angle_diff_mul_min, angle_diff_mul_dec)
  
@dataclass
class surface_properties:
  wall:                 int = 0
  solid_oob:            int = 0
  boost_ramp:           int = 0
  offroad:              int = 0
  boost_panel_or_ramp:  int = 0
  trickable:            int = 0

def read_surface_properties(ptr):
  wall                  = memory.read_u32(ptr) & 0x1
  solid_oob             = memory.read_u32(ptr) & 0x2
  boost_ramp            = memory.read_u32(ptr) & 0x10
  offroad               = memory.read_u32(ptr) & 0x40
  boost_panel_or_ramp   = memory.read_u32(ptr) & 0x100
  trickable             = memory.read_u32(ptr) & 0x800
  
  return surface_properties(wall, solid_oob, boost_ramp, offroad, boost_panel_or_ramp, trickable)
  
@dataclass
class hitbox_properties:
  enable:               int = 0
  pos:                  float = 0.0
  radius:               float = 0.0
  walls_only:           int = 0
  tire_collision_index: int = 0
  
def read_hitbox_properties(ptr):
  enable = memory.read_u16(ptr + 0x0)
  pos = read_vec3(ptr + 0x4)
  radius = memory.read_f32(ptr + 0x10)
  walls_only = memory.read_u16(ptr + 0x14) 
  tire_collision_index = memory.read_u16(ptr + 0x16)

  return hitbox_properties(enable, pos, radius, walls_only, tire_collision_index)
  
@dataclass
class wheel_properties:
  enable:           int = 0
  dist_suspension:  float = 0.0
  speed_suspension: float = 0.0
  slack_y:          float = 0.0
  rel_pos:          float = 0.0
  x_rot:            float = 0.0
  wheel_radius:     float = 0.0
  sphere_radius:    float = 0.0
  
def read_wheel_properties(ptr):
  enable            = memory.read_u16(ptr + 0x0)
  dist_suspension   = memory.read_f32(ptr + 0x4)
  speed_suspension  = memory.read_f32(ptr + 0x8)
  slack_y           = memory.read_f32(ptr + 0xC)
  rel_pos           = read_vec3(ptr + 0x10)
  x_rot             = memory.read_f32(ptr + 0x1C)
  wheel_radius      = memory.read_f32(ptr + 0x20)
  sphere_radius     = memory.read_f32(ptr + 0x24)

  return wheel_properties(enable, dist_suspension, speed_suspension, slack_y, rel_pos, x_rot, wheel_radius, sphere_radius)

# scope of KartObjectManager
def getKartObjectHolder():
    id = utils.get_game_id()
    address = {"RMCE01": 0x809BD110, "RMCP01": 0x809C18F8, "RMCJ01": 0x809C0958, "RMCK01": 0x809AFF38}
    return address[id]

class KartObject:
    def __init__(self, playerIdx=0):
        self.playerIdx = playerIdx
        
    @staticmethod
    # don't know what data type this is
    def player_array(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x20, 0x0], 'u32')
        
    def player_count(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x24], 'u8')    

class KartSub:
    def __init__(self, playerIdx=0):
        self.playerIdx = playerIdx
    
    @staticmethod
    def position(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x3C], 'u8')
    
    def floor_collision_count(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x40], 'u16')

class KartMove:
    def __init__(self, playerIdx=0):
        self.playerIdx = playerIdx
        
    @staticmethod
    def speed_multiplier(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x10], 'f32')
        
    def base_speed(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x14], 'f32')
        
    def soft_speed_limit(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x18], 'f32')
        
    def speed(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x20], 'f32')
        
    def last_speed(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x24], 'f32')
        
    def hard_speed_limit(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x2C], 'f32')
        
    def acceleration(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x30], 'f32')
        
    def speed_drag_multiplier(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x34], 'f32')
        
    def smoothed_up(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x38, 0x0], 'vec3')
    
    def up(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x44, 0x0], 'vec3')
    
    def landing_dir(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x50, 0x0], 'vec3')
    
    def dir(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x5C, 0x0], 'vec3')
        
    def last_dir(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x68, 0x0], 'vec3')
        
    def vel1_dir(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x74, 0x0], 'vec3')
        
    def dir_diff(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x8C, 0x0], 'vec3')
        
    def has_landing_dir(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x98], 'u8')
        
    def outside_drift_angle(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x9C], 'f32')
        
    def landing_angle(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0xA0], 'f32')
        
    def outside_drift_last_dir(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0xA4, 0x0], 'vec3')
        
    def speed_ratio_capped(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0xB0], 'f32')
        
    def speed_ratio(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0xB4], 'f32')
        
    def kcl_speed_factor(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0xB8], 'f32')
        
    def kcl_rot_factor(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0xBC], 'f32')
        
    def kcl_wheel_speed_factor(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0xC0], 'f32')
        
    def kcl_wheel_rot_factor(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0xC4], 'f32')
        
    def floor_collision_count(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0xC8], 'u16')
    
    def hop_stick_x(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0xCC], 'u32')
    
    def hop_frame(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0xD0], 'u32')
    
    def hop_up(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0xD4, 0x0], 'vec3')
        
    def hop_dir(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0xE0, 0x0], 'vec3')
    
    def slipstream_charge(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0xEC], 'u32')

    def diving_rot(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0xF4], 'f32')
        
    def standstill_boost_rot(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0xF8], 'f32')
    
        # drift_state - 1: charging mt; 2: mt charged
    def drift_state(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0xFC], 'u16')
        
    def mt_charge(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0xFE], 'u16')
    
    def smt_charge(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x100], 'u16')
        
    def mt_boost_timer(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x102], 'u16')
        
    def outside_drift_bonus(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x104], 'f32')
        
    def trick_timer(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x114], 'u16')
        
    def zipper_boost(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x12C], 'u16')
        
    def zipper_boost_max(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x12E], 'u16')
        
    def offroad_invincibility(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x148], 'u16')
        
    def ssmt_charge(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x14C], 'u16')
        
    def real_turn(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x158], 'f32')
        
    def weighted_turn(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x15C], 'f32')

    def scale(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x164, 0x0], 'vec3')
    
    def shock_speed_modifier(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x178], 'f32')
    
    def mega_scale(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x17C], 'f32')
    
    def mushroom_timer(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x188], 'u16')

    def star_timer(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x18A], 'u16')
        
    def shock_timer(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x18C], 'u16')
        
    def ink_timer(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x18E], 'u16')
        
    def ink_applied(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x190], 'u8')

    def crush_timer(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x192], 'u16')
        
    def mega_timer(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x194], 'u16')
        
    def jump_pad_min_speed(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x1B0], 'f32')
        
    def jump_pad_max_speed(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x1B4], 'f32')
        
    def jump_pad_properties(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x10], 'jump_pad')
        
    def ramp_boost(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0xC4], 'u16')
        
    def last_pos(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x1E8, 0x0], 'vec3')
        
    def airtime(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x218], 'u32')
        
    def hop_vel_y(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x228], 'f32')
    
    def hop_pos_y(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x22C], 'f32')
    
    def hop_gravity(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x230], 'f32')
    
        # driving_direction - 0: FORWARDS; 1: BRAKING; 2: WAITING_FOR_BACKWARDS; 3: BACKWARDS
    def driving_direction(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x248], 'u32')
    
    def backwards_allow_counter(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x24C], 'u16')

        # special_floor - 1: BOOST_PANEL; 2: BOOST_RAMP; 4: JUMP_PAD
    def special_floor(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x250], 'u32')
        
    def raw_turn(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x288], 'f32')
        
    def ghost_stop_timer(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x290], 'u16')
        
    def lean_rot(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x294], 'f32')
    
    def lean_rot_cap(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x298], 'f32')
    
    def lean_rot_inc(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x29C], 'f32')

    def wheelie_rot(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x2A0], 'f32')
        
    def wheelie_frames(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x2A8], 'u32')
        
    def wheelie_cooldown(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x2B6], 'u16')
        
    def wheelie_rot_dec(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x2B8], 'f32')
        
def PlayerSub10_284(offset, playerIdx, data_type):
    return core.chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x284, 0x0, 0x0, offset], data_type)

def PlayerSub10_2C0(offset, playerIdx, data_type):
    return core.chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x2C0, 0x0, 0x0, offset], data_type)
    
class KartAction:
    def __init__(self, playerIdx=0):
        self.playerIdx = playerIdx
        
    @staticmethod
    def frame(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x14, 0xC4], 'u32')

class KartCollide:
    def __init__(self, playerIdx=0):
        self.playerIdx = playerIdx
        
    @staticmethod
    # SurfaceProperties = 0x1: WALL; 0x2: SOLID_OOB; 0x10: BOOST_RAMP; 0x40: OFFROAD;
    #                     0x100: BOOST_PANEL_OR_RAMP; 0x800: TRICKABLE
    def surface_properties(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x18, 0x2C], 'surface')

    def pre_respawn_timer(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x18, 0x48], 'u16')
    
    def solid_oob_timer(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x18, 0x4A], 'u16')

class KartState:
    def __init__(self, playerIdx=0):
        self.playerIdx = playerIdx
        
    @staticmethod
    def bitfield_0(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x1C, 0x4], 'u32')
    
    def bitfield_1(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x1C, 0x8], 'u32')
    
    def bitfield_2(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x1C, 0xC], 'u32')
        
    def bitfield_3(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x1C, 0x10], 'u32')
    
    def bitfield_4(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x1C, 0x14], 'u32')
    
    def airtime(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x1C, 0x1C], 'u32')
        
    def top(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x1C, 0x28, 0x0], 'vec3')
    
    def hwg_timer(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x1C, 0x6C], 'u32')
        
    def boost_ramp_type(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x1C, 0x74], 'u32')
    
    def jump_pad_type(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x1C, 0x78], 'u32')
        
    def cnpt_id(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x1C, 0x80], 'u32')
        
    def stick_x(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x1C, 0x88], 'f32')
        
    def stick_y(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x1C, 0x8C], 'f32')
    
    def oob_wipe_state(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x1C, 0x90], 'u32')
    
    def oob_wipe_frame(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x1C, 0x94], 'u32')
    
    def start_boost_charge(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x1C, 0x9C], 'f32')
        
    def start_boost_idx(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x1C, 0xA0], 'f32')
        
    def trickable_timer(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x1C, 0xA6], 'u16')
        
def PlayerSub20(offset, playerIdx, data_type):
    return core.chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x20, offset], data_type)

# speed_limit does not work
class KartBoost:
    def __init__(self, playerIdx=0):
        self.playerIdx = playerIdx
        
    @staticmethod
    def all_mt(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x10C], 's16')
        
    def mushroom_and_boost_panel(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x110], 's16')
        
    def trick_and_zipper(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x114], 's16')

    def type(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x118], 's16')

    def multiplier(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x11C], 'f32')
        
    def acceleration(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x120], 'f32')
        
    def speed_limit(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x124], 'f32')

# needs testing
class KartJump:
    def __init__(self, playerIdx=0):
        self.playerIdx = playerIdx
        
    @staticmethod
    def type(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x258, 0x10], 'u16')
    
    def category(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x258, 0x14], 'u32')
        
    def next_direction(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x258, 0x18], 'u8')
        
    def next_allow_timer(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x258, 0x1A], 'u16')
        
    def rot_direction(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x258, 0x10], 'u32')
       
    def properties(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x258, 0x10], 'trick')
    
    def angle(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x258, 0x24], 'f32')

    def angle_diff(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x258, 0x28], 'f32')
    
    def angle_diff_mul(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x258, 0x2C], 'f32')
    
    def angle_diff_mul_dec(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x258, 0x30], 'f32')
        
    def final_angle(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x258, 0x34], 'f32')
        
    def cooldown(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x258, 0x38], 'u16')
        
    def boost_ramp_enabled(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x258, 0x3A], 'u8')
        
    def rot(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x258, 0x34], 'quatf')

def PlayerZipper(offset, playerIdx, data_type):
    return core.chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x10, 0x10, 0x25C, offset], data_type)

# should work
class KartParam:
    def __init__(self, playerIdx=0):
        self.playerIdx = playerIdx
        
    @staticmethod
    def is_bike(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x0], 'u32')
        
    def vehicle(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x4], 'u32')
        
    def character(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x8], 'u32')
        
    def wheel_count0(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0xC], 'u16')
        
    def wheel_count1(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0xE], 'u16')
        
    def player_idx(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x10], 'u8')
        
    def wheel_count_recip(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x2C], 'f32')
        
    def wheel_count_plus_one_recip(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x30], 'f32')

# should work
class PlayerStats:
    def __init__(self, playerIdx=0):
        self.playerIdx = playerIdx
        
    @staticmethod
    def wheel_count(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0x0], 'u32')
        
    def vehicle_type(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0x4], 'u32')
        
    def weight_class(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0x8], 'u32')
        
    def weight(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0x10], 'f32')
        
    def bump_deviation_level(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0x14], 'f32')
        
    def base_speed(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0x18], 'f32')
        
    def turning_speed(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0x1C], 'f32')
        
    def tilt(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0x20], 'f32')
        
    def accel_standard_a0(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0x24], 'f32')
    
    def accel_standard_a1(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0x28], 'f32')
    
    def accel_standard_a2(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0x2C], 'f32')

    def accel_standard_a3(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0x30], 'f32')
    
    def accel_standard_t1(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0x34], 'f32')

    def accel_standard_t2(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0x38], 'f32')
    
    def accel_standard_t3(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0x3C], 'f32')
        
    def accel_drift_a0(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0x40], 'f32')
    
    def accel_drift_a1(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0x44], 'f32')
        
    def accel_drift_a2(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0x48], 'f32')

    def manual_handling(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0x4C], 'f32')
    
    def auto_handling(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0x50], 'f32')
        
    def handling_react(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0x54], 'f32')
    
    def manual_drift(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0x58], 'f32')
        
    def auto_drift(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0x5C], 'f32')
        
    def drift_react(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0x60], 'f32')
        
    def outside_drift_target_angle(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0x64], 'f32')
        
    def outside_drift_decrement(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0x68], 'f32')
    
    def mt_duration(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0x6C], 'u32')
        
    def kcl_speed_00(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0x70], 'f32')
        
    def kcl_speed_01(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0x74], 'f32')
    
    def kcl_speed_02(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0x78], 'f32')
        
    def kcl_speed_03(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0x7C], 'f32')

    def kcl_speed_04(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0x80], 'f32')
        
    def kcl_speed_05(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0x84], 'f32')
        
    def kcl_speed_06(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0x88], 'f32')
        
    def kcl_speed_07(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0x8C], 'f32')
   
    def kcl_speed_08(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0x90], 'f32')
        
    def kcl_speed_09(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0x94], 'f32')

    def kcl_speed_0A(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0x98], 'f32')
        
    def kcl_speed_0B(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0x9C], 'f32')    
        
    def kcl_speed_0C(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0xA0], 'f32')
        
    def kcl_speed_0D(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0xA4], 'f32')
    
    def kcl_speed_0E(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0xA8], 'f32')
        
    def kcl_speed_0F(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0xAC], 'f32')
        
    def kcl_speed_10(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0xB0], 'f32')
        
    def kcl_speed_11(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0xB4], 'f32')
    
    def kcl_speed_12(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0xB8], 'f32')
        
    def kcl_speed_13(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0xBC], 'f32')

    def kcl_speed_14(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0xC0], 'f32')
        
    def kcl_speed_15(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0xC4], 'f32')
        
    def kcl_speed_16(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0xC8], 'f32')
        
    def kcl_speed_17(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0xCC], 'f32')
   
    def kcl_speed_18(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0xD0], 'f32')
        
    def kcl_speed_19(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0xD4], 'f32')

    def kcl_speed_1A(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0xD8], 'f32')
        
    def kcl_speed_1B(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0xDC], 'f32')    
        
    def kcl_speed_1C(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0xE0], 'f32')
        
    def kcl_speed_1D(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0xE4], 'f32')
    
    def kcl_speed_1E(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0xE8], 'f32')
        
    def kcl_speed_1F(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0xEC], 'f32')
        
    def kcl_rot_00(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0xF0], 'f32')
        
    def kcl_rot_01(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0xF4], 'f32')
    
    def kcl_rot_02(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0xF8], 'f32')
        
    def kcl_rot_03(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0xFC], 'f32')

    def kcl_rot_04(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0x100], 'f32')
        
    def kcl_rot_05(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0x104], 'f32')
        
    def kcl_rot_06(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0x108], 'f32')
        
    def kcl_rot_07(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0x10C], 'f32')
   
    def kcl_rot_08(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0x110], 'f32')
        
    def kcl_rot_09(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0x114], 'f32')

    def kcl_rot_0A(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0x118], 'f32')
        
    def kcl_rot_0B(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0x11C], 'f32')    
        
    def kcl_rot_0C(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0x120], 'f32')
        
    def kcl_rot_0D(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0x124], 'f32')
    
    def kcl_rot_0E(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0x128], 'f32')
        
    def kcl_rot_0F(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0x12C], 'f32')
        
    def kcl_rot_10(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0x130], 'f32')
        
    def kcl_rot_11(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0x134], 'f32')
    
    def kcl_rot_12(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0x138], 'f32')
        
    def kcl_rot_13(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0x13C], 'f32')

    def kcl_rot_14(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0x140], 'f32')
        
    def kcl_rot_15(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0x144], 'f32')
        
    def kcl_rot_16(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0x148], 'f32')
        
    def kcl_rot_17(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0x14C], 'f32')
   
    def kcl_rot_18(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0x150], 'f32')
        
    def kcl_rot_19(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0x154], 'f32')

    def kcl_rot_1A(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0x158], 'f32')
        
    def kcl_rot_1B(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0x15C], 'f32')    
        
    def kcl_rot_1C(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0x160], 'f32')
        
    def kcl_rot_1D(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0x164], 'f32')
    
    def kcl_rot_1E(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0x168], 'f32')
        
    def kcl_rot_1F(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0x16C], 'f32')

    def item_radius_z(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0x170], 'f32')
        
    def item_radius_x(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0x174], 'f32')
        
    def item_distance_y(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0x178], 'f32')
        
    def item_offset(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0x17C], 'f32')
        
    def max_normal_acceleration(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0x180], 'f32')
        
    def mega_scale(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0x184], 'f32')
        
    def tire_distance(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0, 0x188], 'f32')
     
# needs testing     
class PlayerGPStats:
    def __init__(self, playerIdx=0):
        self.playerIdx = playerIdx
        
    @staticmethod
    def start_boost_successful(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x34, 0x0], 'u8')
        
    def mts(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x34, 0x4], 'u32')
    
    def offroad(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x34, 0x8], 'u32')
    
    def wallCollision(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x34, 0xC], 'u32')
        
    def object_collision(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x34, 0x10], 'u32')
        
    def oob(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x34, 0x14], 'u32')
        
    def eighteen(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x0, 0x34, 0x18], 'u16')

class VehicleDynamics:
    def __init__(self, playerIdx=0):
        self.playerIdx = playerIdx
        
    @staticmethod
    def pos(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x8, 0x90, 0x18], 'vec3')
    
    def conserved_special_rot(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x8, 0x90, 0x24], 'quatf')
    
    def non_conserved_special_rot(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x8, 0x90, 0x34], 'quatf')
        
    def special_rot(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x8, 0x90, 0x44], 'quatf')
        
    def mat(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x8, 0x90, 0x9C], 'mat34')
        
    def mat_col0(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x8, 0x90, 0xCC], 'vec3')
        
    def mat_col1(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x8, 0x90, 0xD8], 'vec3')
        
    def mat_col2(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x8, 0x90, 0xE4], 'vec3')
        
    def speed(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x8, 0x90, 0xF0], 'vec3')
  
# incomplete, pointer chain works
class VehiclePhysics:
    def __init__(self, playerIdx=0):
        self.playerIdx = playerIdx
        
    @staticmethod
    def inertia_tensor(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x8, 0x90, 0x4, 0x68], 'mat34')
        
    def inv_inertia_tensor(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x8, 0x90, 0x4, 0x68], 'mat34')
        
    def rot_speed(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x8, 0x90, 0x4, 0x64], 'f32')
    
    def pos(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x8, 0x90, 0x4, 0x68], 'vec3')
        
    def external_velocity(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x8, 0x90, 0x4, 0x74], 'vec3')

    def external_velocity_accel(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x8, 0x90, 0x4, 0x80], 'vec3')
    
    def external_velocity_rot_vec(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x8, 0x90, 0x4, 0xA4], 'vec3')
        
    def moving_road_velocity(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x8, 0x90, 0x4, 0xB0], 'vec3')
        
    def internal_velocity_rot_vec(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x8, 0x90, 0x4, 0xBC], 'vec3')
        
    def moving_water_velocity(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x8, 0x90, 0x4, 0xC8], 'vec3')
        
    def speed(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x8, 0x90, 0x4, 0xD4], 'vec3')
        
    def speed_norm(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x8, 0x90, 0x4, 0xE0], 'vec3')
    
    def moving_road_rot_vec(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x8, 0x90, 0x4, 0xE4], 'vec3')
        
    def rot(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x8, 0x90, 0x4, 0xF0], 'quatf')
    
    def rot2(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x8, 0x90, 0x4, 0x100], 'quatf')

    def accel_norm(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x8, 0x90, 0x4, 0x110], 'vec3')
        
    def rot_vec_norm(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x8, 0x90, 0x4, 0x11C], 'vec3')
        
    def special_rot(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x8, 0x90, 0x4, 0x128], 'vec3')
    
    def gravity(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x8, 0x90, 0x4, 0x148], 'f32')

    def internal_velocity(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x8, 0x90, 0x4, 0x14C], 'vec3')
        
    def top(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x8, 0x90, 0x4, 0x158], 'vec3')
        
    def no_gravity(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x8, 0x90, 0x4, 0x171], 'u8')

    def in_bullet(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x8, 0x90, 0x4, 0x174], 'u8')
        
    def stabilization_factor(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x8, 0x90, 0x4, 0x178], 'f32')
        
    def speed_fix(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x8, 0x90, 0x4, 0x17C], 'f32')

    def top2(playerIdx=0):
        return chase_pointer(getKartObjectHolder(), [0x20, playerIdx * 0x4, 0x0, 0x8, 0x90, 0x4, 0x180], 'vec3')

# scope of RaceData
def getRaceDataHolder(playerIdx=0):
    id = utils.get_game_id()
    address = {"RMCE01": 0x809B8F68 + (playerIdx * 0x4), "RMCP01": 0x809BD728 + (playerIdx * 0x4), "RMCJ01": 0x809BC788 + (playerIdx * 0x4), "RMCK01": 0x809ABD68 + (playerIdx * 0x4)}
    return address[id]

class RaceDataScenario:
    def __init__(self, scenarioIdx=0):
        self.scenarioIdx = scenarioIdx
        
    @staticmethod
    def player_count(scenarioIdx=0):
        return chase_pointer(getRaceDataHolder(), [0x20 + (0xBF0 * scenarioIdx) + 0x4], 'u8')
        
    def hud_count(scenarioIdx=0):
        return chase_pointer(getRaceDataHolder(), [0x20 + (0xBF0 * scenarioIdx) + 0x5], 'u8')
        
    def local_player_count(scenarioIdx=0):
        return chase_pointer(getRaceDataHolder(), [0x20 + (0xBF0 * scenarioIdx) + 0x6], 'u8')    
    
    def hud_count2(scenarioIdx=0):
        return chase_pointer(getRaceDataHolder(), [0x20 + (0xBF0 * scenarioIdx) + 0x7], 'u8')

class RaceDataPlayer:
    def __init__(self, playerIdx=0, scenarioIdx=0):
        self.playerIdx = playerIdx
        self.scenarioIdx = scenarioIdx
        
    @staticmethod
    def local_player_num(playerIdx=0, scenarioIdx=0):
        return chase_pointer(getRaceDataHolder(), [0x20 + (0xBF0 * scenarioIdx) + 0x8 + (0xF0 * playerIdx) + 0x5], 'u8')
        
    def player_input_idx(playerIdx=0, scenarioIdx=0):
        return chase_pointer(getRaceDataHolder(), [0x20 + (0xBF0 * scenarioIdx) + 0x8 + (0xF0 * playerIdx) + 0x6], 'u8')
    
    def vehicle_id(playerIdx=0, scenarioIdx=0):
        return chase_pointer(getRaceDataHolder(), [0x20 + (0xBF0 * scenarioIdx) + 0x8 + (0xF0 * playerIdx) + 0x8], 'u32')
         
    def character_id(playerIdx=0, scenarioIdx=0):
        return chase_pointer(getRaceDataHolder(), [0x20 + (0xBF0 * scenarioIdx) + 0x8 + (0xF0 * playerIdx) + 0xC], 'u32')

    def player_type(playerIdx=0, scenarioIdx=0):
        return chase_pointer(getRaceDataHolder(), [0x20 + (0xBF0 * scenarioIdx) + 0x8 + (0xF0 * playerIdx) + 0x10], 'u32')
    
    def team(playerIdx=0, scenarioIdx=0):
        return chase_pointer(getRaceDataHolder(), [0x20 + (0xBF0 * scenarioIdx) + 0x8 + (0xF0 * playerIdx) + 0xCC], 'u32')
        
    def controller_id(playerIdx=0, scenarioIdx=0):
        return chase_pointer(getRaceDataHolder(), [0x20 + (0xBF0 * scenarioIdx) + 0x8 + (0xF0 * playerIdx) + 0xD0], 'u32')
       
    def previous_score(playerIdx=0, scenarioIdx=0):
        return chase_pointer(getRaceDataHolder(), [0x20 + (0xBF0 * scenarioIdx) + 0x8 + (0xF0 * playerIdx) + 0xD8], 'u16')
        
    def gp_score(playerIdx=0, scenarioIdx=0):
        return chase_pointer(getRaceDataHolder(), [0x20 + (0xBF0 * scenarioIdx) + 0x8 + (0xF0 * playerIdx) + 0xDA], 'u16')

    def gp_rank_score(playerIdx=0, scenarioIdx=0):
        return chase_pointer(getRaceDataHolder(), [0x20 + (0xBF0 * scenarioIdx) + 0x8 + (0xF0 * playerIdx) + 0xDE], 'u16')
        
    def prev_finish_pos(playerIdx=0, scenarioIdx=0):
        return chase_pointer(getRaceDataHolder(), [0x20 + (0xBF0 * scenarioIdx) + 0x8 + (0xF0 * playerIdx) + 0xE1], 'u8')
        
    def finish_pos(playerIdx=0, scenarioIdx=0):
        return chase_pointer(getRaceDataHolder(), [0x20 + (0xBF0 * scenarioIdx) + 0x8 + (0xF0 * playerIdx) + 0xE2], 'u8')
        
    def rating(playerIdx=0, scenarioIdx=0):
        return chase_pointer(getRaceDataHolder(), [0x20 + (0xBF0 * scenarioIdx) + 0x8 + (0xF0 * playerIdx) + 0xE8], 'u16')
        
class RaceDataSettings:
    def __init__(self, scenarioIdx=0):
        self.scenarioIdx = scenarioIdx
        
    @staticmethod
    def course_id(scenarioIdx=0):
        return chase_pointer(getRaceDataHolder(), [0x20 + (0xBF0 * scenarioIdx) + 0xB48 + 0x0], 'u32')

    def engine_class(scenarioIdx=0):
        return chase_pointer(getRaceDataHolder(), [0x20 + (0xBF0 * scenarioIdx) + 0xB48 + 0x4], 'u32')

    def game_mode(scenarioIdx=0):
        return chase_pointer(getRaceDataHolder(), [0x20 + (0xBF0 * scenarioIdx) + 0xB48 + 0x8], 'u32')
      
    def game_type(scenarioIdx=0):
        return chase_pointer(getRaceDataHolder(), [0x20 + (0xBF0 * scenarioIdx) + 0xB48 + 0xC], 'u32')
        
    def battle_type(scenarioIdx=0):
        return chase_pointer(getRaceDataHolder(), [0x20 + (0xBF0 * scenarioIdx) + 0xB48 + 0x10], 'u32')
        
    def cpu_mode(scenarioIdx=0):
        return chase_pointer(getRaceDataHolder(), [0x20 + (0xBF0 * scenarioIdx) + 0xB48 + 0x14], 'u32')
        
    def item_mode(scenarioIdx=0):
        return chase_pointer(getRaceDataHolder(), [0x20 + (0xBF0 * scenarioIdx) + 0xB48 + 0x18], 'u32')
    
    def hud_players_i0(scenarioIdx=0):
        return chase_pointer(getRaceDataHolder(), [0x20 + (0xBF0 * scenarioIdx) + 0xB48 + 0x1C], 'u8')
        
    def hud_players_i1(scenarioIdx=0):
        return chase_pointer(getRaceDataHolder(), [0x20 + (0xBF0 * scenarioIdx) + 0xB48 + 0x1D], 'u8')
        
    def hud_players_i2(scenarioIdx=0):
        return chase_pointer(getRaceDataHolder(), [0x20 + (0xBF0 * scenarioIdx) + 0xB48 + 0x1E], 'u8')
        
    def hud_players_i3(scenarioIdx=0):
        return chase_pointer(getRaceDataHolder(), [0x20 + (0xBF0 * scenarioIdx) + 0xB48 + 0x1F], 'u8')

    def cup_id(scenarioIdx=0):
        return chase_pointer(getRaceDataHolder(), [0x20 + (0xBF0 * scenarioIdx) + 0xB48 + 0x20], 'u32')
    
    def race_number(scenarioIdx=0):
        return chase_pointer(getRaceDataHolder(), [0x20 + (0xBF0 * scenarioIdx) + 0xB48 + 0x24], 'u8')
        
    def lap_count(scenarioIdx=0):
        return chase_pointer(getRaceDataHolder(), [0x20 + (0xBF0 * scenarioIdx) + 0xB48 + 0x25], 'u8')
    
    def mode_flags(scenarioIdx=0):
        return chase_pointer(getRaceDataHolder(), [0x20 + (0xBF0 * scenarioIdx) + 0xB48 + 0x28], 'u32')
        
    def seed0(scenarioIdx=0):
        return chase_pointer(getRaceDataHolder(), [0x20 + (0xBF0 * scenarioIdx) + 0xB48 + 0x2C], 'u32')
        
    def seed1(scenarioIdx=0):
        return chase_pointer(getRaceDataHolder(), [0x20 + (0xBF0 * scenarioIdx) + 0xB48 + 0x30], 'u32')

    
# scope of RaceInfo
def getRaceInfoHolder(playerIdx=0):
    id = utils.get_game_id()
    address = {"RMCE01": 0x809B8F70 + (playerIdx * 0x4), "RMCP01": 0x809BD730 + (playerIdx * 0x4), "RMCJ01": 0x809BC790 + (playerIdx * 0x4), "RMCK01": 0x809ABD70 + (playerIdx * 0x4)}
    return address[id]
    
# this is for player only
def getInputStorageAddresses():
    addrFace = chase_pointer(getRaceInfoHolder(), [0xC, 0x0, 0x48, 0xE8, 0x10], 'u32')
    addrDI = addrFace + 0x276C
    addrTrick = addrDI + 0x276C
    
    return [addrFace, addrDI, addrTrick]
    
def GetGhostAddressBase():
    raceData = chase_pointer(getRaceInfoHolder(0), [0xC, 0x4, 0x48, 0x4], 'u32')
    addrFace = memory.read_u32(raceData + 0x94)
    addrDI = memory.read_u32(raceData + 0x98)
    addrTrick = memory.read_u32(raceData + 0x9C)
    
    return [addrFace, addrDI, addrTrick]
    
def getGhostAddressPointer():
    addrFace, addrDI, addrTrick = GetGhostAddressBase()
    return [addrFace + 0x4, addrDI + 0x4, addrTrick + 0x4]
    
def getGhostAddresses():
    addrFace, addrDI, addrTrick = getGhostAddressPointer()
    
    return [memory.read_u32(addrFace), memory.read_u32(addrDI), memory.read_u32(addrTrick)]
    
def getGhostAddressLengthPointer():
    addrFace, addrDI, addrTrick = GetGhostAddressBase()
    return [addrFace + 0xC, addrDI + 0xC, addrTrick + 0xC]

# should work
class RaceInfoPlayer:
    def __init__(self, playerIdx=0):
        self.playerIdx = playerIdx
        
    @staticmethod
    def idx(playerIdx=0):
        return chase_pointer(getRaceInfoHolder(), [0xC, playerIdx, 0x8], 'u8')
    
    def checkpoint_id(playerIdx=0):
        return chase_pointer(getRaceInfoHolder(), [0xC, playerIdx, 0xA], 'u16')
        
    def race_completion(playerIdx=0):
        return chase_pointer(getRaceInfoHolder(), [0xC, playerIdx, 0xC], 'f32')
        
    def race_completion_max(playerIdx=0):
        return chase_pointer(getRaceInfoHolder(), [0xC, playerIdx, 0x10], 'f32')
        
    def checkpoint_factor(playerIdx=0):
        return chase_pointer(getRaceInfoHolder(), [0xC, playerIdx, 0x14], 'f32')
        
    def checkpoint_start_lap_completion(playerIdx=0):
        return chase_pointer(getRaceInfoHolder(), [0xC, playerIdx, 0x18], 'f32')
        
    def lap_completion(playerIdx=0):
        return chase_pointer(getRaceInfoHolder(), [0xC, playerIdx, 0x1C], 'f32')
        
    def position(playerIdx=0):
        return chase_pointer(getRaceInfoHolder(), [0xC, playerIdx, 0x20], 'u8')
        
    def respawn_point(playerIdx=0):
        return chase_pointer(getRaceInfoHolder(), [0xC, playerIdx, 0x21], 'u8')
    
    def battle_score(playerIdx=0):
        return chase_pointer(getRaceInfoHolder(), [0xC, playerIdx, 0x22], 'u16')
        
    def current_lap(playerIdx=0):
        return chase_pointer(getRaceInfoHolder(), [0xC, playerIdx, 0x24], 'u16')
        
    def max_lap(playerIdx=0):
        return chase_pointer(getRaceInfoHolder(), [0xC, playerIdx * 0x4, 0x26], 'u8')
    
    def max_kcp(playerIdx=0):
        return chase_pointer(getRaceInfoHolder(), [0xC, playerIdx, 0x27], 'u8')
    
    def frame_counter(playerIdx=0):
        return chase_pointer(getRaceInfoHolder(), [0xC, playerIdx, 0x2C], 'u32')
        
    def frames_in_first_place(playerIdx=0):
        return chase_pointer(getRaceInfoHolder(), [0xC, playerIdx, 0x30], 'u32')
        
    def flags(playerIdx=0):
        return chase_pointer(getRaceInfoHolder(), [0xC, playerIdx, 0x38], 'u32')
        
    def ablr_buttons(playerIdx=0):
        return chase_pointer(getRaceInfoHolder(), [0xC, playerIdx, 0x48, 0x38, 0x4, 0x9], 'u8')
        
    def x_button(playerIdx=0):
        return chase_pointer(getRaceInfoHolder(), [0xC, playerIdx, 0x48, 0x38, 0x4, 0x14], 'u8')

    def y_button(playerIdx=0):
        return chase_pointer(getRaceInfoHolder(), [0xC, playerIdx, 0x48, 0x38, 0x4, 0x15], 'u8')
        
    def dpad(playerIdx=0):
        return chase_pointer(getRaceInfoHolder(), [0xC, playerIdx, 0x48, 0x38, 0x4, 0x17], 'u8')
        
    def stick_x(playerIdx=0):
        return chase_pointer(getRaceInfoHolder(), [0xC, playerIdx, 0x48, 0x38], 'u8')

    def stick_y(playerIdx=0):
        return chase_pointer(getRaceInfoHolder(), [0xC, playerIdx, 0x48, 0x39], 'u8')
        
class RaceInfo:
    def intro_timer():
        return chase_pointer(getRaceInfoHolder(), [0x1E], 'u16')

    def timer():
        return chase_pointer(getRaceInfoHolder(), [0x20], 'u32')
        
    def stage():
        return chase_pointer(getRaceInfoHolder(), [0x28], 'u32')
        
    def spectator_mode():
        return chase_pointer(getRaceInfoHolder(), [0x2D], 'u8')
        
    def can_countdown_start():
        return chase_pointer(getRaceInfoHolder(), [0x2E], 'u8')
        
    def cutscene_mode():
        return chase_pointer(getRaceInfoHolder(), [0x2F], 'u8')

class InputMgr:
    @staticmethod
    def chain():
        address = {"RMCE01": 0x809b8f4c, "RMCP01": 0x809bd70c, "RMCJ01": 0x809bc76c, "RMCK01": 0x809abd4c}
        return address[utils.get_game_id()]
        
    def drift_id(playerIdx=0):
        return chase_pointer(InputMgr.chain() + (playerIdx * 0x4), [0xC4], 'u16')