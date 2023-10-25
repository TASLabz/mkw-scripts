from dolphin import memory

from . import KartObject, mat34

class KartSub:
    def __init__(self, player_idx=0, addr=None):
        self.addr = addr if addr else KartSub.chain(player_idx)

        self.position = self.inst_position
        self.floor_collision_count = self.inst_floor_collision_count
        self.rotation = self.inst_rotation
        self.wheelie_rotate_angle = self.inst_wheelie_rotate_angle

    @staticmethod
    def chain(player_idx=0) -> int:
        return KartObject.kart_sub(player_idx)

    @staticmethod
    def position(player_idx=0) -> int:
        kart_sub_ref = KartSub.chain(player_idx)
        position_ref = kart_sub_ref + 0x3C
        return memory.read_u8(position_ref)

    def inst_position(self) -> int:
        position_ref = self.addr + 0x3C
        return memory.read_u8(position_ref)

    @staticmethod
    def floor_collision_count(player_idx=0) -> int:
        kart_sub_ref = KartSub.chain(player_idx)
        floor_collision_count_ref = kart_sub_ref + 0x40
        return memory.read_u16(floor_collision_count_ref)

    def inst_floor_collision_count(self) -> int:
        floor_collision_count_ref = self.addr + 0x40
        return memory.read_u16(floor_collision_count_ref)

    @staticmethod
    def rotation(player_idx=0) -> mat34:
        kart_sub_ref = KartSub.chain(player_idx)
        rotation_ref = kart_sub_ref + 0x68
        return mat34.read(rotation_ref)

    def inst_rotation(self) -> mat34:
        rotation_ref = self.addr + 0x68
        return mat34.read(rotation_ref)

    @staticmethod
    def wheelie_rotate_angle(player_idx=0) -> float:
        kart_sub_ref = KartSub.chain(player_idx)
        wheelie_rotate_angle_ref = kart_sub_ref + 0x98
        return memory.read_f32(wheelie_rotate_angle_ref)

    def inst_wheelie_rotate_angle(self) -> float:
        wheelie_rotate_angle_ref = self.addr + 0x98
        return memory.read_f32(wheelie_rotate_angle_ref)