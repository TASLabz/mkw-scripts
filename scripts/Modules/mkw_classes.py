# NOTE (xi): unfinished, vabold is taking the duty of rewriting this
# currently only for the use of testing other scripts that rely on this module

from dolphin import memory, utils
from dataclasses import dataclass
# will be removed soon
from Modules import mkw_core as core
  
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

  return trick_properties(initial_angle_diff, angle_diff_min,
                          angle_diff_mul_min, angle_diff_mul_dec)
  
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
  
  return surface_properties(wall, solid_oob, boost_ramp, offroad,
                            boost_panel_or_ramp, trickable)
  
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

  return wheel_properties(enable, dist_suspension, speed_suspension, slack_y,
                          rel_pos, x_rot, wheel_radius, sphere_radius)

# scope of KartObjectManager
def getKartObjectHolder():
    id = utils.get_game_id()
    address = {"RMCE01": 0x809BD110, "RMCP01": 0x809C18F8,
               "RMCJ01": 0x809C0958, "RMCK01": 0x809AFF38}
    return address[id]

class KartObject:
    def __init__(self, playerIdx=0):
        self.playerIdx = playerIdx
        
    @staticmethod
    # don't know what data type this is
    def player_array(playerIdx=0):
        offsets = [0x20, playerIdx * 0x4, 0x20, 0x0]
        return chase_pointer(getKartObjectHolder(), offsets, 'u32')
        
    @staticmethod
    def player_count(playerIdx=0):
        offsets = [0x20, playerIdx * 0x4, 0x24]
        return chase_pointer(getKartObjectHolder(), offsets, 'u8')    

class KartSub:
    def __init__(self, playerIdx=0):
        self.playerIdx = playerIdx
    
    @staticmethod
    def position(playerIdx=0):
        offsets = [0x20, playerIdx * 0x4, 0x10, 0x3C]
        return chase_pointer(getKartObjectHolder(), offsets, 'u8')
    
    @staticmethod
    def floor_collision_count(playerIdx=0):
        offsets = [0x20, playerIdx * 0x4, 0x10, 0x40]
        return chase_pointer(getKartObjectHolder(), offsets, 'u16')

class KartMove:
    def __init__(self, playerIdx=0):
        self.playerIdx = playerIdx
        
    @staticmethod
    def instance(playerIdx=0):
        offsets = [0x20, playerIdx * 0x4, 0x10, 0x10]
        return chase_pointer(getKartObjectHolder(), offsets, 'u32')
        
    @staticmethod
    def speed_multiplier(playerIdx=0):
        return memory.read_f32(KartMove.instance(playerIdx) + 0x10)
    
    @staticmethod
    def base_speed(playerIdx=0):
        return memory.read_f32(KartMove.instance(playerIdx) + 0x14)
        
    @staticmethod
    def soft_speed_limit(playerIdx=0):
        return memory.read_f32(KartMove.instance(playerIdx) + 0x18)
        
    @staticmethod
    def speed(playerIdx=0):
        return memory.read_f32(KartMove.instance(playerIdx) + 0x20)
        
    @staticmethod
    def last_speed(playerIdx=0):
        return memory.read_f32(KartMove.instance(playerIdx) + 0x24)
        
    @staticmethod
    def hard_speed_limit(playerIdx=0):
        return memory.read_f32(KartMove.instance(playerIdx) + 0x2C)
        
    @staticmethod
    def acceleration(playerIdx=0):
        return memory.read_f32(KartMove.instance(playerIdx) + 0x30)
        
    @staticmethod
    def speed_drag_multiplier(playerIdx=0):
        return memory.read_f32(KartMove.instance(playerIdx) + 0x34)
        
    @staticmethod
    def smoothed_up(playerIdx=0):
        return chase_pointer(KartMove.instance(playerIdx) + 0x38, [0x0], 'vec3')
    
    @staticmethod
    def up(playerIdx=0):
        return chase_pointer(KartMove.instance(playerIdx) + 0x44, [0x0], 'vec3')
    
    @staticmethod
    def landing_dir(playerIdx=0):
        return chase_pointer(KartMove.instance(playerIdx) + 0x50, [0x0], 'vec3')
    
    @staticmethod
    def dir(playerIdx=0):
        return chase_pointer(KartMove.instance(playerIdx) + 0x5C, [0x0], 'vec3')
        
    @staticmethod
    def last_dir(playerIdx=0):
        return chase_pointer(KartMove.instance(playerIdx) + 0x68, [0x0], 'vec3')
    
    @staticmethod
    def vel1_dir(playerIdx=0):
        return chase_pointer(KartMove.instance(playerIdx) + 0x74, [0x0], 'vec3')
        
    @staticmethod
    def dir_diff(playerIdx=0):
        return chase_pointer(KartMove.instance(playerIdx) + 0x8C, [0x0], 'vec3')
        
    @staticmethod
    def has_landing_dir(playerIdx=0):
        return memory.read_u8(KartMove.instance(playerIdx) + 0x98)
        
    @staticmethod
    def outside_drift_angle(playerIdx=0):
        return memory.read_f32(KartMove.instance(playerIdx) + 0x9C)
        
    @staticmethod
    def landing_angle(playerIdx=0):
        return memory.read_f32(KartMove.instance(playerIdx) + 0xA0)
        
    @staticmethod
    def outside_drift_last_dir(playerIdx=0):
        return chase_pointer(KartMove.instance(playerIdx) + 0xA4, [0x0], 'vec3')
        
    @staticmethod
    def speed_ratio_capped(playerIdx=0):
        return memory.read_f32(KartMove.instance(playerIdx) + 0xB0)
        
    @staticmethod
    def speed_ratio(playerIdx=0):
        return memory.read_f32(KartMove.instance(playerIdx) + 0xB4)
        
    @staticmethod
    def kcl_speed_factor(playerIdx=0):
        return memory.read_f32(KartMove.instance(playerIdx) + 0xB8)
        
    @staticmethod
    def kcl_rot_factor(playerIdx=0):
        return memory.read_f32(KartMove.instance(playerIdx) + 0xBC)
        
    @staticmethod
    def kcl_wheel_speed_factor(playerIdx=0):
        return memory.read_f32(KartMove.instance(playerIdx) + 0xC0)
        
    @staticmethod
    def kcl_wheel_rot_factor(playerIdx=0):
        return memory.read_f32(KartMove.instance(playerIdx) + 0xC4)
        
    @staticmethod
    def floor_collision_count(playerIdx=0):
        return memory.read_u16(KartMove.instance(playerIdx) + 0xC8)
    
    @staticmethod
    def hop_stick_x(playerIdx=0):
        return memory.read_u32(KartMove.instance(playerIdx) + 0xCC)
    
    @staticmethod
    def hop_frame(playerIdx=0):
        return memory.read_u32(KartMove.instance(playerIdx) + 0xD0)
    
    @staticmethod
    def hop_up(playerIdx=0):
        return chase_pointer(KartMove.instance(playerIdx) + 0xD4, [0x0], 'vec3')
        
    @staticmethod
    def hop_dir(playerIdx=0):
        return chase_pointer(KartMove.instance(playerIdx) + 0xE0, [0x0], 'vec3')
    
    @staticmethod
    def slipstream_charge(playerIdx=0):
        return memory.read_u32(KartMove.instance(playerIdx) + 0xEC)
    
    @staticmethod
    def diving_rot(playerIdx=0):
        return memory.read_f32(KartMove.instance(playerIdx) + 0xF4)
        
    @staticmethod
    def standstill_boost_rot(playerIdx=0):
        return memory.read_f32(KartMove.instance(playerIdx) + 0xF8)
    
    # drift_state - 1: charging mt; 2: mt charged
    @staticmethod
    def drift_state(playerIdx=0):
        return memory.read_u16(KartMove.instance(playerIdx) + 0xFC)
        
    @staticmethod
    def mt_charge(playerIdx=0):
        return memory.read_u16(KartMove.instance(playerIdx) + 0xFE)
    
    @staticmethod
    def smt_charge(playerIdx=0):
        return memory.read_u16(KartMove.instance(playerIdx) + 0x100)
        
    @staticmethod
    def mt_boost_timer(playerIdx=0):
        return memory.read_u16(KartMove.instance(playerIdx) + 0x102)
        
    @staticmethod
    def outside_drift_bonus(playerIdx=0):
        return memory.read_f32(KartMove.instance(playerIdx) + 0x104)
        
    @staticmethod
    def trick_timer(playerIdx=0):
        return memory.read_u16(KartMove.instance(playerIdx) + 0x114)
        
    @staticmethod
    def zipper_boost(playerIdx=0):
        return memory.read_u16(KartMove.instance(playerIdx) + 0x12C)
        
    @staticmethod
    def zipper_boost_max(playerIdx=0):
        return memory.read_u16(KartMove.instance(playerIdx) + 0x12E)
        
    @staticmethod
    def offroad_invincibility(playerIdx=0):
        return memory.read_u16(KartMove.instance(playerIdx) + 0x148)
        
    @staticmethod
    def ssmt_charge(playerIdx=0):
        return memory.read_u16(KartMove.instance(playerIdx) + 0x14C)
        
    @staticmethod
    def real_turn(playerIdx=0):
        return memory.read_f32(KartMove.instance(playerIdx) + 0x158)
        
    @staticmethod
    def weighted_turn(playerIdx=0):
        return memory.read_f32(KartMove.instance(playerIdx) + 0x15C)
        
    @staticmethod
    def scale(playerIdx=0):
        return chase_pointer(KartMove.instance(playerIdx) + 0x164, [0x0], 'vec3')
    
    @staticmethod
    def shock_speed_modifier(playerIdx=0):
        return memory.read_f32(KartMove.instance(playerIdx) + 0x178)
    
    @staticmethod
    def mega_scale(playerIdx=0):
        return memory.read_f32(KartMove.instance(playerIdx) + 0x17C)
    
    @staticmethod
    def mushroom_timer(playerIdx=0):
        return memory.read_u16(KartMove.instance(playerIdx) + 0x188)
    
    @staticmethod
    def star_timer(playerIdx=0):
        return memory.read_u16(KartMove.instance(playerIdx) + 0x18A)
        
    @staticmethod
    def shock_timer(playerIdx=0):
        return memory.read_u16(KartMove.instance(playerIdx) + 0x18C)
        
    @staticmethod
    def ink_timer(playerIdx=0):
        return memory.read_u16(KartMove.instance(playerIdx) + 0x18E)
        
    @staticmethod
    def ink_applied(playerIdx=0):
        return memory.read_u8(KartMove.instance(playerIdx) + 0x190)
    
    @staticmethod
    def crush_timer(playerIdx=0):
        return memory.read_u16(KartMove.instance(playerIdx) + 0x192)
        
    @staticmethod
    def mega_timer(playerIdx=0):
        return memory.read_u16(KartMove.instance(playerIdx) + 0x194)
        
    @staticmethod
    def jump_pad_min_speed(playerIdx=0):
        return memory.read_f32(KartMove.instance(playerIdx) + 0x1B0)
        
    @staticmethod
    def jump_pad_max_speed(playerIdx=0):
        return memory.read_f32(KartMove.instance(playerIdx) + 0x1B4)
        
    @staticmethod
    def jump_pad_properties(playerIdx=0):
        return read_jump_pad_properties(KartMove.instance(playerIdx) + 0x10)
        
    @staticmethod
    def ramp_boost(playerIdx=0):
        return memory.read_u16(KartMove.instance(playerIdx) + 0xC4)
        
    @staticmethod
    def last_pos(playerIdx=0):
        return chase_pointer(KartMove.instance(playerIdx) + 0x1E8, [0x0], 'vec3')
        
    @staticmethod
    def airtime(playerIdx=0):
        return memory.read_u32(KartMove.instance(playerIdx) + 0x218)
        
    @staticmethod
    def hop_vel_y(playerIdx=0):
        return memory.read_f32(KartMove.instance(playerIdx) + 0x228)
    
    @staticmethod
    def hop_pos_y(playerIdx=0):
        return memory.read_f32(KartMove.instance(playerIdx) + 0x22C)
    
    @staticmethod
    def hop_gravity(playerIdx=0):
        return memory.read_f32(KartMove.instance(playerIdx) + 0x230)
    
    # driving_direction - 0: FORWARDS; 1: BRAKING;
    # 2: WAITING_FOR_BACKWARDS; 3: BACKWARDS
    @staticmethod
    def driving_direction(playerIdx=0):
        return memory.read_u32(KartMove.instance(playerIdx) + 0x248)
    
    @staticmethod
    def backwards_allow_counter(playerIdx=0):
        return memory.read_u16(KartMove.instance(playerIdx) + 0x24C)

    # special_floor - 1: BOOST_PANEL; 2: BOOST_RAMP; 4: JUMP_PAD
    @staticmethod
    def special_floor(playerIdx=0):
        return memory.read_u32(KartMove.instance(playerIdx) + 0x250)
        
    @staticmethod
    def raw_turn(playerIdx=0):
        return memory.read_f32(KartMove.instance(playerIdx) + 0x288)
        
    @staticmethod
    def ghost_stop_timer(playerIdx=0):
        return memory.read_u16(KartMove.instance(playerIdx) + 0x290)
        
    @staticmethod
    def lean_rot(playerIdx=0):
        return memory.read_f32(KartMove.instance(playerIdx) + 0x294)
    
    @staticmethod
    def lean_rot_cap(playerIdx=0):
        return memory.read_f32(KartMove.instance(playerIdx) + 0x298)
    
    @staticmethod
    def lean_rot_inc(playerIdx=0):
        return memory.read_f32(KartMove.instance(playerIdx) + 0x29C)

    @staticmethod
    def wheelie_rot(playerIdx=0):
        return memory.read_f32(KartMove.instance(playerIdx) + 0x2A0)
        
    @staticmethod
    def wheelie_frames(playerIdx=0):
        return memory.read_u32(KartMove.instance(playerIdx) + 0x2A8)
        
    @staticmethod
    def wheelie_cooldown(playerIdx=0):
        return memory.read_u16(KartMove.instance(playerIdx) + 0x2B6)
        
    @staticmethod
    def wheelie_rot_dec(playerIdx=0):
        return memory.read_f32(KartMove.instance(playerIdx) + 0x2B8)
        
    @staticmethod
    def PlayerSub10_284(offset, playerIdx, data_type):
        offsets = [0x0, 0x0, offset]
        return chase_pointer(KartMove.instance(playerIdx) + 0x284, offsets, data_type)
    
    @staticmethod
    def PlayerSub10_2C0(offset, playerIdx, data_type):
        offsets = [0x0, 0x0, offset]
        return chase_pointer(KartMove.instance(playerIdx) + 0x2C0, offsets, data_type)
    
class KartAction:
    def __init__(self, playerIdx=0):
        self.playerIdx = playerIdx
        
    @staticmethod
    def frame(playerIdx=0):
        offsets = [0x20, playerIdx * 0x4, 0x10, 0x10, 0x14, 0xC4]
        return chase_pointer(getKartObjectHolder(), offsets, 'u32')

class KartCollide:
    # TODO: Condense offsets into general instance() function for this class's location
    def __init__(self, playerIdx=0):
        self.playerIdx = playerIdx
        
    # SurfaceProperties = 0x1: WALL; 0x2: SOLID_OOB; 0x10: BOOST_RAMP; 0x40: OFFROAD;
    #                     0x100: BOOST_PANEL_OR_RAMP; 0x800: TRICKABLE
    @staticmethod
    def surface_properties(playerIdx=0):
        offsets = [0x20, playerIdx * 0x4, 0x10, 0x18, 0x2C]
        return chase_pointer(getKartObjectHolder(), offsets, 'surface')
    
    @staticmethod
    def pre_respawn_timer(playerIdx=0):
        offsets = [0x20, playerIdx * 0x4, 0x10, 0x10, 0x18, 0x48]
        return chase_pointer(getKartObjectHolder(), offsets, 'u16')
    
    @staticmethod
    def solid_oob_timer(playerIdx=0):
        offsets = [0x20, playerIdx * 0x4, 0x10, 0x10, 0x18, 0x4A]
        return chase_pointer(getKartObjectHolder(), offsets, 'u16')

class KartState:
    def __init__(self, playerIdx=0):
        self.playerIdx = playerIdx
        
    @staticmethod
    def instance(playerIdx=0):
        offsets = [0x20, playerIdx * 0x4, 0x10, 0x10, 0x1C]
        return chase_pointer(getKartObjectHolder(), offsets, 'u32')
        
    @staticmethod
    def bitfield_0(playerIdx=0):
        return memory.read_u32(KartState.instance(playerIdx) + 0x4)
    
    @staticmethod
    def bitfield_1(playerIdx=0):
        return memory.read_u32(KartState.instance(playerIdx) + 0x8)
    
    @staticmethod
    def bitfield_2(playerIdx=0):
        return memory.read_u32(KartState.instance(playerIdx) + 0xC)
        
    @staticmethod
    def bitfield_3(playerIdx=0):
        return memory.read_u32(KartState.instance(playerIdx) + 0x10)
    
    @staticmethod
    def bitfield_4(playerIdx=0):
        return memory.read_u32(KartState.instance(playerIdx) + 0x14)
    
    @staticmethod
    def airtime(playerIdx=0):
        return memory.read_u32(KartState.instance(playerIdx) + 0x1C)
    
    @staticmethod
    def top(playerIdx=0):
        return chase_pointer(KartState.instance(playerIdx) + 0x28, [0x0], 'vec3')
    
    @staticmethod
    def hwg_timer(playerIdx=0):
        return memory.read_u32(KartState.instance(playerIdx) + 0x6C)
        
    @staticmethod
    def boost_ramp_type(playerIdx=0):
        return memory.read_u32(KartState.instance(playerIdx) + 0x74)
    
    @staticmethod
    def jump_pad_type(playerIdx=0):
        return memory.read_u32(KartState.instance(playerIdx) + 0x78)
        
    @staticmethod
    def cnpt_id(playerIdx=0):
        return memory.read_u32(KartState.instance(playerIdx) + 0x80)
        
    @staticmethod
    def stick_x(playerIdx=0):
        return memory.read_f32(KartState.instance(playerIdx) + 0x88)
        
    @staticmethod
    def stick_y(playerIdx=0):
        return memory.read_f32(KartState.instance(playerIdx) + 0x8C)
    
    @staticmethod
    def oob_wipe_state(playerIdx=0):
        return memory.read_u32(KartState.instance(playerIdx) + 0x90)
    
    @staticmethod
    def oob_wipe_frame(playerIdx=0):
        return memory.read_u32(KartState.instance(playerIdx) + 0x94)
    
    @staticmethod
    def start_boost_charge(playerIdx=0):
        return memory.read_f32(KartState.instance(playerIdx) + 0x9C)
        
    @staticmethod
    def start_boost_idx(playerIdx=0):
        return memory.read_f32(KartState.instance(playerIdx) + 0xA0)
        
    @staticmethod
    def trickable_timer(playerIdx=0):
        return memory.read_u16(KartState.instance(playerIdx) + 0xA6)
        
def PlayerSub20(offset, playerIdx, data_type):
    offsets = [0x20, playerIdx * 0x4, 0x10, 0x10, 0x20, offset]
    return core.chase_pointer(getKartObjectHolder(), offsets, data_type)

# speed_limit does not work
class KartBoost:
    def __init__(self, playerIdx=0):
        self.playerIdx = playerIdx
        
    @staticmethod
    # TODO: This is the same definition as KartMove.instance()...
    # They should share a common getter function
    def instance(playerIdx=0):
        offsets = [0x20, playerIdx * 0x4, 0x10, 0x10]
        return chase_pointer(getKartObjectHolder(), offsets, 'u32')
        
    @staticmethod
    def all_mt(playerIdx=0):
        return memory.read_s16(KartBoost.instance(playerIdx) + 0x10C)
        
    @staticmethod
    def mushroom_and_boost_panel(playerIdx=0):
        return memory.read_s16(KartBoost.instance(playerIdx) + 0x110)
        
    @staticmethod
    def trick_and_zipper(playerIdx=0):
        return memory.read_s16(KartBoost.instance(playerIdx) + 0x114)

    @staticmethod
    def type(playerIdx=0):
        return memory.read_s16(KartBoost.instance(playerIdx) + 0x118)

    @staticmethod
    def multiplier(playerIdx=0):
        return memory.read_f32(KartBoost.instance(playerIdx) + 0x11C)
        
    @staticmethod
    def acceleration(playerIdx=0):
        return memory.read_f32(KartBoost.instance(playerIdx) + 0x120)
        
    @staticmethod
    def speed_limit(playerIdx=0):
        return memory.read_f32(KartBoost.instance(playerIdx) + 0x124)

# needs testing
class KartJump:
    def __init__(self, playerIdx=0):
        self.playerIdx = playerIdx
        
    @staticmethod
    def instance(playerIdx=0):
        offsets = [0x20, playerIdx * 0x4, 0x10, 0x10, 0x258]
        return chase_pointer(getKartObjectHolder(), offsets, 'u32')
        
    @staticmethod
    # TODO: Somebody messed up...
    # This is identical to rot_direction() and properties()
    def type(playerIdx=0):
        return memory.read_u16(KartJump.instance(playerIdx) + 0x10)
    
    @staticmethod
    def category(playerIdx=0):
        return memory.read_u32(KartJump.instance(playerIdx) + 0x14)
        
    @staticmethod
    def next_direction(playerIdx=0):
        return memory.read_u8(KartJump.instance(playerIdx) + 0x18)
        
    @staticmethod
    def next_allow_timer(playerIdx=0):
        return memory.read_u16(KartJump.instance(playerIdx) + 0x1A)
        
    @staticmethod
    def rot_direction(playerIdx=0):
        return memory.read_u32(KartJump.instance(playerIdx) + 0x10)
    
    @staticmethod
    def properties(playerIdx=0):
        return read_trick_properties(KartJump.instance(playerIdx) + 0x10)
    
    @staticmethod
    def angle(playerIdx=0):
        return memory.read_f32(KartJump.instance(playerIdx) + 0x24)
    
    @staticmethod
    def angle_diff(playerIdx=0):
        return memory.read_f32(KartJump.instance(playerIdx) + 0x28)
    
    @staticmethod
    def angle_diff_mul(playerIdx=0):
        return memory.read_f32(KartJump.instance(playerIdx) + 0x2C)
    
    @staticmethod
    def angle_diff_mul_dec(playerIdx=0):
        return memory.read_f32(KartJump.instance(playerIdx) + 0x30)
    
    @staticmethod
    def final_angle(playerIdx=0):
        return memory.read_f32(KartJump.instance(playerIdx) + 0x34)
        
    @staticmethod
    def cooldown(playerIdx=0):
        return memory.read_u16(KartJump.instance(playerIdx) + 0x38)
        
    @staticmethod
    def boost_ramp_enabled(playerIdx=0):
        return memory.read_u8(KartJump.instance(playerIdx) + 0x3A)
        
    @staticmethod
    # TODO: This is the same as final_angle?
    def rot(playerIdx=0):
        return read_quatf(KartJump.instance(playerIdx) + 0x34)

def PlayerZipper(offset, playerIdx, data_type):
    offsets = [0x20, playerIdx * 0x4, 0x10, 0x10, 0x25C, offset]
    return core.chase_pointer(getKartObjectHolder(), offsets, data_type)

# should work
class KartParam:
    def __init__(self, playerIdx=0):
        self.playerIdx = playerIdx
        
    @staticmethod
    def instance(playerIdx=0):
        offsets = [0x20, playerIdx * 0x4, 0x0, 0x0]
        return chase_pointer(getKartObjectHolder(), offsets, 'u32')
        
    @staticmethod
    def is_bike(playerIdx=0):
        return memory.read_u32(KartParam.instance(playerIdx) + 0x0)
        
    @staticmethod
    def vehicle(playerIdx=0):
        return memory.read_u32(KartParam.instance(playerIdx) + 0x4)
        
    @staticmethod
    def character(playerIdx=0):
        return memory.read_u32(KartParam.instance(playerIdx) + 0x8)
        
    @staticmethod
    def wheel_count0(playerIdx=0):
        return memory.read_u16(KartParam.instance(playerIdx) + 0xC)
        
    @staticmethod
    def wheel_count1(playerIdx=0):
        return memory.read_u16(KartParam.instance(playerIdx) + 0xE)
        
    @staticmethod
    def player_idx(playerIdx=0):
        return memory.read_u8(KartParam.instance(playerIdx) + 0x10)
        
    @staticmethod
    def wheel_count_recip(playerIdx=0):
        return memory.read_f32(KartParam.instance(playerIdx) + 0x2C)
        
    @staticmethod
    def wheel_count_plus_one_recip(playerIdx=0):
        return memory.read_f32(KartParam.instance(playerIdx) + 0x30)

# should work
class PlayerStats:
    def __init__(self, playerIdx=0):
        self.playerIdx = playerIdx
        
    @staticmethod
    def instance(playerIdx=0):
        offsets = [0x20, playerIdx * 0x4, 0x0, 0x0, 0x14, 0x0]
        return chase_pointer(getKartObjectHolder(), offsets, 'u32')
        
    @staticmethod
    def wheel_count(playerIdx=0):
        return memory.read_u32(PlayerStats.instance(playerIdx) + 0x0)
        
    @staticmethod
    def vehicle_type(playerIdx=0):
        return memory.read_u32(PlayerStats.instance(playerIdx) + 0x4)
        
    @staticmethod
    def weight_class(playerIdx=0):
        return memory.read_u32(PlayerStats.instance(playerIdx) + 0x8)
        
    @staticmethod
    def weight(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0x10)
        
    @staticmethod
    def bump_deviation_level(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0x14)
        
    @staticmethod
    def base_speed(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0x18)
        
    @staticmethod
    def turning_speed(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0x1C)
        
    @staticmethod
    def tilt(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0x20)
        
    @staticmethod
    def accel_standard_a0(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0x24)
    
    @staticmethod
    def accel_standard_a1(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0x28)
    
    @staticmethod
    def accel_standard_a2(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0x2C)
    
    @staticmethod
    def accel_standard_a3(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0x30)
    
    @staticmethod
    def accel_standard_t1(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0x34)
    
    @staticmethod
    def accel_standard_t2(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0x38)
    
    @staticmethod
    def accel_standard_t3(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0x3C)
        
    @staticmethod
    def accel_drift_a0(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0x40)
    
    @staticmethod
    def accel_drift_a1(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0x44)
        
    @staticmethod
    def accel_drift_a2(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0x48)
    
    @staticmethod
    def manual_handling(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0x4C)
    
    @staticmethod
    def auto_handling(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0x50)
        
    @staticmethod
    def handling_react(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0x54)
    
    @staticmethod
    def manual_drift(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0x58)
        
    @staticmethod
    def auto_drift(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0x5C)
        
    @staticmethod
    def drift_react(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0x60)
        
    @staticmethod
    def outside_drift_target_angle(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0x64)
        
    @staticmethod
    def outside_drift_decrement(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0x68)
    
    @staticmethod
    def mt_duration(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0x6C)
        
    @staticmethod
    def kcl_speed_00(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0x70)
        
    @staticmethod
    def kcl_speed_01(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0x74)
    
    @staticmethod
    def kcl_speed_02(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0x78)
        
    @staticmethod
    def kcl_speed_03(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0x7C)
    
    @staticmethod
    def kcl_speed_04(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0x80)
        
    @staticmethod
    def kcl_speed_05(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0x84)
        
    @staticmethod
    def kcl_speed_06(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0x88)
        
    @staticmethod
    def kcl_speed_07(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0x8C)
    
    @staticmethod
    def kcl_speed_08(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0x90)
        
    @staticmethod
    def kcl_speed_09(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0x94)
    
    @staticmethod
    def kcl_speed_0A(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0x98)
        
    @staticmethod
    def kcl_speed_0B(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0x9C)    
        
    @staticmethod
    def kcl_speed_0C(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0xA0)
        
    @staticmethod
    def kcl_speed_0D(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0xA4)
    
    @staticmethod
    def kcl_speed_0E(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0xA8)
        
    @staticmethod
    def kcl_speed_0F(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0xAC)
        
    @staticmethod
    def kcl_speed_10(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0xB0)
        
    @staticmethod
    def kcl_speed_11(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0xB4)
    
    @staticmethod
    def kcl_speed_12(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0xB8)
        
    @staticmethod
    def kcl_speed_13(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0xBC)
    
    @staticmethod
    def kcl_speed_14(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0xC0)
        
    @staticmethod
    def kcl_speed_15(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0xC4)
        
    @staticmethod
    def kcl_speed_16(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0xC8)
        
    @staticmethod
    def kcl_speed_17(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0xCC)
    
    @staticmethod
    def kcl_speed_18(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0xD0)
        
    @staticmethod
    def kcl_speed_19(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0xD4)
    
    @staticmethod
    def kcl_speed_1A(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0xD8)
        
    @staticmethod
    def kcl_speed_1B(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0xDC)    
        
    @staticmethod
    def kcl_speed_1C(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0xE0)
        
    @staticmethod
    def kcl_speed_1D(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0xE4)
    
    @staticmethod
    def kcl_speed_1E(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0xE8)
        
    @staticmethod
    def kcl_speed_1F(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0xEC)
        
    @staticmethod
    def kcl_rot_00(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0xF0)
        
    @staticmethod
    def kcl_rot_01(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0xF4)
    
    @staticmethod
    def kcl_rot_02(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0xF8)
        
    @staticmethod
    def kcl_rot_03(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0xFC)
    
    @staticmethod
    def kcl_rot_04(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0x100)
        
    @staticmethod
    def kcl_rot_05(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0x104)
        
    @staticmethod
    def kcl_rot_06(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0x108)
        
    @staticmethod
    def kcl_rot_07(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0x10C)
    
    @staticmethod
    def kcl_rot_08(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0x110)
        
    @staticmethod
    def kcl_rot_09(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0x114)
    
    @staticmethod
    def kcl_rot_0A(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0x118)
        
    @staticmethod
    def kcl_rot_0B(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0x11C)    
        
    @staticmethod
    def kcl_rot_0C(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0x120)
        
    @staticmethod
    def kcl_rot_0D(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0x124)
    
    @staticmethod
    def kcl_rot_0E(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0x128)
        
    @staticmethod
    def kcl_rot_0F(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0x12C)
        
    @staticmethod
    def kcl_rot_10(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0x130)
        
    @staticmethod
    def kcl_rot_11(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0x134)
    
    @staticmethod
    def kcl_rot_12(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0x138)
        
    @staticmethod
    def kcl_rot_13(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0x13C)
    
    @staticmethod
    def kcl_rot_14(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0x140)
        
    @staticmethod
    def kcl_rot_15(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0x144)
        
    @staticmethod
    def kcl_rot_16(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0x148)
        
    @staticmethod
    def kcl_rot_17(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0x14C)
        
    @staticmethod
    def kcl_rot_18(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0x150)
        
    @staticmethod
    def kcl_rot_19(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0x154)
        
    @staticmethod
    def kcl_rot_1A(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0x158)
        
    @staticmethod
    def kcl_rot_1B(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0x15C)    
        
    @staticmethod
    def kcl_rot_1C(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0x160)
        
    @staticmethod
    def kcl_rot_1D(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0x164)
    
    @staticmethod
    def kcl_rot_1E(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0x168)
        
    @staticmethod
    def kcl_rot_1F(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0x16C)
    
    @staticmethod
    def item_radius_z(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0x170)
        
    @staticmethod
    def item_radius_x(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0x174)
        
    @staticmethod
    def item_distance_y(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0x178)
        
    @staticmethod
    def item_offset(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0x17C)
        
    @staticmethod
    def max_normal_acceleration(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0x180)
        
    @staticmethod
    def mega_scale(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0x184)
        
    @staticmethod
    def tire_distance(playerIdx=0):
        return memory.read_f32(PlayerStats.instance(playerIdx) + 0x188)
    
# needs testing     
class PlayerGPStats:
    def __init__(self, playerIdx=0):
        self.playerIdx = playerIdx
        
    @staticmethod
    def instance(playerIdx=0):
        offsets = [0x20, playerIdx * 0x4, 0x0, 0x0, 0x34]
        return chase_pointer(getKartObjectHolder(), offsets, 'u32')
        
    @staticmethod
    def start_boost_successful(playerIdx=0):
        return memory.read_u8(PlayerGPStats.instance(playerIdx) + 0x0)
    
    @staticmethod
    def mts(playerIdx=0):
        return memory.read_u32(PlayerGPStats.instance(playerIdx) + 0x4)
    
    @staticmethod
    def offroad(playerIdx=0):
        return memory.read_u32(PlayerGPStats.instance(playerIdx) + 0x8)
    
    @staticmethod
    def wallCollision(playerIdx=0):
        return memory.read_u32(PlayerGPStats.instance(playerIdx) + 0xC)
    
    @staticmethod
    def object_collision(playerIdx=0):
        return memory.read_u32(PlayerGPStats.instance(playerIdx) + 0x10)
        
    @staticmethod
    def oob(playerIdx=0):
        return memory.read_u32(PlayerGPStats.instance(playerIdx) + 0x14)
        
    @staticmethod
    def eighteen(playerIdx=0):
        return memory.read_u16(PlayerGPStats.instance(playerIdx) + 0x18)

class VehicleDynamics:
    def __init__(self, playerIdx=0):
        self.playerIdx = playerIdx
        
    @staticmethod
    def instance(playerIdx=0):
        offsets = [0x20, playerIdx * 0x4, 0x0, 0x8, 0x90]
        return chase_pointer(getKartObjectHolder(), offsets, 'u32')
        
    @staticmethod
    def pos(playerIdx=0):
        return read_vec3(VehicleDynamics.instance(playerIdx) + 0x18)
    
    @staticmethod
    def conserved_special_rot(playerIdx=0):
        return read_quatf(VehicleDynamics.instance(playerIdx) + 0x24)
    
    @staticmethod
    def non_conserved_special_rot(playerIdx=0):
        return read_quatf(VehicleDynamics.instance(playerIdx) + 0x34)
        
    @staticmethod
    def special_rot(playerIdx=0):
        return read_quatf(VehicleDynamics.instance(playerIdx) + 0x44)
        
    @staticmethod
    def mat(playerIdx=0):
        return read_mat34(VehicleDynamics.instance(playerIdx) + 0x9C)
        
    @staticmethod
    def mat_col0(playerIdx=0):
        return read_vec3(VehicleDynamics.instance(playerIdx) + 0xCC)
        
    @staticmethod
    def mat_col1(playerIdx=0):
        return read_vec3(VehicleDynamics.instance(playerIdx) + 0xD8)
        
    @staticmethod
    def mat_col2(playerIdx=0):
        return read_vec3(VehicleDynamics.instance(playerIdx) + 0xE4)
        
    @staticmethod
    def speed(playerIdx=0):
        return read_vec3(VehicleDynamics.instance(playerIdx) + 0xF0)
    
# incomplete, pointer chain works
class VehiclePhysics:
    def __init__(self, playerIdx=0):
        self.playerIdx = playerIdx
        
    @staticmethod
    def instance(playerIdx=0):
        offsets = [0x20, playerIdx * 0x4, 0x0, 0x8, 0x90, 0x4]
        return chase_pointer(getKartObjectHolder(), offsets, 'u32')
        
    @staticmethod
    def inertia_tensor(playerIdx=0):
        return read_mat34(VehiclePhysics.instance(playerIdx) + 0x68)
        
    @staticmethod
    # TODO: Same as above???
    def inv_inertia_tensor(playerIdx=0):
        return read_mat34(VehiclePhysics.instance(playerIdx) + 0x68)
        
    @staticmethod
    def rot_speed(playerIdx=0):
        return memory.read_f32(VehiclePhysics.instance(playerIdx) + 0x64)
    
    @staticmethod
    # TODO: Same as intertia???
    def pos(playerIdx=0):
        return read_vec3(VehiclePhysics.instance(playerIdx) + 0x68)
        
    @staticmethod
    def external_velocity(playerIdx=0):
        return read_vec3(VehiclePhysics.instance(playerIdx) + 0x74)
    
    @staticmethod
    def external_velocity_accel(playerIdx=0):
        return read_vec3(VehiclePhysics.instance(playerIdx) + 0x80)
    
    @staticmethod
    def external_velocity_rot_vec(playerIdx=0):
        return read_vec3(VehiclePhysics.instance(playerIdx) + 0xA4)
        
    @staticmethod
    def moving_road_velocity(playerIdx=0):
        return read_vec3(VehiclePhysics.instance(playerIdx) + 0xB0)
        
    @staticmethod
    def internal_velocity_rot_vec(playerIdx=0):
        return read_vec3(VehiclePhysics.instance(playerIdx) + 0xBC)
        
    @staticmethod
    def moving_water_velocity(playerIdx=0):
        return read_vec3(VehiclePhysics.instance(playerIdx) + 0xC8)
        
    @staticmethod
    def speed(playerIdx=0):
        return read_vec3(VehiclePhysics.instance(playerIdx) + 0xD4)
        
    @staticmethod
    def speed_norm(playerIdx=0):
        return read_vec3(VehiclePhysics.instance(playerIdx) + 0xE0)
    
    @staticmethod
    def moving_road_rot_vec(playerIdx=0):
        return read_vec3(VehiclePhysics.instance(playerIdx) + 0xE4)
        
    @staticmethod
    def rot(playerIdx=0):
        return read_quatf(VehiclePhysics.instance(playerIdx) + 0xF0)
    
    @staticmethod
    def rot2(playerIdx=0):
        return read_quatf(VehiclePhysics.instance(playerIdx) + 0x100)
    
    @staticmethod
    def accel_norm(playerIdx=0):
        return read_vec3(VehiclePhysics.instance(playerIdx) + 0x110)
    
    @staticmethod    
    def rot_vec_norm(playerIdx=0):
        return read_vec3(VehiclePhysics.instance(playerIdx) + 0x11C)
        
    @staticmethod
    def special_rot(playerIdx=0):
        return read_vec3(VehiclePhysics.instance(playerIdx) + 0x128)
    
    @staticmethod
    def gravity(playerIdx=0):
        return memory.read_f32(VehiclePhysics.instance(playerIdx) + 0x148)
    
    @staticmethod
    def internal_velocity(playerIdx=0):
        return read_vec3(VehiclePhysics.instance(playerIdx) + 0x14C)
    
    @staticmethod
    def top(playerIdx=0):
        return read_vec3(VehiclePhysics.instance(playerIdx) + 0x158)
        
    @staticmethod
    def no_gravity(playerIdx=0):
        return memory.read_u8(VehiclePhysics.instance(playerIdx) + 0x171)
    
    @staticmethod
    def in_bullet(playerIdx=0):
        return memory.read_u8(VehiclePhysics.instance(playerIdx) + 0x174)
        
    @staticmethod
    def stabilization_factor(playerIdx=0):
        return memory.read_f32(VehiclePhysics.instance(playerIdx) + 0x178)
        
    @staticmethod
    def speed_fix(playerIdx=0):
        return memory.read_f32(VehiclePhysics.instance(playerIdx) + 0x17C)
    
    @staticmethod
    def top2(playerIdx=0):
        return read_vec3(VehiclePhysics.instance(playerIdx) + 0x180)
    
# scope of RaceData
def getRaceDataHolder(playerIdx=0):
    id = utils.get_game_id()
    address = {"RMCE01": 0x809B8F68, "RMCP01": 0x809BD728,
               "RMCJ01": 0x809BC788, "RMCK01": 0x809ABD68}
    return address[id] + (playerIdx * 0x4)

class RaceDataScenario:
    def __init__(self, scenarioIdx=0):
        self.scenarioIdx = scenarioIdx
        
    @staticmethod
    #TODO: Validate this is correct
    def apply_offset(scenarioIdx=0, offset=0):
        return 0x20 + (0xBF0 * scenarioIdx) + offset
        
    @staticmethod
    def player_count(scenarioIdx=0):
        offset = RaceDataScenario.apply_offset(scenarioIdx, 0x4)
        return chase_pointer(getRaceDataHolder(), [offset], 'u8')
    
    @staticmethod
    def hud_count(scenarioIdx=0):
        offset = RaceDataScenario.apply_offset(scenarioIdx, 0x5)
        return chase_pointer(getRaceDataHolder(), [offset], 'u8')
        
    @staticmethod
    def local_player_count(scenarioIdx=0):
        offset = RaceDataScenario.apply_offset(scenarioIdx, 0x6)
        return chase_pointer(getRaceDataHolder(), [offset], 'u8')
    
    @staticmethod
    def hud_count2(scenarioIdx=0):
        offset = RaceDataScenario.apply_offset(scenarioIdx, 0x7)
        return chase_pointer(getRaceDataHolder(), [offset], 'u8')

class RaceDataPlayer:
    def __init__(self, playerIdx=0, scenarioIdx=0):
        self.playerIdx = playerIdx
        self.scenarioIdx = scenarioIdx
        
    @staticmethod
    def apply_offset(playerIdx=0, scenarioIdx=0, offset=0):
        return 0x20 + (0xBF0 * scenarioIdx) + 0x8 + (0xF0 * playerIdx) + offset
        
    @staticmethod
    def local_player_num(playerIdx=0, scenarioIdx=0):
        offset = RaceDataPlayer.apply_offset(playerIdx, scenarioIdx, 0x5)
        return chase_pointer(getRaceDataHolder(), [offset], 'u8')
        
    @staticmethod
    def player_input_idx(playerIdx=0, scenarioIdx=0):
        offset = RaceDataPlayer.apply_offset(playerIdx, scenarioIdx, 0x6)
        return chase_pointer(getRaceDataHolder(), [offset], 'u8')
    
    @staticmethod
    def vehicle_id(playerIdx=0, scenarioIdx=0):
        offset = RaceDataPlayer.apply_offset(playerIdx, scenarioIdx, 0x8)
        return chase_pointer(getRaceDataHolder(), [offset], 'u32')
         
    @staticmethod
    def character_id(playerIdx=0, scenarioIdx=0):
        offset = RaceDataPlayer.apply_offset(playerIdx, scenarioIdx, 0xC)
        return chase_pointer(getRaceDataHolder(), [offset], 'u32')
    
    @staticmethod
    def player_type(playerIdx=0, scenarioIdx=0):
        offset = RaceDataPlayer.apply_offset(playerIdx, scenarioIdx, 0x10)
        return chase_pointer(getRaceDataHolder(), [offset], 'u32')
    
    @staticmethod
    def team(playerIdx=0, scenarioIdx=0):
        offset = RaceDataPlayer.apply_offset(playerIdx, scenarioIdx, 0xCC)
        return chase_pointer(getRaceDataHolder(), [offset], 'u32')
        
    @staticmethod
    def controller_id(playerIdx=0, scenarioIdx=0):
        offset = RaceDataPlayer.apply_offset(playerIdx, scenarioIdx, 0xD0)
        return chase_pointer(getRaceDataHolder(), [offset], 'u32')
    
    @staticmethod
    def previous_score(playerIdx=0, scenarioIdx=0):
        offset = RaceDataPlayer.apply_offset(playerIdx, scenarioIdx, 0xD8)
        return chase_pointer(getRaceDataHolder(), [offset], 'u16')
    
    @staticmethod
    def gp_score(playerIdx=0, scenarioIdx=0):
        offset = RaceDataPlayer.apply_offset(playerIdx, scenarioIdx, 0xDA)
        return chase_pointer(getRaceDataHolder(), [offset], 'u16')
    
    @staticmethod
    def gp_rank_score(playerIdx=0, scenarioIdx=0):
        offset = RaceDataPlayer.apply_offset(playerIdx, scenarioIdx, 0xDE)
        return chase_pointer(getRaceDataHolder(), [offset], 'u16')
    
    @staticmethod
    def prev_finish_pos(playerIdx=0, scenarioIdx=0):
        offset = RaceDataPlayer.apply_offset(playerIdx, scenarioIdx, 0xE1)
        return chase_pointer(getRaceDataHolder(), [offset], 'u8')
        
    @staticmethod
    def finish_pos(playerIdx=0, scenarioIdx=0):
        offset = RaceDataPlayer.apply_offset(playerIdx, scenarioIdx, 0xE2)
        return chase_pointer(getRaceDataHolder(), [offset], 'u8')
        
    @staticmethod
    def rating(playerIdx=0, scenarioIdx=0):
        offset = RaceDataPlayer.apply_offset(playerIdx, scenarioIdx, 0xE8)
        return chase_pointer(getRaceDataHolder(), [offset], 'u8')
        
class RaceDataSettings:
    def __init__(self, scenarioIdx=0):
        self.scenarioIdx = scenarioIdx
        
    @staticmethod
    def apply_offset(scenarioIdx=0, offset=0):
        return 0x20 + (0xBF0 * scenarioIdx) + 0xB48 + offset
        
    @staticmethod
    def course_id(scenarioIdx=0):
        offset = RaceDataSettings.apply_offset(scenarioIdx, 0x0)
        return chase_pointer(getRaceDataHolder(), [offset], 'u32')
    
    @staticmethod
    def engine_class(scenarioIdx=0):
        offset = RaceDataSettings.apply_offset(scenarioIdx, 0x4)
        return chase_pointer(getRaceDataHolder(), [offset], 'u32')
    
    @staticmethod
    def game_mode(scenarioIdx=0):
        offset = RaceDataSettings.apply_offset(scenarioIdx, 0x8)
        return chase_pointer(getRaceDataHolder(), [offset], 'u32')
    
    @staticmethod
    def game_type(scenarioIdx=0):
        offset = RaceDataSettings.apply_offset(scenarioIdx, 0xC)
        return chase_pointer(getRaceDataHolder(), [offset], 'u32')
    
    @staticmethod
    def battle_type(scenarioIdx=0):
        offset = RaceDataSettings.apply_offset(scenarioIdx, 0x10)
        return chase_pointer(getRaceDataHolder(), [offset], 'u32')
    
    @staticmethod
    def cpu_mode(scenarioIdx=0):
        offset = RaceDataSettings.apply_offset(scenarioIdx, 0x14)
        return chase_pointer(getRaceDataHolder(), [offset], 'u32')
        
    @staticmethod
    def item_mode(scenarioIdx=0):
        offset = RaceDataSettings.apply_offset(scenarioIdx, 0x18)
        return chase_pointer(getRaceDataHolder(), [offset], 'u32')
    
    @staticmethod
    def hud_players_i0(scenarioIdx=0):
        offset = RaceDataSettings.apply_offset(scenarioIdx, 0x1C)
        return chase_pointer(getRaceDataHolder(), [offset], 'u8')
        
    @staticmethod
    def hud_players_i1(scenarioIdx=0):
        offset = RaceDataSettings.apply_offset(scenarioIdx, 0x1D)
        return chase_pointer(getRaceDataHolder(), [offset], 'u8')
        
    @staticmethod
    def hud_players_i2(scenarioIdx=0):
        offset = RaceDataSettings.apply_offset(scenarioIdx, 0x1E)
        return chase_pointer(getRaceDataHolder(), [offset], 'u8')
        
    @staticmethod
    def hud_players_i3(scenarioIdx=0):
        offset = RaceDataSettings.apply_offset(scenarioIdx, 0x1F)
        return chase_pointer(getRaceDataHolder(), [offset], 'u8')
        
    @staticmethod
    def cup_id(scenarioIdx=0):
        offset = RaceDataSettings.apply_offset(scenarioIdx, 0x20)
        return chase_pointer(getRaceDataHolder(), [offset], 'u32')
    
    @staticmethod
    def race_number(scenarioIdx=0):
        offset = RaceDataSettings.apply_offset(scenarioIdx, 0x24)
        return chase_pointer(getRaceDataHolder(), [offset], 'u8')
        
    @staticmethod
    def lap_count(scenarioIdx=0):
        offset = RaceDataSettings.apply_offset(scenarioIdx, 0x25)
        return chase_pointer(getRaceDataHolder(), [offset], 'u8')
    
    @staticmethod
    def mode_flags(scenarioIdx=0):
        offset = RaceDataSettings.apply_offset(scenarioIdx, 0x28)
        return chase_pointer(getRaceDataHolder(), [offset], 'u32')
        
    @staticmethod
    def seed0(scenarioIdx=0):
        offset = RaceDataSettings.apply_offset(scenarioIdx, 0x2C)
        return chase_pointer(getRaceDataHolder(), [offset], 'u32')
        
    @staticmethod
    def seed1(scenarioIdx=0):
        offset = RaceDataSettings.apply_offset(scenarioIdx, 0x30)
        return chase_pointer(getRaceDataHolder(), [offset], 'u32')
    
# scope of RaceInfo
def getRaceInfoHolder(playerIdx=0):
    id = utils.get_game_id()
    address = {"RMCE01": 0x809B8F70, "RMCP01": 0x809BD730,
               "RMCJ01": 0x809BC790, "RMCK01": 0x809ABD70}
    return address[id] + (playerIdx * 0x4)
    
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
    return list(map(memory.read_u32, getGhostAddressPointer()))
    
def getGhostAddressLengthPointer():
    addrFace, addrDI, addrTrick = GetGhostAddressBase()
    return [addrFace + 0xC, addrDI + 0xC, addrTrick + 0xC]

# should work
class RaceInfoPlayer:
    def __init__(self, playerIdx=0):
        self.playerIdx = playerIdx
        
    @staticmethod
    def instance(playerIdx=0):
        return chase_pointer(getRaceInfoHolder(), [0xC, playerIdx * 0x4], 'u32')
        
    @staticmethod
    def idx(playerIdx=0):
        return memory.read_u8(RaceInfoPlayer.instance(playerIdx) + 0x8)
    
    @staticmethod
    def checkpoint_id(playerIdx=0):
        return memory.read_u16(RaceInfoPlayer.instance(playerIdx) + 0xA)
        
    @staticmethod
    def race_completion(playerIdx=0):
        return memory.read_f32(RaceInfoPlayer.instance(playerIdx) + 0xC)
        
    @staticmethod
    def race_completion_max(playerIdx=0):
        return memory.read_f32(RaceInfoPlayer.instance(playerIdx) + 0x10)
        
    @staticmethod
    def checkpoint_factor(playerIdx=0):
        return memory.read_f32(RaceInfoPlayer.instance(playerIdx) + 0x14)
        
    @staticmethod
    def checkpoint_start_lap_completion(playerIdx=0):
        return memory.read_f32(RaceInfoPlayer.instance(playerIdx) + 0x18)
        
    @staticmethod
    def lap_completion(playerIdx=0):
        return memory.read_f32(RaceInfoPlayer.instance(playerIdx) + 0x1C)
        
    @staticmethod
    def position(playerIdx=0):
        return memory.read_u8(RaceInfoPlayer.instance(playerIdx) + 0x20)
        
    @staticmethod
    def respawn_point(playerIdx=0):
        return memory.read_u8(RaceInfoPlayer.instance(playerIdx) + 0x21)
    
    @staticmethod
    def battle_score(playerIdx=0):
        return memory.read_u16(RaceInfoPlayer.instance(playerIdx) + 0x22)
        
    @staticmethod
    def current_lap(playerIdx=0):
        return memory.read_u16(RaceInfoPlayer.instance(playerIdx) + 0x24)
    
    @staticmethod
    def max_lap(playerIdx=0):
        return memory.read_u8(RaceInfoPlayer.instance(playerIdx) + 0x26)
    
    @staticmethod
    def max_kcp(playerIdx=0):
        return memory.read_u8(RaceInfoPlayer.instance(playerIdx) + 0x27)
    
    @staticmethod
    def frame_counter(playerIdx=0):
        return memory.read_u32(RaceInfoPlayer.instance(playerIdx) + 0x2C)
        
    @staticmethod
    def frames_in_first_place(playerIdx=0):
        return memory.read_u32(RaceInfoPlayer.instance(playerIdx) + 0x30)
        
    @staticmethod
    def flags(playerIdx=0):
        return memory.read_u32(RaceInfoPlayer.instance(playerIdx) + 0x38)
        
    # TODO: Everything below here should be in a subclass probably
    @staticmethod
    def ablr_buttons(playerIdx=0):
        offsets = [0x4, 0x9]
        return chase_pointer(RaceInfoPlayer.instance(playerIdx) + 0x48, offsets, 'u8')
        
    @staticmethod
    def x_button(playerIdx=0):
        offsets = [0x38, 0x4, 0x14]
        return chase_pointer(RaceInfoPlayer.instance(playerIdx) + 0x48, offsets, 'u8')
        
    @staticmethod
    def y_button(playerIdx=0):
        offsets = [0x38, 0x4, 0x15]
        return chase_pointer(RaceInfoPlayer.instance(playerIdx) + 0x48, offsets, 'u8')
        
    @staticmethod
    def dpad(playerIdx=0):
        offsets = [0x4, 0x17]
        return chase_pointer(RaceInfoPlayer.instance(playerIdx) + 0x48, offsets, 'u8')
        
    @staticmethod
    def stick_x(playerIdx=0):
        return chase_pointer(RaceInfoPlayer.instance(playerIdx) + 0x48, [0x38], 'u8')
        
    @staticmethod
    def stick_y(playerIdx=0):
        return chase_pointer(RaceInfoPlayer.instance(playerIdx) + 0x48, [0x39], 'u8')
        
class RaceInfo:
    @staticmethod
    def intro_timer():
        return chase_pointer(getRaceInfoHolder(), [0x1E], 'u16')

    @staticmethod
    def timer():
        return chase_pointer(getRaceInfoHolder(), [0x20], 'u32')
        
    @staticmethod
    def stage():
        return chase_pointer(getRaceInfoHolder(), [0x28], 'u32')
        
    @staticmethod
    def spectator_mode():
        return chase_pointer(getRaceInfoHolder(), [0x2D], 'u8')
        
    @staticmethod
    def can_countdown_start():
        return chase_pointer(getRaceInfoHolder(), [0x2E], 'u8')
        
    @staticmethod
    def cutscene_mode():
        return chase_pointer(getRaceInfoHolder(), [0x2F], 'u8')

class InputMgr:
    @staticmethod
    def chain():
        address = {"RMCE01": 0x809b8f4c, "RMCP01": 0x809bd70c,
                   "RMCJ01": 0x809bc76c, "RMCK01": 0x809abd4c}
        return address[utils.get_game_id()]
        
    @staticmethod
    def drift_id(playerIdx=0):
        return chase_pointer(InputMgr.chain() + (playerIdx * 0x4), [0xC4], 'u16')
