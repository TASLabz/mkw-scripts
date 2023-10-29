from dolphin import memory

from . import quatf, KartMove

class KartHalfPipe:
    def __init__(self, player_idx=0, addr=None):
        self.addr = addr if addr else KartHalfPipe.chain(player_idx)

        self.type = self.inst_type
        self.rot_sign = self.inst_rot_sign
        self.next_timer = self.inst_next_timer
        self.trick_direction = self.inst_trick_direction
        self.rotation = self.inst_rotation

    @staticmethod
    def chain(player_idx=0) -> int:
        return KartMove.kart_half_pipe(player_idx)
    
    @staticmethod
    def type(player_idx=0) -> int:
        half_pipe_ref = KartHalfPipe.chain(player_idx)
        type_ref = half_pipe_ref + 0x70
        return memory.read_u32(type_ref)
    
    def inst_type(self) -> int:
        type_ref = self.addr + 0x70
        return memory.read_u32(type_ref)
    
    @staticmethod
    def rot_sign(player_idx=0) -> float:
        """+1 or -1?"""
        half_pipe_ref = KartHalfPipe.chain(player_idx)
        rot_sign_ref = half_pipe_ref + 0x74
        return memory.read_f32(rot_sign_ref)
    
    def inst_rot_sign(self) -> float:
        """+1 or -1?"""
        rot_sign_ref = self.addr + 0x74
        return memory.read_f32(rot_sign_ref)
    
    @staticmethod
    def next_timer(player_idx=0) -> int:
        half_pipe_ref = KartHalfPipe.chain(player_idx)
        next_timer_ref = half_pipe_ref + 0x78
        return memory.read_u16(next_timer_ref)
    
    def inst_next_timer(self) -> int:
        next_timer_ref = self.addr + 0x78
        return memory.read_u16(next_timer_ref)
    
    @staticmethod
    def trick_direction(player_idx=0) -> int:
        half_pipe_ref = KartHalfPipe.chain(player_idx)
        trick_direction_ref = half_pipe_ref + 0x7A
        return memory.read_u8(trick_direction_ref)
    
    def inst_trick_direction(self) -> int:
        trick_direction_ref = self.addr + 0x7A
        return memory.read_u8(trick_direction_ref)
    
    @staticmethod
    def rotation(player_idx=0) -> quatf:
        half_pipe_ref = KartHalfPipe.chain(player_idx)
        rotation_ref = half_pipe_ref + 0x7C
        return quatf.read(rotation_ref)
    
    def inst_rotation(self) -> quatf:
        rotation_ref = self.addr + 0x7C
        return quatf.read(rotation_ref)