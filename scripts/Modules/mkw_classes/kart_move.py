#TODO

from dolphin import memory
from enum import Enum

from . import KartSettings, KartObject, vec3, SpecialFloor

class KartMove:
    class JumpPadProperties:
        def __init__(self, player_idx=0, addr=None):
            self.addr = addr if addr else KartMove.JumpPadProperties.chain(player_idx)

            self.min_speed = self.inst_min_speed
            self.max_speed = self.inst_max_speed
            self.velocity_y = self.inst_velocity_y

        @staticmethod
        def chain(player_idx=0) -> int:
            return KartMove.jump_pad_properties(player_idx)
        
        @staticmethod
        def min_speed(player_idx=0) -> float:
            jump_pad_properties_ref = KartMove.JumpPadProperties.chain(player_idx)
            min_speed_ref = jump_pad_properties_ref + 0x0
            return memory.read_f32(min_speed_ref)
        
        def inst_min_speed(self) -> float:
            min_speed_ref = self.addr + 0x0
            return memory.read_f32(min_speed_ref)
        
        @staticmethod
        def max_speed(player_idx=0) -> float:
            jump_pad_properties_ref = KartMove.JumpPadProperties.chain(player_idx)
            max_speed_ref = jump_pad_properties_ref + 0x4
            return memory.read_f32(max_speed_ref)
        
        def inst_max_speed(self) -> float:
            max_speed_ref = self.addr + 0x4
            return memory.read_f32(max_speed_ref)
        
        @staticmethod
        def velocity_y(player_idx=0) -> float:
            jump_pad_properties_ref = KartMove.JumpPadProperties.chain(player_idx)
            velocity_y_ref = jump_pad_properties_ref + 0x8
            return memory.read_f32(velocity_y_ref)
        
        def inst_velocity_y(self) -> float:
            velocity_y_ref = self.addr + 0x8
            return memory.read_f32(velocity_y_ref)
    
    class DrivingDirection(Enum):
        FORWARDS = 0
        BRAKING = 1
        WAITING_FOR_BACKWARDS = 2
        BACKWARDS = 3

    def __init__(self, player_idx=0, addr=None):
        self.addr = addr if addr else KartMove.chain(player_idx)

        #Used to enforce the varying sizes of KartMove
        self.is_bike = KartSettings.is_bike(player_idx)

        self.speed_multiplier = self.inst_speed_multiplier
        self.base_speed = self.inst_base_speed
        self.soft_speed_limit = self.inst_soft_speed_limit
        self.speed = self.inst_speed
        self.last_speed = self.inst_last_speed
        self.hard_speed_limit = self.inst_hard_speed_limit
        self.acceleration = self.inst_acceleration
        self.speed_drag_multiplier = self.inst_speed_drag_multiplier
        self.smoothed_up = self.inst_smoothed_up
        self.up = self.inst_up
        self.landing_dir = self.inst_landing_dir
        self.dir = self.inst_dir
        self.last_dir = self.inst_last_dir
        self.vel1_dir = self.inst_vel1_dir
        self.dir_diff = self.inst_dir_diff
        self.has_landing_dir = self.inst_has_landing_dir
        self.outside_drift_angle = self.inst_outside_drift_angle
        self.landing_angle = self.inst_landing_angle
        self.outside_drift_last_dir = self.inst_outside_drift_last_dir
        self.speed_ratio_capped = self.inst_speed_ratio_capped
        self.speed_ratio = self.inst_speed_ratio
        self.kcl_speed_factor = self.inst_kcl_speed_factor
        self.kcl_rot_factor = self.inst_kcl_rot_factor
        self.kcl_wheel_speed_factor = self.inst_kcl_wheel_speed_factor
        self.kcl_wheel_rot_factor = self.inst_kcl_wheel_rot_factor
        self.floor_collision_count = self.inst_floor_collision_count
        self.hop_stick_x = self.inst_hop_stick_x
        self.hop_frame = self.inst_hop_frame
        self.hop_up = self.inst_hop_up
        self.hop_dir = self.inst_hop_dir
        self.slipstream_charge = self.inst_slipstream_charge
        self.diving_rotation = self.inst_diving_rotation
        self.standstil_boost_rotation = self.inst_standstil_boost_rotation
        self.mt_charge = self.inst_mt_charge
        self.smt_charge = self.inst_smt_charge
        self.mt_boost_timer = self.inst_mt_boost_timer
        self.outside_drift_bonus = self.inst_outside_drift_bonus
        self.kart_boost = self.inst_kart_boost
        self.zipper_boost = self.inst_zipper_boost
        self.zipper_boost_max = self.inst_zipper_boost_max
        self.offroad_invincibility = self.inst_offroad_invincibility
        self.ssmt_charge = self.inst_ssmt_charge
        self.real_turn = self.inst_real_turn
        self.weighted_turn = self.inst_weighted_turn
        self.scale = self.inst_scale
        self.shock_speed_modifier = self.inst_shock_speed_modifier
        self.mega_scale = self.inst_mega_scale
        self.mushroom_timer = self.inst_mushroom_timer
        self.star_timer = self.inst_star_timer
        self.shock_timer = self.inst_shock_timer
        self.ink_timer = self.inst_ink_timer
        self.ink_applied = self.inst_ink_applied
        self.crush_timer = self.inst_crush_timer
        self.mega_timer = self.inst_mega_timer
        self.blink_timer = self.inst_blink_timer
        self.jump_pad_min_speed = self.inst_jump_pad_min_speed
        self.jump_pad_max_speed = self.inst_jump_pad_max_speed
        self.jump_pad_properties = self.inst_jump_pad_properties
        self.ramp_boost = self.inst_ramp_boost
        self.auto_drift_angle = self.inst_auto_drift_angle
        self.auto_drift_start_frame_counter = self.inst_auto_drift_start_frame_counter
        self.last_position = self.inst_last_position
        self.airtime = self.inst_airtime
        self.before_battle_respawn_frames = self.inst_before_battle_respawn_frames
        self.hop_velocity_y = self.inst_hop_velocity_y
        self.hop_position_y = self.inst_hop_position_y
        self.hop_gravity = self.inst_hop_gravity
        self.time_in_respawn = self.inst_time_in_respawn
        self.respawn_timer = self.inst_respawn_timer
        self.wheelie_bump_timer = self.inst_wheelie_bump_timer
        self.driving_direction = self.inst_driving_direction
        self.backwards_allow_counter = self.inst_backwards_allow_counter
        self.special_floor = self.inst_special_floor
        self.kart_jump = self.inst_kart_jump
        self.kart_half_pipe = self.inst_kart_half_pipe
        self.kart_scale = self.inst_kart_scale
        self.raw_turn = self.inst_raw_turn
        self.ghost_stop_timer = self.inst_ghost_stop_timer
        self.lean_rot = self.inst_lean_rot
        self.lean_rot_cap = self.inst_lean_rot_cap
        self.lean_rot_increase = self.inst_lean_rot_increase
        self.wheelie_rotation = self.inst_wheelie_rotation
        self.max_wheelie_rotation = self.inst_max_wheelie_rotation
        self.wheelie_frames = self.inst_wheelie_frames
        self.wheelie_cooldown = self.inst_wheelie_cooldown
        self.wheelie_rotation_decrease = self.inst_wheelie_rotation_decrease
    
    @staticmethod
    def chain(player_idx=0) -> int:
        return KartObject.kart_move(player_idx)

    @staticmethod
    def speed_multiplier(player_idx=0) -> float:
        kart_move_ref = KartMove.chain(player_idx)
        speed_multiplier_ref = kart_move_ref + 0x10
        return memory.read_f32(speed_multiplier_ref)

    def inst_speed_multiplier(self) -> float:
        speed_multiplier_ref = self.addr + 0x10
        return memory.read_f32(speed_multiplier_ref)

    @staticmethod
    def base_speed(player_idx=0) -> float:
        kart_move_ref = KartMove.chain(player_idx)
        position_ref = kart_move_ref + 0x14
        return memory.read_f32(position_ref)

    def inst_base_speed(self) -> float:
        position_ref = self.addr + 0x14
        return memory.read_f32(position_ref)

    @staticmethod
    def soft_speed_limit(player_idx=0) -> float:
        kart_move_ref = KartMove.chain(player_idx)
        soft_speed_limit_ref = kart_move_ref + 0x18
        return memory.read_f32(soft_speed_limit_ref)

    def inst_soft_speed_limit(self) -> float:
        soft_speed_limit_ref = self.addr + 0x18
        return memory.read_f32(soft_speed_limit_ref)

    @staticmethod
    def speed(player_idx=0) -> float:
        kart_move_ref = KartMove.chain(player_idx)
        speed_ref = kart_move_ref + 0x20
        return memory.read_f32(speed_ref)

    def inst_speed(self) -> float:
        speed_ref = self.addr + 0x20
        return memory.read_f32(speed_ref)

    @staticmethod
    def last_speed(player_idx=0) -> float:
        kart_move_ref = KartMove.chain(player_idx)
        last_speed_ref = kart_move_ref + 0x24
        return memory.read_f32(last_speed_ref)

    def inst_last_speed(self) -> float:
        last_speed_ref = self.addr + 0x24
        return memory.read_f32(last_speed_ref)

    @staticmethod
    def hard_speed_limit(player_idx=0) -> float:
        kart_move_ref = KartMove.chain(player_idx)
        hard_speed_limit_ref = kart_move_ref + 0x2C
        return memory.read_f32(hard_speed_limit_ref)

    def inst_hard_speed_limit(self) -> float:
        hard_speed_limit_ref = self.addr + 0x2C
        return memory.read_f32(hard_speed_limit_ref)

    @staticmethod
    def acceleration(player_idx=0) -> float:
        kart_move_ref = KartMove.chain(player_idx)
        acceleration_ref = kart_move_ref + 0x30
        return memory.read_f32(acceleration_ref)

    def inst_acceleration(self) -> float:
        acceleration_ref = self.addr + 0x30
        return memory.read_f32(acceleration_ref)

    @staticmethod
    def speed_drag_multiplier(player_idx=0) -> float:
        kart_move_ref = KartMove.chain(player_idx)
        speed_drag_multiplier_ref = kart_move_ref + 0x34
        return memory.read_f32(speed_drag_multiplier_ref)

    def inst_speed_drag_multiplier(self) -> float:
        speed_drag_multiplier_ref = self.addr + 0x34
        return memory.read_f32(speed_drag_multiplier_ref)

    @staticmethod
    def smoothed_up(player_idx=0) -> vec3:
        """Smoothed version of up()"""
        kart_move_ref = KartMove.chain(player_idx)
        smoothed_up_ref = kart_move_ref + 0x38
        return vec3.read(smoothed_up_ref)

    def inst_smoothed_up(self) -> vec3:
        """Smoothed version of up()"""
        smoothed_up_ref = self.addr + 0x38
        return vec3.read(smoothed_up_ref)

    @staticmethod
    def up(player_idx=0) -> vec3:
        """Vector perpendicular to the floor, pointing upwards"""
        kart_move_ref = KartMove.chain(player_idx)
        up_ref = kart_move_ref + 0x44
        return vec3.read(up_ref)

    def inst_up(self) -> vec3:
        """Vector perpendicular to the floor, pointing upwards"""
        up_ref = self.addr + 0x44
        return vec3.read(up_ref)

    @staticmethod
    def landing_dir(player_idx=0) -> vec3:
        kart_move_ref = KartMove.chain(player_idx)
        landing_dir_ref = kart_move_ref + 0x50
        return vec3.read(landing_dir_ref)

    def inst_landing_dir(self) -> vec3:
        landing_dir_ref = self.addr + 0x50
        return vec3.read(landing_dir_ref)

    @staticmethod
    def dir(player_idx=0) -> vec3:
        kart_move_ref = KartMove.chain(player_idx)
        dir_ref = kart_move_ref + 0x5C
        return vec3.read(dir_ref)

    def inst_dir(self) -> vec3:
        dir_ref = self.addr + 0x5C
        return vec3.read(dir_ref)

    @staticmethod
    def last_dir(player_idx=0) -> vec3:
        kart_move_ref = KartMove.chain(player_idx)
        last_dir_ref = kart_move_ref + 0x68
        return vec3.read(last_dir_ref)

    def inst_last_dir(self) -> vec3:
        last_dir_ref = self.addr + 0x68
        return vec3.read(last_dir_ref)

    @staticmethod
    def vel1_dir(player_idx=0) -> vec3:
        kart_move_ref = KartMove.chain(player_idx)
        vel1_dir_ref = kart_move_ref + 0x74
        return vec3.read(vel1_dir_ref)

    def inst_vel1_dir(self) -> vec3:
        vel1_dir_ref = self.addr + 0x74
        return vec3.read(vel1_dir_ref)

    @staticmethod
    def dir_diff(player_idx=0) -> vec3:
        kart_move_ref = KartMove.chain(player_idx)
        dir_diff_ref = kart_move_ref + 0x8C
        return vec3.read(dir_diff_ref)

    def inst_dir_diff(self) -> vec3:
        dir_diff_ref = self.addr + 0x8C
        return vec3.read(dir_diff_ref)

    @staticmethod
    def has_landing_dir(player_idx=0) -> int:
        kart_move_ref = KartMove.chain(player_idx)
        has_landing_dir_ref = kart_move_ref + 0x98
        return memory.read_u8(has_landing_dir_ref)

    def inst_has_landing_dir(self) -> int:
        has_landing_dir_ref = self.addr + 0x98
        return memory.read_u8(has_landing_dir_ref)

    @staticmethod
    def outside_drift_angle(player_idx=0) -> float:
        kart_move_ref = KartMove.chain(player_idx)
        outside_drift_angle_ref = kart_move_ref + 0x9C
        return memory.read_f32(outside_drift_angle_ref)

    def inst_outside_drift_angle(self) -> float:
        outside_drift_angle_ref = self.addr + 0x9C
        return memory.read_f32(outside_drift_angle_ref)

    @staticmethod
    def landing_angle(player_idx=0) -> float:
        kart_move_ref = KartMove.chain(player_idx)
        landing_angle_ref = kart_move_ref + 0xA0
        return memory.read_f32(landing_angle_ref)

    def inst_landing_angle(self) -> float:
        landing_angle_ref = self.addr + 0xA0
        return memory.read_f32(landing_angle_ref)

    @staticmethod
    def outside_drift_last_dir(player_idx=0) -> vec3:
        kart_move_ref = KartMove.chain(player_idx)
        outside_drift_last_dir_ref = kart_move_ref + 0xA4
        return vec3.read(outside_drift_last_dir_ref)

    def inst_outside_drift_last_dir(self) -> vec3:
        outside_drift_last_dir_ref = self.addr + 0xA4
        return vec3.read(outside_drift_last_dir_ref)

    @staticmethod
    def speed_ratio_capped(player_idx=0) -> float:
        kart_move_ref = KartMove.chain(player_idx)
        speed_ratio_capped_ref = kart_move_ref + 0xB0
        return memory.read_f32(speed_ratio_capped_ref)

    def inst_speed_ratio_capped(self) -> float:
        speed_ratio_capped_ref = self.addr + 0xB0
        return memory.read_f32(speed_ratio_capped_ref)

    @staticmethod
    def speed_ratio(player_idx=0) -> float:
        kart_move_ref = KartMove.chain(player_idx)
        speed_ratio_ref = kart_move_ref + 0xB4
        return memory.read_f32(speed_ratio_ref)

    def inst_speed_ratio(self) -> float:
        speed_ratio_ref = self.addr + 0xB4
        return memory.read_f32(speed_ratio_ref)

    @staticmethod
    def kcl_speed_factor(player_idx=0) -> float:
        kart_move_ref = KartMove.chain(player_idx)
        kcl_speed_factor_ref = kart_move_ref + 0xB8
        return memory.read_f32(kcl_speed_factor_ref)

    def inst_kcl_speed_factor(self) -> float:
        kcl_speed_factor_ref = self.addr + 0xB8
        return memory.read_f32(kcl_speed_factor_ref)

    @staticmethod
    def kcl_rot_factor(player_idx=0) -> float:
        kart_move_ref = KartMove.chain(player_idx)
        kcl_rot_factor_ref = kart_move_ref + 0xBC
        return memory.read_f32(kcl_rot_factor_ref)

    def inst_kcl_rot_factor(self) -> float:
        kcl_rot_factor_ref = self.addr + 0xBC
        return memory.read_f32(kcl_rot_factor_ref)
    
    @staticmethod
    def kcl_wheel_speed_factor(player_idx=0) -> float:
        kart_move_ref = KartMove.chain(player_idx)
        kcl_wheel_speed_factor_ref = kart_move_ref + 0xC0
        return memory.read_f32(kcl_wheel_speed_factor_ref)
    
    def inst_kcl_wheel_speed_factor(self) -> float:
        kcl_wheel_speed_factor_ref = self.addr + 0xC0
        return memory.read_f32(kcl_wheel_speed_factor_ref)
    
    @staticmethod
    def kcl_wheel_rot_factor(player_idx=0) -> float:
        kart_move_ref = KartMove.chain(player_idx)
        kcl_wheel_rot_factor_ref = kart_move_ref + 0xC4
        return memory.read_f32(kcl_wheel_rot_factor_ref)
    
    def inst_kcl_wheel_rot_factor(self) -> float:
        kcl_wheel_rot_factor_ref = self.addr + 0xC4
        return memory.read_f32(kcl_wheel_rot_factor_ref)
    
    @staticmethod
    def floor_collision_count(player_idx=0) -> float:
        kart_move_ref = KartMove.chain(player_idx)
        floor_collision_count_ref = kart_move_ref + 0xC8
        return memory.read_f32(floor_collision_count_ref)

    def inst_floor_collision_count(self) -> int:
        floor_collision_count_ref = self.addr + 0xC8
        return memory.read_u16(floor_collision_count_ref)
    
    @staticmethod
    def hop_stick_x(player_idx=0) -> int:
        kart_move_ref = KartMove.chain(player_idx)
        hop_stick_x_ref = kart_move_ref + 0xCC
        return memory.read_s32(hop_stick_x_ref)
    
    def inst_hop_stick_x(self) -> int:
        hop_stick_x_ref = self.addr + 0xCC
        return memory.read_s32(hop_stick_x_ref)
    
    @staticmethod
    def hop_frame(player_idx=0) -> int:
        kart_move_ref = KartMove.chain(player_idx)
        hop_frame_ref = kart_move_ref + 0xD0
        return memory.read_s32(hop_frame_ref)
    
    def inst_hop_frame(self) -> int:
        hop_frame_ref = self.addr + 0xD0
        return memory.read_s32(hop_frame_ref)
    
    @staticmethod
    def hop_up(player_idx=0) -> vec3:
        kart_move_ref = KartMove.chain(player_idx)
        hop_up_ref = kart_move_ref + 0xD4
        return vec3.read(hop_up_ref)
    
    def inst_hop_up(self) -> vec3:
        hop_up_ref = self.addr + 0xD4
        return vec3.read(hop_up_ref)
    
    @staticmethod
    def hop_dir(player_idx=0) -> vec3:
        kart_move_ref = KartMove.chain(player_idx)
        hop_dir_ref = kart_move_ref + 0xE0
        return vec3.read(hop_dir_ref)

    def inst_hop_dir(self) -> vec3:
        hop_dir_ref = self.addr + 0xE0
        return vec3.read(hop_dir_ref)
    
    @staticmethod
    def slipstream_charge(player_idx=0) -> int:
        kart_move_ref = KartMove.chain(player_idx)
        slipstream_charge_ref = kart_move_ref + 0xEC
        return memory.read_u32(slipstream_charge_ref)
    
    def inst_slipstream_charge(self) -> int:
        slipstream_charge_ref = self.addr + 0xEC
        return memory.read_u32(slipstream_charge_ref)
    
    @staticmethod
    def diving_rotation(player_idx=0) -> float:
        kart_move_ref = KartMove.chain(player_idx)
        diving_rotation_ref = kart_move_ref + 0xF4
        return memory.read_f32(diving_rotation_ref)
    
    def inst_diving_rotation(self) -> float:
        diving_rotation_ref = self.addr + 0xF4
        return memory.read_f32(diving_rotation_ref)
    
    @staticmethod
    def standstil_boost_rotation(player_idx=0) -> float:
        kart_move_ref = KartMove.chain(player_idx)
        standstil_boost_rotation_ref = kart_move_ref + 0xF8
        return memory.read_f32(standstil_boost_rotation_ref)
    
    def inst_standstil_boost_rotation(self) -> float:
        standstil_boost_rotation_ref = self.addr + 0xF8
        return memory.read_f32(standstil_boost_rotation_ref)
    
    @staticmethod
    def drift_state(player_idx=0) -> int:
        """1: Charging MT
           2: MT Charged"""
        kart_move_ref = KartMove.chain(player_idx)
        drift_state_ref = kart_move_ref + 0xFC
        return memory.read_u16(drift_state_ref)
    
    def inst_drift_state(self) -> int:
        """1: Charging MT
           2: MT Charged"""
        drift_state_ref = self.addr + 0xFC
        return memory.read_u16(drift_state_ref)
    
    @staticmethod
    def mt_charge(player_idx=0) -> int:
        kart_move_ref = KartMove.chain(player_idx)
        mt_charge_ref = kart_move_ref + 0xFE
        return memory.read_u16(mt_charge_ref)
    
    def inst_mt_charge(self) -> int:
        mt_charge_ref = self.addr + 0xFE
        return memory.read_u16(mt_charge_ref)
    
    @staticmethod
    def smt_charge(player_idx=0) -> int:
        kart_move_ref = KartMove.chain(player_idx)
        smt_charge_ref = kart_move_ref + 0x100
        return memory.read_u16(smt_charge_ref)
    
    def inst_smt_charge(self) -> int:
        smt_charge_ref = self.addr + 0x100
        return memory.read_u16(smt_charge_ref)
    
    @staticmethod
    def mt_boost_timer(player_idx=0) -> int:
        kart_move_ref = KartMove.chain(player_idx)
        mt_boost_timer_ref = kart_move_ref + 0x102
        return memory.read_u16(mt_boost_timer_ref)
    
    def inst_mt_boost_timer(self) -> int:
        mt_boost_timer_ref = self.addr + 0x102
        return memory.read_u16(mt_boost_timer_ref)
    
    @staticmethod
    def outside_drift_bonus(player_idx=0) -> float:
        kart_move_ref = KartMove.chain(player_idx)
        outside_drift_bonus_ref = kart_move_ref + 0x104
        return memory.read_f32(outside_drift_bonus_ref)
    
    def inst_outside_drift_bonus(self) -> float:
        outside_drift_bonus_ref = self.addr + 0x104
        return memory.read_f32(outside_drift_bonus_ref)
    
    @staticmethod
    def kart_boost(player_idx=0) -> int:
        kart_move_ref = KartMove.chain(player_idx)
        boost_ref = kart_move_ref + 0x108
        return boost_ref
    
    def inst_kart_boost(self) -> int:
        boost_ref = self.addr + 0x108
        return boost_ref
    
    @staticmethod
    def zipper_boost(player_idx=0) -> int:
        kart_move_ref = KartMove.chain(player_idx)
        zipper_boost_ref = kart_move_ref + 0x12C
        return memory.read_u16(zipper_boost_ref)
    
    def inst_zipper_boost(self) -> int:
        zipper_boost_ref = self.addr + 0x12C
        return memory.read_u16(zipper_boost_ref)
    
    @staticmethod
    def zipper_boost_max(player_idx=0) -> int:
        kart_move_ref = KartMove.chain(player_idx)
        inst_zipper_boost_max_ref = kart_move_ref + 0x12C
        return memory.read_u16(inst_zipper_boost_max_ref)
    
    def inst_zipper_boost_max(self) -> int:
        inst_zipper_boost_max_ref = self.addr + 0x12C
        return memory.read_u16(inst_zipper_boost_max_ref)
    
    @staticmethod
    def offroad_invincibility(player_idx=0) -> int:
        kart_move_ref = KartMove.chain(player_idx)
        offroad_invincibility_ref = kart_move_ref + 0x148
        return memory.read_u16(offroad_invincibility_ref)
    
    def inst_offroad_invincibility(self) -> int:
        offroad_invincibility_ref = self.addr + 0x148
        return memory.read_u16(offroad_invincibility_ref)
    
    @staticmethod
    def ssmt_charge(player_idx=0) -> int:
        kart_move_ref = KartMove.chain(player_idx)
        ssmt_charge_ref = kart_move_ref + 0x14C
        return memory.read_u16(ssmt_charge_ref)
    
    def inst_ssmt_charge(self) -> int:
        ssmt_charge_ref = self.addr + 0x14C
        return memory.read_u16(ssmt_charge_ref)
    
    # 0x152 pertains to something POW-related

    @staticmethod
    def real_turn(player_idx=0) -> float:
        kart_move_ref = KartMove.chain(player_idx)
        real_turn_ref = kart_move_ref + 0x158
        return memory.read_f32(real_turn_ref)
    
    def inst_real_turn(self) -> float:
        real_turn_ref = self.addr + 0x158
        return memory.read_f32(real_turn_ref)
    
    @staticmethod
    def weighted_turn(player_idx=0) -> float:
        kart_move_ref = KartMove.chain(player_idx)
        real_turn_ref = kart_move_ref + 0x15C
        return memory.read_f32(real_turn_ref)
    
    def inst_weighted_turn(self) -> float:
        real_turn_ref = self.addr + 0x15C
        return memory.read_f32(real_turn_ref)
    
    @staticmethod
    def scale(player_idx=0) -> vec3:
        kart_move_ref = KartMove.chain(player_idx)
        scale_ref = kart_move_ref + 0x164
        return vec3.read(scale_ref)
    
    def inst_scale(self) -> vec3:
        scale_ref = self.addr + 0x164
        return vec3.read(scale_ref)
    
    @staticmethod
    def shock_speed_modifier(player_idx=0) -> float:
        kart_move_ref = KartMove.chain(player_idx)
        shock_speed_modifier_ref = kart_move_ref + 0x178
        return memory.read_f32(shock_speed_modifier_ref)
    
    def inst_shock_speed_modifier(self) -> float:
        shock_speed_modifier_ref = self.addr + 0x178
        return memory.read_f32(shock_speed_modifier_ref)
    
    @staticmethod
    def mega_scale(player_idx=0) -> float:
        kart_move_ref = KartMove.chain(player_idx)
        mega_scale_ref = kart_move_ref + 0x17C
        return memory.read_f32(mega_scale_ref)
    
    def inst_mega_scale(self) -> float:
        mega_scale_ref = self.addr + 0x17C
        return memory.read_f32(mega_scale_ref)
    
    @staticmethod
    def mushroom_timer(player_idx=0) -> int:
        kart_move_ref = KartMove.chain(player_idx)
        mushroom_timer_ref = kart_move_ref + 0x188
        return memory.read_u16(mushroom_timer_ref)
    
    def inst_mushroom_timer(self) -> int:
        mushroom_timer_ref = self.addr + 0x188
        return memory.read_u16(mushroom_timer_ref)
    
    @staticmethod
    def star_timer(player_idx=0) -> int:
        kart_move_ref = KartMove.chain(player_idx)
        star_timer_ref = kart_move_ref + 0x18A
        return memory.read_u16(star_timer_ref)
    
    def inst_star_timer(self) -> int:
        star_timer_ref = self.addr + 0x18A
        return memory.read_u16(star_timer_ref)
    
    @staticmethod
    def shock_timer(player_idx=0) -> int:
        kart_move_ref = KartMove.chain(player_idx)
        shock_timer_ref = kart_move_ref + 0x18C
        return memory.read_u16(shock_timer_ref)
    
    def inst_shock_timer(self) -> int:
        shock_timer_ref = self.addr + 0x18C
        return memory.read_u16(shock_timer_ref)
    
    @staticmethod
    def ink_timer(player_idx=0) -> int:
        kart_move_ref = KartMove.chain(player_idx)
        ink_timer_ref = kart_move_ref + 0x18E
        return memory.read_u16(ink_timer_ref)
    
    def inst_ink_timer(self) -> int:
        ink_timer_ref = self.addr + 0x18E
        return memory.read_u16(ink_timer_ref)
    
    @staticmethod
    def ink_applied(player_idx=0) -> bool:
        kart_move_ref = KartMove.chain(player_idx)
        ink_applied_ref = kart_move_ref + 0x190
        return memory.read_u8(ink_applied_ref) > 0
    
    def inst_ink_applied(self) -> bool:
        ink_applied_ref = self.addr + 0x190
        return memory.read_u8(ink_applied_ref) > 0
    
    @staticmethod
    def crush_timer(player_idx=0) -> int:
        kart_move_ref = KartMove.chain(player_idx)
        crush_timer_ref = kart_move_ref + 0x192
        return memory.read_u16(crush_timer_ref)
    
    def inst_crush_timer(self) -> int:
        crush_timer_ref = self.addr + 0x192
        return memory.read_u16(crush_timer_ref)
    
    @staticmethod
    def mega_timer(player_idx=0) -> int:
        kart_move_ref = KartMove.chain(player_idx)
        mega_timer_ref = kart_move_ref + 0x194
        return memory.read_u16(mega_timer_ref)
    
    def inst_mega_timer(self) -> int:
        mega_timer_ref = self.addr + 0x194
        return memory.read_u16(mega_timer_ref)
    
    @staticmethod
    def blink_timer(player_idx=0) -> int:
        kart_move_ref = KartMove.chain(player_idx)
        blink_timer_ref = kart_move_ref + 0x1A8
        return memory.read_u16(blink_timer_ref)
    
    def inst_blink_timer(self) -> int:
        blink_timer_ref = self.addr + 0x1A8
        return memory.read_u16(blink_timer_ref)
    
    @staticmethod
    def jump_pad_min_speed(player_idx=0) -> float:
        kart_move_ref = KartMove.chain(player_idx)
        jump_pad_min_speed_ref = kart_move_ref + 0x1B0
        return memory.read_f32(jump_pad_min_speed_ref)
    
    def inst_jump_pad_min_speed(self) -> float:
        jump_pad_min_speed_ref = self.addr + 0x1B0
        return memory.read_f32(jump_pad_min_speed_ref)
    
    @staticmethod
    def jump_pad_max_speed(player_idx=0) -> float:
        kart_move_ref = KartMove.chain(player_idx)
        jump_pad_max_speed_ref = kart_move_ref + 0x1B4
        return memory.read_f32(jump_pad_max_speed_ref)
    
    def inst_jump_pad_max_speed(self) -> float:
        jump_pad_max_speed_ref = self.addr + 0x1B4
        return memory.read_f32(jump_pad_max_speed_ref)
    
    @staticmethod
    def jump_pad_properties(player_idx=0) -> int:
        kart_move_ref = KartMove.chain(player_idx)
        jump_pad_properties_ref = kart_move_ref + 0x1C0
        return memory.read_u32(jump_pad_properties_ref)
    
    def inst_jump_pad_properties(self) -> int:
        jump_pad_properties_ref = self.addr + 0x1C0
        return memory.read_u32(jump_pad_properties_ref)
    
    @staticmethod
    def ramp_boost(player_idx=0) -> int:
        kart_move_ref = KartMove.chain(player_idx)
        ramp_boost_ref = kart_move_ref + 0x1C4
        return memory.read_u16(ramp_boost_ref)
    
    def inst_ramp_boost(self) -> int:
        ramp_boost_ref = self.addr + 0x1C4
        return memory.read_u16(ramp_boost_ref)
    
    @staticmethod
    def auto_drift_angle(player_idx=0) -> float:
        kart_move_ref = KartMove.chain(player_idx)
        auto_drift_angle_ref = kart_move_ref + 0x1C8
        return memory.read_f32(auto_drift_angle_ref)
    
    def inst_auto_drift_angle(self) -> float:
        auto_drift_angle_ref = self.addr + 0x1C8
        return memory.read_f32(auto_drift_angle_ref)
    
    @staticmethod
    def auto_drift_start_frame_counter(player_idx=0) -> int:
        kart_move_ref = KartMove.chain(player_idx)
        auto_drift_start_frame_counter_ref = kart_move_ref + 0x1CC
        return memory.read_u16(auto_drift_start_frame_counter_ref)
    
    def inst_auto_drift_start_frame_counter(self) -> int:
        auto_drift_start_frame_counter_ref = self.addr + 0x1CC
        return memory.read_u16(auto_drift_start_frame_counter_ref)
    
    @staticmethod
    def last_position(player_idx=0) -> vec3:
        kart_move_ref = KartMove.chain(player_idx)
        last_position_ref = kart_move_ref + 0x1E8
        return vec3.read(last_position_ref)
    
    def inst_last_position(self) -> vec3:
        last_position_ref = self.addr + 0x1E8
        return vec3.read(last_position_ref)
    
    @staticmethod
    def airtime(player_idx=0) -> int:
        kart_move_ref = KartMove.chain(player_idx)
        airtime_ref = kart_move_ref + 0x218
        return memory.read_u32(airtime_ref)
    
    def inst_airtime(self) -> int:
        airtime_ref = self.addr + 0x218
        return memory.read_u32(airtime_ref)
    
    @staticmethod
    def before_battle_respawn_frames(player_idx=0) -> int:
        kart_move_ref = KartMove.chain(player_idx)
        before_battle_respawn_frames_ref = kart_move_ref + 0x21C
        return memory.read_u16(before_battle_respawn_frames_ref)
    
    def inst_before_battle_respawn_frames(self) -> int:
        before_battle_respawn_frames_ref = self.addr + 0x21C
        return memory.read_u16(before_battle_respawn_frames_ref)
    
    @staticmethod
    def hop_velocity_y(player_idx=0) -> float:
        kart_move_ref = KartMove.chain(player_idx)
        hop_velocity_y_ref = kart_move_ref + 0x228
        return memory.read_f32(hop_velocity_y_ref)
    
    def inst_hop_velocity_y(self) -> float:
        hop_velocity_y_ref = self.addr + 0x228
        return memory.read_f32(hop_velocity_y_ref)
    
    @staticmethod
    def hop_position_y(player_idx=0) -> float:
        kart_move_ref = KartMove.chain(player_idx)
        hop_position_y_ref = kart_move_ref + 0x22C
        return memory.read_f32(hop_position_y_ref)
    
    def inst_hop_position_y(self) -> float:
        hop_position_y_ref = self.addr + 0x22C
        return memory.read_f32(hop_position_y_ref)
    
    @staticmethod
    def hop_gravity(player_idx=0) -> float:
        kart_move_ref = KartMove.chain(player_idx)
        hop_gravity_ref = kart_move_ref + 0x230
        return memory.read_f32(hop_gravity_ref)
    
    def inst_hop_gravity(self) -> float:
        hop_gravity_ref = self.addr + 0x230
        return memory.read_f32(hop_gravity_ref)
    
    @staticmethod
    def time_in_respawn(player_idx=0) -> int:
        kart_move_ref = KartMove.chain(player_idx)
        time_in_respawn_ref = kart_move_ref + 0x234
        return memory.read_u16(time_in_respawn_ref)
    
    def inst_time_in_respawn(self) -> int:
        time_in_respawn_ref = self.addr + 0x234
        return memory.read_u16(time_in_respawn_ref)
    
    @staticmethod
    def respawn_timer(player_idx=0) -> int:
        kart_move_ref = KartMove.chain(player_idx)
        respawn_timer_ref = kart_move_ref + 0x23A
        return memory.read_u16(respawn_timer_ref)
    
    def inst_respawn_timer(self) -> int:
        respawn_timer_ref = self.addr + 0x23A
        return memory.read_u16(respawn_timer_ref)
    
    @staticmethod
    def wheelie_bump_timer(player_idx=0) -> int:
        kart_move_ref = KartMove.chain(player_idx)
        wheelie_bump_timer_ref = kart_move_ref + 0x23C
        return memory.read_u16(wheelie_bump_timer_ref)
    
    def inst_wheelie_bump_timer(self) -> int:
        wheelie_bump_timer_ref = self.addr + 0x23C
        return memory.read_u16(wheelie_bump_timer_ref)
    
    @staticmethod
    def driving_direction(player_idx=0) -> DrivingDirection:
        kart_move_ref = KartMove.chain(player_idx)
        driving_direction_ref = kart_move_ref + 0x23C
        return KartMove.DrivingDirection(memory.read_u32(driving_direction_ref))
    
    def inst_driving_direction(self) -> DrivingDirection:
        driving_direction_ref = self.addr + 0x23C
        return KartMove.DrivingDirection(memory.read_u32(driving_direction_ref))

    @staticmethod
    def backwards_allow_counter(player_idx=0) -> int:
        kart_move_ref = KartMove.chain(player_idx)
        backwards_allow_counter_ref = kart_move_ref + 0x24C
        return memory.read_u16(backwards_allow_counter_ref)
    
    def inst_backwards_allow_counter(self) -> int:
        backwards_allow_counter_ref = self.addr + 0x24C
        return memory.read_u16(backwards_allow_counter_ref)
    
    @staticmethod
    def special_floor(player_idx=0) -> SpecialFloor:
        kart_move_ref = KartMove.chain(player_idx)
        special_floor_ref = kart_move_ref + 0x250
        return SpecialFloor(memory.read_u32(special_floor_ref))
    
    def inst_special_floor(self) -> SpecialFloor:
        special_floor_ref = self.addr + 0x250
        return SpecialFloor(memory.read_u32(special_floor_ref))
    
    @staticmethod
    def kart_jump(player_idx=0) -> int:
        kart_move_ref = KartMove.chain(player_idx)
        kart_jump_ptr = kart_move_ref + 0x258
        return memory.read_u32(kart_jump_ptr)
    
    def inst_kart_jump(self) -> int:
        kart_jump_ptr = self.addr + 0x258
        return memory.read_u32(kart_jump_ptr)
    
    @staticmethod
    def kart_half_pipe(player_idx=0) -> int:
        kart_move_ref = KartMove.chain(player_idx)
        kart_half_pipe_ptr = kart_move_ref + 0x25C
        return memory.read_u32(kart_half_pipe_ptr)
    
    def inst_kart_half_pipe(self) -> int:
        kart_half_pipe_ptr = self.addr + 0x25C
        return memory.read_u32(kart_half_pipe_ptr)

    @staticmethod
    def kart_scale(player_idx=0) -> int:
        kart_move_ref = KartMove.chain(player_idx)
        kart_scale_ptr = kart_move_ref + 0x260
        return memory.read_u32(kart_scale_ptr)
    
    def inst_kart_scale(self) -> int:
        kart_scale_ptr = self.addr + 0x260
        return memory.read_u32(kart_scale_ptr)

    @staticmethod
    def raw_turn(player_idx=0) -> float:
        kart_move_ref = KartMove.chain(player_idx)
        raw_turn_ref = kart_move_ref + 0x288
        return memory.read_f32(raw_turn_ref)
    
    def inst_raw_turn(self) -> float:
        raw_turn_ref = self.addr + 0x288
        return memory.read_f32(raw_turn_ref)
    
    @staticmethod
    def ghost_stop_timer(player_idx=0) -> int:
        kart_move_ref = KartMove.chain(player_idx)
        ghost_stop_timer_ref = kart_move_ref + 0x290
        return memory.read_u16(ghost_stop_timer_ref)
    
    def inst_ghost_stop_timer(self) -> int:
        ghost_stop_timer_ref = self.addr + 0x290
        return memory.read_u16(ghost_stop_timer_ref)
    
    # The below addresses are only available for bikes.
    # In KartSub::createComponents, KartMove size depends on vehicle type.
    # It's 0x294 for karts, and 0x2C4 for bikes. Enforce this!

    @staticmethod
    def lean_rot(player_idx=0) -> float:
        assert(KartSettings.is_bike(player_idx))
        kart_move_ref = KartMove.chain(player_idx)
        lean_rot_ref = kart_move_ref + 0x294
        return memory.read_f32(lean_rot_ref)
    
    def inst_lean_rot(self) -> float:
        assert(self.is_bike)
        lean_rot_ref = self.addr + 0x294
        return memory.read_f32(lean_rot_ref)
    
    @staticmethod
    def lean_rot_cap(player_idx=0) -> float:
        assert(KartSettings.is_bike(player_idx))
        kart_move_ref = KartMove.chain(player_idx)
        lean_rot_cap_ref = kart_move_ref + 0x298
        return memory.read_f32(lean_rot_cap_ref)
    
    def inst_lean_rot_cap(self) -> float:
        assert(self.is_bike)
        lean_rot_cap_ref = self.addr + 0x298
        return memory.read_f32(lean_rot_cap_ref)
    
    @staticmethod
    def lean_rot_increase(player_idx=0) -> float:
        assert(KartSettings.is_bike(player_idx))
        kart_move_ref = KartMove.chain(player_idx)
        lean_rot_increase_ref = kart_move_ref + 0x29C
        return memory.read_f32(lean_rot_increase_ref)
    
    def inst_lean_rot_increase(self) -> float:
        assert(self.is_bike)
        lean_rot_increase_ref = self.addr + 0x29C
        return memory.read_f32(lean_rot_increase_ref)
    
    @staticmethod
    def wheelie_rotation(player_idx=0) -> float:
        assert(KartSettings.is_bike(player_idx))
        kart_move_ref = KartMove.chain(player_idx)
        wheelie_rotation_ref = kart_move_ref + 0x2A0
        return memory.read_f32(wheelie_rotation_ref)
    
    def inst_wheelie_rotation(self) -> float:
        assert(self.is_bike)
        wheelie_rotation_ref = self.addr + 0x2A0
        return memory.read_f32(wheelie_rotation_ref)
    
    @staticmethod
    def max_wheelie_rotation(player_idx=0) -> float:
        assert(KartSettings.is_bike(player_idx))
        kart_move_ref = KartMove.chain(player_idx)
        max_wheelie_rotation_ref = kart_move_ref + 0x2A4
        return memory.read_f32(max_wheelie_rotation_ref)
    
    def inst_max_wheelie_rotation(self) -> float:
        assert(self.is_bike)
        max_wheelie_rotation_ref = self.addr + 0x2A4
        return memory.read_f32(max_wheelie_rotation_ref)
    
    @staticmethod
    def wheelie_frames(player_idx=0) -> int:
        assert(KartSettings.is_bike(player_idx))
        kart_move_ref = KartMove.chain(player_idx)
        wheelie_frames_ref = kart_move_ref + 0x2A8
        return memory.read_u32(wheelie_frames_ref)
    
    def inst_wheelie_frames(self) -> int:
        assert(self.is_bike)
        wheelie_frames_ref = self.addr + 0x2A8
        return memory.read_u32(wheelie_frames_ref)
    
    @staticmethod
    def wheelie_cooldown(player_idx=0) -> int:
        assert(KartSettings.is_bike(player_idx))
        kart_move_ref = KartMove.chain(player_idx)
        wheelie_cooldown_ref = kart_move_ref + 0x2B6
        return memory.read_u16(wheelie_cooldown_ref)
    
    def inst_wheelie_cooldown(self) -> int:
        assert(self.addr)
        wheelie_cooldown_ref = self.addr + 0x2B6
        return memory.read_u16(wheelie_cooldown_ref)
    
    @staticmethod
    def wheelie_rotation_decrease(player_idx=0) -> float:
        assert(KartSettings.is_bike(player_idx))
        kart_move_ref = KartMove.chain(player_idx)
        wheelie_rotation_decrease_ref = kart_move_ref + 0x2B8
        return memory.read_f32(wheelie_rotation_decrease_ref)
    
    def inst_wheelie_rotation_decrease(self) -> float:
        assert(self.is_bike)
        wheelie_rotation_decrease_ref = self.addr + 0x2B8
        return memory.read_f32(wheelie_rotation_decrease_ref)