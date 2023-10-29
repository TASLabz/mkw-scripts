from dolphin import memory

from . import mat34, vec3, quatf, VehicleDynamics

class VehiclePhysics:
    def __init__(self, player_idx=0, addr=None):
        self.addr = addr if addr else VehiclePhysics.chain(player_idx)

        self.inertia_tensor = self.inst_inertia_tensor
        self.inverse_inertia_tensor = self.inst_inverse_inertia_tensor
        self.rotation_speed = self.inst_rotation_speed
        self.position = self.inst_position
        self.external_velocity = self.inst_external_velocity
        self.external_velocity_accel = self.inst_external_velocity_accel
        self.moving_road_velocity = self.inst_moving_road_velocity
        self.moving_water_velocity = self.inst_moving_water_velocity
        self.speed = self.inst_speed
        self.speed_norm = self.inst_speed_norm
        self.main_rotation = self.inst_main_rotation
        self.full_rotation = self.inst_full_rotation
        self.rotation_vector_norm = self.inst_rotation_vector_norm
        self.special_rotation = self.inst_special_rotation
        self.extra_rotation = self.inst_extra_rotation
        self.gravity = self.inst_gravity
        self.internal_velocity = self.inst_internal_velocity
        self.top = self.inst_top
        self.no_gravity = self.inst_no_gravity
        self.in_bullet = self.inst_in_bullet
        self.stabilization_factor = self.inst_stabilization_factor
        self.speed_fix = self.inst_speed_fix
        self.top_2 = self.inst_top_2
        self.scale = self.inst_scale

    @staticmethod
    def chain(player_idx=0) -> int:
        return VehicleDynamics.vehicle_physics(player_idx)
    
    @staticmethod
    def inertia_tensor(player_idx=0) -> mat34:
        vehicle_physics_ref = VehiclePhysics.chain(player_idx)
        inertia_tensor_ref = vehicle_physics_ref + 0x4
        return mat34.read(inertia_tensor_ref)
    
    def inst_inertia_tensor(self) -> mat34:
        inertia_tensor_ref = self.addr + 0x4
        return mat34.read(inertia_tensor_ref)
    
    @staticmethod
    def inverse_inertia_tensor(player_idx=0) -> mat34:
        vehicle_physics_ref = VehiclePhysics.chain(player_idx)
        inverse_inertia_tensor_ref = vehicle_physics_ref + 0x34
        return mat34.read(inverse_inertia_tensor_ref)
    
    def inst_inverse_inertia_tensor(self) -> mat34:
        inverse_inertia_tensor_ref = self.addr + 0x34
        return mat34.read(inverse_inertia_tensor_ref)
    
    @staticmethod
    def rotation_speed(player_idx=0) -> float:
        vehicle_physics_ref = VehiclePhysics.chain(player_idx)
        rotation_speed_ref = vehicle_physics_ref + 0x64
        return mat34.read(rotation_speed_ref)
    
    def inst_rotation_speed(self) -> float:
        rotation_speed_ref = self.addr + 0x64
        return mat34.read(rotation_speed_ref)
    
    @staticmethod
    def position(player_idx=0) -> vec3:
        vehicle_physics_ref = VehiclePhysics.chain(player_idx)
        position_ref = vehicle_physics_ref + 0x68
        return vec3.read(position_ref)
    
    def inst_position(self) -> vec3:
        position_ref = self.addr + 0x68
        return vec3.read(position_ref)
    
    @staticmethod
    def external_velocity(player_idx=0) -> vec3:
        vehicle_physics_ref = VehiclePhysics.chain(player_idx)
        external_velocity_ref = vehicle_physics_ref + 0x74
        return vec3.read(external_velocity_ref)
    
    def inst_external_velocity(self) -> vec3:
        external_velocity_ref = self.addr + 0x74
        return vec3.read(external_velocity_ref)
    
    @staticmethod
    def external_velocity_accel(player_idx=0) -> vec3:
        vehicle_physics_ref = VehiclePhysics.chain(player_idx)
        external_velocity_accel_ref = vehicle_physics_ref + 0x80
        return vec3.read(external_velocity_accel_ref)
    
    def inst_external_velocity_accel(self) -> vec3:
        external_velocity_accel_ref = self.addr + 0x80
        return vec3.read(external_velocity_accel_ref)
    
    @staticmethod
    def moving_road_velocity(player_idx=0) -> vec3:
        vehicle_physics_ref = VehiclePhysics.chain(player_idx)
        moving_road_velocity_ref = vehicle_physics_ref + 0xB0
        return vec3.read(moving_road_velocity_ref)
    
    def inst_moving_road_velocity(self) -> vec3:
        moving_road_velocity_ref = self.addr + 0xB0
        return vec3.read(moving_road_velocity_ref)
    
    # 0xBC rotVec1 is unused

    @staticmethod
    def moving_water_velocity(player_idx=0) -> vec3:
        vehicle_physics_ref = VehiclePhysics.chain(player_idx)
        moving_water_velocity_ref = vehicle_physics_ref + 0xC8
        return vec3.read(moving_water_velocity_ref)
    
    def inst_moving_water_velocity(self) -> vec3:
        moving_water_velocity_ref = self.addr + 0xC8
        return vec3.read(moving_water_velocity_ref)
    
    @staticmethod
    def speed(player_idx=0) -> vec3:
        vehicle_physics_ref = VehiclePhysics.chain(player_idx)
        speed_ref = vehicle_physics_ref + 0xD4
        return vec3.read(speed_ref)
    
    def inst_speed(self) -> vec3:
        speed_ref = self.addr + 0xD4
        return vec3.read(speed_ref)
    
    @staticmethod
    def speed_norm(player_idx=0) -> float:
        vehicle_physics_ref = VehiclePhysics.chain(player_idx)
        speed_norm_ref = vehicle_physics_ref + 0xE0
        return memory.read_f32(speed_norm_ref)
    
    def inst_speed_norm(self) -> float:
        speed_norm_ref = self.addr + 0xE0
        return memory.read_f32(speed_norm_ref)
    
    # 0xE4 rotVec2 is unused
    
    @staticmethod
    def main_rotation(player_idx=0) -> quatf:
        vehicle_physics_ref = VehiclePhysics.chain(player_idx)
        main_rotation_ref = vehicle_physics_ref + 0xF0
        return quatf.read(main_rotation_ref)
    
    def inst_main_rotation(self) -> quatf:
        main_rotation_ref = self.addr + 0xF0
        return quatf.read(main_rotation_ref)
    
    @staticmethod
    def full_rotation(player_idx=0) -> quatf:
        vehicle_physics_ref = VehiclePhysics.chain(player_idx)
        full_rotation_ref = vehicle_physics_ref + 0x100
        return quatf.read(full_rotation_ref)
    
    def inst_full_rotation(self) -> quatf:
        full_rotation_ref = self.addr + 0x100
        return quatf.read(full_rotation_ref)
    
    @staticmethod
    def accel_norm(player_idx=0) -> vec3:
        vehicle_physics_ref = VehiclePhysics.chain(player_idx)
        accel_norm_ref = vehicle_physics_ref + 0x110
        return vec3.read(accel_norm_ref)
    
    def inst_accel_norm(self) -> vec3:
        accel_norm_ref = self.addr + 0x110
        return vec3.read(accel_norm_ref)
    
    @staticmethod
    def rotation_vector_norm(player_idx=0) -> vec3:
        vehicle_physics_ref = VehiclePhysics.chain(player_idx)
        rotation_vector_norm_ref = vehicle_physics_ref + 0x11C
        return vec3.read(rotation_vector_norm_ref)
    
    def inst_rotation_vector_norm(self) -> vec3:
        rotation_vector_norm_ref = self.addr + 0x11C
        return vec3.read(rotation_vector_norm_ref)
    
    @staticmethod
    def special_rotation(player_idx=0) -> quatf:
        vehicle_physics_ref = VehiclePhysics.chain(player_idx)
        special_rotation_ref = vehicle_physics_ref + 0x128
        return quatf.read(special_rotation_ref)
    
    def inst_special_rotation(self) -> quatf:
        special_rotation_ref = self.addr + 0x128
        return quatf.read(special_rotation_ref)
    
    @staticmethod
    def extra_rotation(player_idx=0) -> quatf:
        vehicle_physics_ref = VehiclePhysics.chain(player_idx)
        extra_rotation_ref = vehicle_physics_ref + 0x138
        return quatf.read(extra_rotation_ref)
    
    def inst_extra_rotation(self) -> quatf:
        extra_rotation_ref = self.addr + 0x138
        return quatf.read(extra_rotation_ref)
    
    @staticmethod
    def gravity(player_idx=0) -> float:
        vehicle_physics_ref = VehiclePhysics.chain(player_idx)
        gravity_ref = vehicle_physics_ref + 0x148
        return memory.read_f32(gravity_ref)
    
    def inst_gravity(player_idx=0) -> float:
        vehicle_physics_ref = VehiclePhysics.chain(player_idx)
        gravity_ref = vehicle_physics_ref + 0x148
        return memory.read_f32(gravity_ref)
    
    @staticmethod
    def internal_velocity(player_idx=0) -> vec3:
        vehicle_physics_ref = VehiclePhysics.chain(player_idx)
        internal_velocity_ref = vehicle_physics_ref + 0x14C
        return vec3.read(internal_velocity_ref)
    
    def inst_internal_velocity(self) -> vec3:
        internal_velocity_ref = self.addr + 0x14C
        return vec3.read(internal_velocity_ref)
    
    @staticmethod
    def top(player_idx=0) -> vec3:
        vehicle_physics_ref = VehiclePhysics.chain(player_idx)
        top_ref = vehicle_physics_ref + 0x158
        return vec3.read(top_ref)
    
    def inst_top(self) -> vec3:
        top_ref = self.addr + 0x158
        return vec3.read(top_ref)
    
    @staticmethod
    def no_gravity(player_idx=0) -> bool:
        vehicle_physics_ref = VehiclePhysics.chain(player_idx)
        no_gravity_ref = vehicle_physics_ref + 0x171
        return memory.read_u8(no_gravity_ref) > 0
    
    def inst_no_gravity(self) -> bool:
        no_gravity_ref = self.addr + 0x171
        return memory.read_u8(no_gravity_ref) > 0
    
    @staticmethod
    def in_bullet(player_idx=0) -> bool:
        vehicle_physics_ref = VehiclePhysics.chain(player_idx)
        in_bullet_ref = vehicle_physics_ref + 0x174
        return memory.read_u8(in_bullet_ref) > 0
    
    def inst_in_bullet(self) -> bool:
        in_bullet_ref = self.addr + 0x174
        return memory.read_u8(in_bullet_ref) > 0
    
    @staticmethod
    def stabilization_factor(player_idx=0) -> float:
        vehicle_physics_ref = VehiclePhysics.chain(player_idx)
        stabilization_factor_ref = vehicle_physics_ref + 0x178
        return memory.read_f32(stabilization_factor_ref)
    
    def inst_stabilization_factor(self) -> float:
        stabilization_factor_ref = self.addr + 0x178
        return memory.read_f32(stabilization_factor_ref)
    
    @staticmethod
    def speed_fix(player_idx=0) -> float:
        vehicle_physics_ref = VehiclePhysics.chain(player_idx)
        speed_fix_ref = vehicle_physics_ref + 0x17C
        return memory.read_f32(speed_fix_ref)
    
    def inst_speed_fix(self) -> float:
        speed_fix_ref = self.addr + 0x17C
        return memory.read_f32(speed_fix_ref)
    
    @staticmethod
    def top_2(player_idx=0) -> vec3:
        vehicle_physics_ref = VehiclePhysics.chain(player_idx)
        top_2_ref = vehicle_physics_ref + 0x180
        return vec3.read(top_2_ref)
    
    def inst_top_2(self) -> vec3:
        top_2_ref = self.addr + 0x180
        return vec3.read(top_2_ref)
    
    @staticmethod
    def scale(player_idx=0) -> vec3:
        vehicle_physics_ref = VehiclePhysics.chain(player_idx)
        scale_ref = vehicle_physics_ref + 0x1A8
        return vec3.read(scale_ref)
    
    def inst_scale(self) -> vec3:
        scale_ref = self.addr + 0x1A8
        return vec3.read(scale_ref)