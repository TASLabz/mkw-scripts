from dolphin import memory

from . import InputMgr

class PlayerInput:
    def __init__(self, player_idx=0, addr=None):
        assert(0 <= player_idx < 4)
        self.addr = addr if addr else PlayerInput.chain(player_idx)

        self.kart_input = self.inst_kart_input
        self.ghost_buffer = self.inst_ghost_buffer
        self.is_locked = self.inst_is_locked
        self.ghost_writer = self.inst_ghost_writer

    @staticmethod
    def chain(player_idx=0) -> int:
        return InputMgr.player_input(player_idx)

    @staticmethod
    def kart_input(player_idx=0) -> int:
        player_input_ref = PlayerInput.chain(player_idx)
        kart_input_ref = player_input_ref + 0x0
        return kart_input_ref

    def inst_kart_input(self) -> int:
        kart_input_ref = self.addr + 0x0
        return kart_input_ref
    
    @staticmethod
    def ghost_buffer(player_idx=0) -> int:
        player_input_ref = PlayerInput.chain(player_idx)
        ghost_buffer_ptr = player_input_ref + 0xD8
        return memory.read_u32(ghost_buffer_ptr)
    
    def inst_ghost_buffer(self) -> int:
        ghost_buffer_ptr = self.addr + 0xD8
        return memory.read_u32(ghost_buffer_ptr)
    
    @staticmethod
    def is_locked(player_idx=0) -> bool:
        player_input_ref = PlayerInput.chain(player_idx)
        is_locked_ref = player_input_ref + 0xE4
        return memory.read_u8(is_locked_ref) > 0
    
    def inst_is_locked(self) -> bool:
        is_locked_ref = self.addr + 0xE4
        return memory.read_u8(is_locked_ref) > 0
    
    @staticmethod
    def ghost_writer(player_idx=0) -> int:
        player_input_ref = PlayerInput.chain(player_idx)
        ghost_writer_ptr = player_input_ref + 0xE8
        return memory.read_u32(ghost_writer_ptr)
    
    def inst_ghost_writer(self) -> int:
        ghost_writer_ptr = self.addr + 0xE8
        return memory.read_u32(ghost_writer_ptr)