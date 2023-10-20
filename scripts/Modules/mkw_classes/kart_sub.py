from dolphin import memory

from . import KartObject, mat34

class KartSub:
    def __init__(self, playerIdx=0, addr=None):
        self.addr = addr if addr else KartSub.chain(playerIdx)

        self.position = self.inst_position
        self.floor_collision_count = self.inst_floor_collision_count
        self.rotation = self.inst_rotation
        self.wheelie_rotate_angle = self.inst_wheelie_rotate_angle

    @staticmethod
    def chain(playerIdx=0) -> int:
        return KartObject.kart_sub(playerIdx)

    @staticmethod
    def position(playerIdx=0) -> int:
        kart_sub_ref = KartSub.chain(playerIdx)
        position_ref = kart_sub_ref + 0x3C
        return memory.read_u8(position_ref)

    def inst_position(self) -> int:
        position_ref = self.addr + 0x3C
        return memory.read_u8(position_ref)

    @staticmethod
    def floor_collision_count(playerIdx=0) -> int:
        kart_sub_ref = KartSub.chain(playerIdx)
        floor_collision_count_ref = kart_sub_ref + 0x40
        return memory.read_u16(floor_collision_count_ref)

    def inst_floor_collision_count(self) -> int:
        floor_collision_count_ref = self.addr + 0x40
        return memory.read_u16(floor_collision_count_ref)

    @staticmethod
    def rotation(playerIdx=0) -> mat34:
        kart_sub_ref = KartSub.chain(playerIdx)
        rotation_ref = kart_sub_ref + 0x68
        return mat34.read(rotation_ref)

    def inst_rotation(self) -> mat34:
        rotation_ref = self.addr + 0x68
        return mat34.read(rotation_ref)

    @staticmethod
    def wheelie_rotate_angle(playerIdx=0) -> float:
        kart_sub_ref = KartSub.chain(playerIdx)
        wheelie_rotate_angle_ref = kart_sub_ref + 0x98
        return memory.read_f32(wheelie_rotate_angle_ref)

    def inst_wheelie_rotate_angle(self) -> float:
        wheelie_rotate_angle_ref = self.addr + 0x98
        return memory.read_f32(wheelie_rotate_angle_ref)