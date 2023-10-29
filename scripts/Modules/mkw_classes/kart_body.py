from dolphin import memory

from . import mat34, KartObject

class KartBody:
    def __init__(self, player_idx=0, addr=None):
        self.addr = addr if addr else KartBody.chain(player_idx)

        self.kart_body_base = self.inst_kart_body_base
        self.kart_part_base = self.inst_kart_part_base
        self.kart_part_rotation = self.inst_kart_part_rotation
        self.vehicle_dynamics = self.inst_vehicle_dynamics
        self.angle = self.inst_angle
    
    @staticmethod
    def chain(player_idx=0) -> int:
        return KartObject.kart_body(player_idx)

    @staticmethod
    def kart_body_base(player_idx=0) -> int:
        kart_body_ref = KartBody.chain(player_idx)
        return kart_body_ref + 0x10
    
    def inst_kart_body_base(self) -> int:
        return self.addr + 0x10

    @staticmethod
    def kart_part_base(player_idx=0) -> int:
        """This function basically does nothing.
           It's just for readability."""
        kart__body_base = KartBody.kart_body_base(player_idx)
        return kart__body_base + 0x0
    
    def inst_kart_part_base(self) -> int:
        """This function basically does nothing.
           It's just for readability."""
        return self.addr + 0x0
    
    @staticmethod
    def kart_part_rotation(player_idx=0) -> int:
        kart_part_base_ref = KartBody.kart_part_base(player_idx)
        kart_part_rotation_ref = kart_part_base_ref + 0xC
        return mat34.read(kart_part_rotation_ref)
    
    def inst_kart_part_rotation(self) -> int:
        kart_part_rotation_ref = self.addr + 0xC
        return mat34.read(kart_part_rotation_ref)
    
    @staticmethod
    def vehicle_dynamics(player_idx=0) -> int:
        kart_body_base_ref = KartBody.kart_body_base(player_idx)
        vehicle_dynamics_ptr = kart_body_base_ref + 0x80
        return memory.read_u32(vehicle_dynamics_ptr)
    
    def inst_vehicle_dynamics(self) -> int:
        vehicle_dynamics_ptr = self.kart_body_base() + 0x80
        return memory.read_u32(vehicle_dynamics_ptr)
    
    @staticmethod
    def angle(player_idx=0) -> float:
        """Unknown?"""
        kart_part_base_ref = KartBody.kart_body_base(player_idx)
        angle_ptr = kart_part_base_ref + 0x84
        return memory.read_f32(angle_ptr)
    
    def inst_angle(self) -> float:
        """Unknown?"""
        angle_ptr = self.kart_body_base() + 0x84
        return memory.read_f32(angle_ptr)