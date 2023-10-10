from dolphin import memory

from . import PlayerInput

class GhostWriter:
    def __init__(self, playerIdx=0, addr=None):
        self.addr = addr if addr else GhostWriter.chain(playerIdx)

        self.button_stream = self.inst_button_stream
        self.buffer = self.inst_buffer

    @staticmethod
    def chain(playerIdx=0) -> int:
        return PlayerInput.ghost_writer(playerIdx)
    
    @staticmethod
    def button_stream(playerIdx=0, streamIdx=0) -> int:
        assert(0 <= streamIdx < 3)
        ghost_writer_ref = GhostWriter.chain(playerIdx)
        button_stream_ptr = ghost_writer_ref + 0x4 + (streamIdx * 0x4)
        return memory.read_u32(button_stream_ptr)
    
    def inst_button_stream(self, streamIdx=0) -> int:
        assert(0 <= streamIdx < 3)
        button_stream_ptr = self.addr + 0x4 + (streamIdx * 0x4)
        return memory.read_u32(button_stream_ptr)
    
    @staticmethod
    def buffer(playerIdx=0) -> int:
        ghost_writer_ref = GhostWriter.chain(playerIdx)
        buffer_ptr = ghost_writer_ref + 0x10
        return memory.read_u32(buffer_ptr)
    
    def inst_buffer(self) -> int:
        buffer_ptr = self.addr + 0x10
        return memory.read_u32(buffer_ptr)