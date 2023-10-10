from dolphin import memory

from . import vec3, quatf, mat34, KartBody

class VehicleDynamics:
    def __init__(self, playerIdx=0, addr=None):
        self.addr = addr if addr else VehicleDynamics.chain(playerIdx)

        self.vehicle_physics = self.inst_vehicle_physics
        self.collision_group = self.inst_collision_group
        self.position = self.inst_position
        self.decaying_trick_rotation = self.inst_decaying_trick_rotation
        self.instantaneous_trick_rotation = self.inst_instantaneous_trick_rotation
        self.special_rotation = self.inst_special_rotation
        self.decaying_extra_rotation = self.inst_decaying_extra_rotation
        self.instantaneous_extra_rotation = self.inst_instantaneous_extra_rotation
        self.extra_rotation = self.inst_extra_rotation
        self.pose = self.inst_pose
        self.x_axis = self.inst_x_axis
        self.y_axis = self.inst_y_axis
        self.z_axis = self.inst_z_axis
        self.speed = self.inst_speed

    @staticmethod
    def chain(playerIdx=0) -> int:
        return KartBody.vehicle_dynamics(playerIdx)
    
    @staticmethod
    def vehicle_physics(playerIdx=0) -> int:
        vehicle_dynamics_ref = VehicleDynamics.chain(playerIdx)
        vehicle_physics_ptr = vehicle_dynamics_ref + 0x4
        return memory.read_u32(vehicle_physics_ptr)
    
    def inst_vehicle_physics(self) -> int:
        vehicle_physics_ptr = self.addr + 0x4
        return memory.read_u32(vehicle_physics_ptr)
    
    @staticmethod
    def collision_group(playerIdx=0) -> int:
        vehicle_dynamics_ref = VehicleDynamics.chain(playerIdx)
        collision_group_ptr = vehicle_dynamics_ref + 0x8
        return memory.read_u32(collision_group_ptr)
        #TODO

    def inst_collision_group(self) -> int:
        collision_group_ptr = self.addr + 0x8
        return memory.read_u32(collision_group_ptr)
    
    @staticmethod
    def position(playerIdx=0) -> vec3:
        vehicle_dynamics_ref = VehicleDynamics.chain(playerIdx)
        position_ref = vehicle_dynamics_ref + 0x18
        return vec3.read(position_ref)
    
    def inst_position(self) -> vec3:
        position_ref = self.addr + 0x18
        return vec3.read(position_ref)
    
    @staticmethod
    def decaying_trick_rotation(playerIdx=0) -> quatf:
        """After ending a trick early, this contains the leftover
           trick rotation, which decays to zero."""
        vehicle_dynamics_ref = VehicleDynamics.chain(playerIdx)
        decaying_trick_rotation_ref = vehicle_dynamics_ref + 0x24
        return quatf.read(decaying_trick_rotation_ref)
    
    def inst_decaying_trick_rotation(self) -> quatf:
        """After ending a trick early, this contains the leftover
           trick rotation, which decays to zero."""
        decaying_trick_rotation_ref = self.addr + 0x24
        return quatf.read(decaying_trick_rotation_ref)
    
    @staticmethod
    def instantaneous_trick_rotation(playerIdx=0) -> quatf:
        """The extra rotation from a trick during midair."""
        vehicle_dynamics_ref = VehicleDynamics.chain(playerIdx)
        instantaneous_trick_rotation_ref = vehicle_dynamics_ref + 0x34
        return quatf.read(instantaneous_trick_rotation_ref)
    
    def inst_instantaneous_trick_rotation(self) -> quatf:
        """The extra rotation from a trick during midair."""
        instantaneous_trick_rotation_ref = self.addr + 0x34
        return quatf.read(instantaneous_trick_rotation_ref)
    
    @staticmethod
    def special_rotation(playerIdx=0) -> quatf:
        """Extra rotation caused by ramp/halfpipe tricks.
           Only for display. Does not affect physics."""
        vehicle_dynamics_ref = VehicleDynamics.chain(playerIdx)
        special_rotation_ref = vehicle_dynamics_ref + 0x44
        return quatf.read(special_rotation_ref)
    
    def inst_special_rotation(self) -> quatf:
        """Extra rotation caused by ramp/halfpipe tricks.
           Only for display. Does not affect physics."""
        special_rotation_ref = self.addr + 0x44
        return quatf.read(special_rotation_ref)
    
    @staticmethod
    def decaying_extra_rotation(playerIdx=0) -> quatf:
        vehicle_dynamics_ref = VehicleDynamics.chain(playerIdx)
        decaying_extra_rotation_ref = vehicle_dynamics_ref + 0x54
        return quatf.read(decaying_extra_rotation_ref)
    
    def inst_decaying_extra_rotation(self) -> quatf:
        decaying_extra_rotation_ref = self.addr + 0x54
        return quatf.read(decaying_extra_rotation_ref)
    
    @staticmethod
    def instantaneous_extra_rotation(playerIdx=0) -> quatf:
        vehicle_dynamics_ref = VehicleDynamics.chain(playerIdx)
        instantaneous_extra_rotation_ref = vehicle_dynamics_ref + 0x64
        return quatf.read(instantaneous_extra_rotation_ref)
    
    def inst_instantaneous_extra_rotation(self) -> quatf:
        instantaneous_extra_rotation_ref = self.addr + 0x64
        return quatf.read(instantaneous_extra_rotation_ref)
    
    @staticmethod
    def extra_rotation(playerIdx=0) -> quatf:
        vehicle_dynamics_ref = VehicleDynamics.chain(playerIdx)
        extra_rotation_ref = vehicle_dynamics_ref + 0x74
        return quatf.read(extra_rotation_ref)
    
    def inst_extra_rotation(self) -> quatf:
        extra_rotation_ref = self.addr + 0x74
        return quatf.read(extra_rotation_ref)
    
    @staticmethod
    def pose(playerIdx=0) -> mat34:
        """Does not include wheelie"""
        vehicle_dynamics_ref = VehicleDynamics.chain(playerIdx)
        pose_ref = vehicle_dynamics_ref + 0x9C
        return mat34.read(pose_ref)
    
    def inst_pose(self) -> mat34:
        """Does not include wheelie"""
        pose_ref = self.addr + 0x9C
        return mat34.read(pose_ref)
    
    @staticmethod
    def x_axis(playerIdx=0) -> vec3:
        vehicle_dynamics_ref = VehicleDynamics.chain(playerIdx)
        x_axis_ref = vehicle_dynamics_ref + 0xCC
        return vec3.read(x_axis_ref)
    
    def inst_x_axis(self) -> vec3:
        x_axis_ref = self.addr + 0xCC
        return vec3.read(x_axis_ref)
    
    @staticmethod
    def y_axis(playerIdx=0) -> vec3:
        vehicle_dynamics_ref = VehicleDynamics.chain(playerIdx)
        y_axis_ref = vehicle_dynamics_ref + 0xD8
        return vec3.read(y_axis_ref)
    
    def inst_y_axis(self) -> vec3:
        y_axis_ref = self.addr + 0xD8
        return vec3.read(y_axis_ref)
    
    @staticmethod
    def z_axis(playerIdx=0) -> vec3:
        vehicle_dynamics_ref = VehicleDynamics.chain(playerIdx)
        z_axis_ref = vehicle_dynamics_ref + 0xE4
        return vec3.read(z_axis_ref)
    
    def inst_z_axis(self) -> vec3:
        z_axis_ref = self.addr + 0xE4
        return vec3.read(z_axis_ref)
    
    @staticmethod
    def speed(playerIdx=0) -> vec3:
        vehicle_dynamics_ref = VehicleDynamics.chain(playerIdx)
        speed_ref = vehicle_dynamics_ref + 0xF0
        return vec3.read(speed_ref)
    
    def inst_speed(self) -> vec3:
        speed_ref = self.addr + 0xF0
        return vec3.read(speed_ref)