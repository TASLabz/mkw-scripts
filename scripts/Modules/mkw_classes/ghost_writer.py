from dolphin import memory

from . import PlayerInput

class GhostWriter:
    def __init__(self, player_idx=0, addr=None):
        self.addr = addr if addr else GhostWriter.chain(player_idx)

        self.button_stream = self.inst_button_stream
        self.buffer = self.inst_buffer

    @staticmethod
    def chain(player_idx=0) -> int:
        return PlayerInput.ghost_writer(player_idx)
    
    @staticmethod
    def button_stream(player_idx=0, stream_idx=0) -> int:
        assert(0 <= stream_idx < 3)
        ghost_writer_ref = GhostWriter.chain(player_idx)
        button_stream_ptr = ghost_writer_ref + 0x4 + (stream_idx * 0x4)
        return memory.read_u32(button_stream_ptr)
    
    def inst_button_stream(self, stream_idx=0) -> int:
        assert(0 <= stream_idx < 3)
        button_stream_ptr = self.addr + 0x4 + (stream_idx * 0x4)
        return memory.read_u32(button_stream_ptr)
    
    @staticmethod
    def buffer(player_idx=0) -> int:
        ghost_writer_ref = GhostWriter.chain(player_idx)
        buffer_ptr = ghost_writer_ref + 0x10
        return memory.read_u32(buffer_ptr)
    
    def inst_buffer(self) -> int:
        buffer_ptr = self.addr + 0x10
        return memory.read_u32(buffer_ptr)