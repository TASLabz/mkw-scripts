from dolphin import memory

from . import KartParam, WheelCount, VehicleType

class PlayerStats:
    def __init__(self, playerIdx=0, addr=None):
        self.addr = addr if addr else PlayerStats.chain(playerIdx)

        self.wheel_count_enum = self.inst_wheel_count_enum
        self.vehicle_type_enum = self.inst_vehicle_type_enum
        self.weight_class = self.inst_weight_class
        self.weight = self.inst_weight
        self.bump_deviation_level = self.inst_bump_deviation_level
        self.base_speed = self.inst_base_speed
        self.handling_speed_multiplier = self.inst_handling_speed_multiplier
        self.tilt = self.inst_tilt
        self.standard_accel_as = self.inst_standard_accel_as
        self.standard_accel_ts = self.inst_standard_accel_ts
        self.drift_accel_as = self.inst_drift_accel_as
        self.drift_accel_ts = self.inst_drift_accel_ts
        self.manual_handling = self.inst_manual_handling
        self.auto_handling = self.inst_auto_handling
        self.handling_reactivity = self.inst_handling_reactivity
        self.manual_drift = self.inst_manual_drift
        self.auto_drift = self.inst_auto_drift
        self.drift_reactivity = self.inst_drift_reactivity
        self.target_angle = self.inst_target_angle
        self.outside_drift_decrement = self.inst_outside_drift_decrement
        self.mt_duration = self.inst_mt_duration
        self.speed_factors = self.inst_speed_factors
        self.handling_factors = self.inst_handling_factors
        self.rotating_item_obj_param = self.inst_rotating_item_obj_param
        self.vertical_tilt = self.inst_vertical_tilt
        self.mega_scale = self.inst_mega_scale
        self.tire_distance = self.inst_tire_distance
    
    @staticmethod
    def chain(playerIdx=0) -> int:
        return KartParam.player_stats(playerIdx)

    @staticmethod
    def wheel_count_enum(playerIdx=0) -> WheelCount:
        player_stats_ref = PlayerStats.chain(playerIdx)
        wheel_count_enum_ref = player_stats_ref + 0x0
        return WheelCount(memory.read_u32(wheel_count_enum_ref))

    def inst_wheel_count_enum(self) -> WheelCount:
        wheel_count_enum_ref = self.addr + 0x0
        return WheelCount(memory.read_u32(wheel_count_enum_ref))

    @staticmethod
    def vehicle_type_enum(playerIdx=0) -> VehicleType:
        player_stats_ref = PlayerStats.chain(playerIdx)
        vehicle_type_enum_ref = player_stats_ref + 0x4
        return VehicleType(memory.read_u32(vehicle_type_enum_ref))

    def inst_vehicle_type_enum(self) -> VehicleType:
        vehicle_type_enum_ref = self.addr + 0x4
        return VehicleType(memory.read_u32(vehicle_type_enum_ref))

    @staticmethod
    def weight_class(playerIdx=0) -> int:
        player_stats_ref = PlayerStats.chain(playerIdx)
        weight_class_ref = player_stats_ref + 0x8
        return memory.read_u32(weight_class_ref)

    def inst_weight_class(self) -> int:
        weight_class_ref = self.addr + 0x8
        return memory.read_u32(weight_class_ref)

    @staticmethod
    def weight(playerIdx=0) -> float:
        player_stats_ref = PlayerStats.chain(playerIdx)
        weight_ref = player_stats_ref + 0x10
        return memory.read_f32(weight_ref)

    def inst_weight(self) -> float:
        weight_ref = self.addr + 0x10
        return memory.read_f32(weight_ref)

    @staticmethod
    def bump_deviation_level(playerIdx=0) -> float:
        player_stats_ref = PlayerStats.chain(playerIdx)
        bump_deviation_level_ref = player_stats_ref + 0x14
        return memory.read_f32(bump_deviation_level_ref)

    def inst_bump_deviation_level(self) -> float:
        bump_deviation_level_ref = self.addr + 0x14
        return memory.read_f32(bump_deviation_level_ref)

    @staticmethod
    def base_speed(playerIdx=0) -> float:
        player_stats_ref = PlayerStats.chain(playerIdx)
        base_speed_ref = player_stats_ref + 0x18
        return memory.read_f32(base_speed_ref)

    def inst_base_speed(self) -> float:
        base_speed_ref = self.addr + 0x18
        return memory.read_f32(base_speed_ref)

    @staticmethod
    def handling_speed_multiplier(playerIdx=0) -> float:
        player_stats_ref = PlayerStats.chain(playerIdx)
        handling_speed_multiplier_ref = player_stats_ref + 0x1C
        return memory.read_f32(handling_speed_multiplier_ref)

    def inst_handling_speed_multiplier(self) -> float:
        handling_speed_multiplier_ref = self.addr + 0x1C
        return memory.read_f32(handling_speed_multiplier_ref)

    @staticmethod
    def tilt(playerIdx=0) -> float:
        player_stats_ref = PlayerStats.chain(playerIdx)
        tilt_ref = player_stats_ref + 0x20
        return memory.read_f32(tilt_ref)

    def inst_tilt(self) -> float:
        tilt_ref = self.addr + 0x20
        return memory.read_f32(tilt_ref)

    @staticmethod
    def standard_accel_as(playerIdx=0, accelIdx=0) -> float:
        player_stats_ref = PlayerStats.chain(playerIdx)
        assert (0 <= accelIdx <= 3)
        standard_accel_as_ref = player_stats_ref + 0x24 + (accelIdx * 0x4)
        return memory.read_f32(standard_accel_as_ref)

    def inst_standard_accel_as(self, accelIdx=0) -> float:
        assert (0 <= accelIdx <= 3)
        standard_accel_as_ref = self.addr + 0x24 + (accelIdx * 0x4)
        return memory.read_f32(standard_accel_as_ref)

    @staticmethod
    def standard_accel_ts(playerIdx=0, accelIdx=0) -> float:
        player_stats_ref = PlayerStats.chain(playerIdx)
        assert (0 <= accelIdx <= 2)
        standard_accel_ts_ref = player_stats_ref + 0x34 + (accelIdx * 0x4)
        return memory.read_f32(standard_accel_ts_ref)

    def inst_standard_accel_ts(self, accelIdx=0) -> float:
        assert (0 <= accelIdx <= 2)
        standard_accel_ts_ref = self.addr + 0x34 + (accelIdx * 0x4)
        return memory.read_f32(standard_accel_ts_ref)

    @staticmethod
    def drift_accel_as(playerIdx=0, accelIdx=0) -> float:
        player_stats_ref = PlayerStats.chain(playerIdx)
        assert (0 <= accelIdx <= 1)
        drift_accel_as_ref = player_stats_ref + 0x40 + (accelIdx * 0x4)
        return memory.read_f32(drift_accel_as_ref)

    def inst_drift_accel_as(self, accelIdx=0) -> float:
        assert (0 <= accelIdx <= 1)
        drift_accel_as_ref = self.addr + 0x40 + (accelIdx * 0x4)
        return memory.read_f32(drift_accel_as_ref)

    @staticmethod
    def drift_accel_ts(playerIdx=0) -> float:
        player_stats_ref = PlayerStats.chain(playerIdx)
        drift_accel_ts_ref = player_stats_ref + 0x48
        return memory.read_f32(drift_accel_ts_ref)

    def inst_drift_accel_ts(self) -> float:
        drift_accel_ts_ref = self.addr + 0x48
        return memory.read_f32(drift_accel_ts_ref)

    @staticmethod
    def manual_handling(playerIdx=0) -> float:
        player_stats_ref = PlayerStats.chain(playerIdx)
        manual_handling_ref = player_stats_ref + 0x4C
        return memory.read_f32(manual_handling_ref)

    def inst_manual_handling(self) -> float:
        manual_handling_ref = self.addr + 0x4C
        return memory.read_f32(manual_handling_ref)

    @staticmethod
    def auto_handling(playerIdx=0) -> float:
        player_stats_ref = PlayerStats.chain(playerIdx)
        auto_handling_ref = player_stats_ref + 0x50
        return memory.read_f32(auto_handling_ref)

    def inst_auto_handling(self) -> float:
        auto_handling_ref = self.addr + 0x50
        return memory.read_f32(auto_handling_ref)

    @staticmethod
    def handling_reactivity(playerIdx=0) -> float:
        player_stats_ref = PlayerStats.chain(playerIdx)
        handling_reactivity_ref = player_stats_ref + 0x54
        return memory.read_f32(handling_reactivity_ref)

    def inst_handling_reactivity(self) -> float:
        handling_reactivity_ref = self.addr + 0x54
        return memory.read_f32(handling_reactivity_ref)

    @staticmethod
    def manual_drift(playerIdx=0) -> float:
        player_stats_ref = PlayerStats.chain(playerIdx)
        manual_drift_ref = player_stats_ref + 0x58
        return memory.read_f32(manual_drift_ref)

    def inst_manual_drift(self) -> float:
        manual_drift_ref = self.addr + 0x58
        return memory.read_f32(manual_drift_ref)

    @staticmethod
    def auto_drift(playerIdx=0) -> float:
        player_stats_ref = PlayerStats.chain(playerIdx)
        auto_drift_ref = player_stats_ref + 0x5C
        return memory.read_f32(auto_drift_ref)

    def inst_auto_drift(self) -> float:
        auto_drift_ref = self.addr + 0x5C
        return memory.read_f32(auto_drift_ref)

    @staticmethod
    def drift_reactivity(playerIdx=0) -> float:
        player_stats_ref = PlayerStats.chain(playerIdx)
        drift_reactivity_ref = player_stats_ref + 0x60
        return memory.read_f32(drift_reactivity_ref)

    def inst_drift_reactivity(self) -> float:
        drift_reactivity_ref = self.addr + 0x60
        return memory.read_f32(drift_reactivity_ref)

    @staticmethod
    def target_angle(playerIdx=0) -> float:
        """Outside drift target angle"""
        player_stats_ref = PlayerStats.chain(playerIdx)
        target_angle_ref = player_stats_ref + 0x64
        return memory.read_f32(target_angle_ref)

    def inst_target_angle(self) -> float:
        target_angle_ref = self.addr + 0x64
        return memory.read_f32(target_angle_ref)

    @staticmethod
    def outside_drift_decrement(playerIdx=0) -> float:
        player_stats_ref = PlayerStats.chain(playerIdx)
        outside_drift_decrement_ref = player_stats_ref + 0x68
        return memory.read_f32(outside_drift_decrement_ref)

    def inst_outside_drift_decrement(self) -> float:
        """Unknown purpose?"""
        outside_drift_decrement_ref = self.addr + 0x68
        return memory.read_f32(outside_drift_decrement_ref)

    @staticmethod
    def mt_duration(playerIdx=0) -> int:
        player_stats_ref = PlayerStats.chain(playerIdx)
        mt_duration_ref = player_stats_ref + 0x6C
        return memory.read_s32(mt_duration_ref)

    def inst_mt_duration(self) -> int:
        mt_duration_ref = self.addr + 0x6C
        return memory.read_s32(mt_duration_ref)

    @staticmethod
    def speed_factors(playerIdx=0, factorIdx=0) -> float:
        assert(0 <= factorIdx < 0x20)
        player_stats_ref = PlayerStats.chain(playerIdx)
        speed_factor_ref = player_stats_ref + 0x70 + (factorIdx * 0x4)
        return memory.read_f32(speed_factor_ref)

    def inst_speed_factors(self, factorIdx=0) -> float:
        assert(0 <= factorIdx < 0x20)
        speed_factor_ref = self.addr + 0x70 + (factorIdx * 0x4)
        return memory.read_f32(speed_factor_ref)

    @staticmethod
    def handling_factors(playerIdx=0, factorIdx=0) -> float:
        assert(0 <= factorIdx < 0x20)
        player_stats_ref = PlayerStats.chain(playerIdx)
        handling_factor_ref = player_stats_ref + 0xF0 + (factorIdx * 0x4)
        return memory.read_f32(handling_factor_ref)

    def inst_handling_factors(self, factorIdx=0) -> float:
        assert(0 <= factorIdx < 0x20)
        handling_factor_ref = self.addr + 0xF0 + (factorIdx * 0x4)
        return memory.read_f32(handling_factor_ref)

    @staticmethod
    def rotating_item_obj_param(playerIdx=0, idx=0) -> float:
        assert(0 <= idx < 4)
        player_stats_ref = PlayerStats.chain(playerIdx)
        rotating_item_obj_param_ref = player_stats_ref + 0x170 + (idx * 0x4)
        return memory.read_f32(rotating_item_obj_param_ref)

    def inst_rotating_item_obj_param(self, idx=0) -> float:
        assert(0 <= idx < 4)
        rotating_item_obj_param_ref = self.addr + 0x170 + (idx * 0x4)
        return memory.read_f32(rotating_item_obj_param_ref)

    @staticmethod
    def vertical_tilt(playerIdx=0) -> float:
        player_stats_ref = PlayerStats.chain(playerIdx)
        vertical_tilt_ref = player_stats_ref + 0x180
        return memory.read_f32(vertical_tilt_ref)

    def inst_vertical_tilt(self) -> float:
        vertical_tilt_ref = self.addr + 0x180
        return memory.read_f32(vertical_tilt_ref)

    @staticmethod
    def mega_scale(playerIdx=0) -> float:
        player_stats_ref = PlayerStats.chain(playerIdx)
        mega_scale_ref = player_stats_ref + 0x184
        return memory.read_f32(mega_scale_ref)

    def inst_mega_scale(self) -> float:
        mega_scale_ref = self.addr + 0x184
        return memory.read_f32(mega_scale_ref)

    @staticmethod
    def tire_distance(playerIdx=0) -> float:
        player_stats_ref = PlayerStats.chain(playerIdx)
        tire_distance_ref = player_stats_ref + 0x188
        return memory.read_f32(tire_distance_ref)

    def inst_tire_distance(self) -> float:
        tire_distance_ref = self.addr + 0x188
        return memory.read_f32(tire_distance_ref)