from dolphin import memory

class GhostButtonsStream:
        def __init__(self, addr):
            """There are multiple instances of this class.
               Require that the caller provide the address."""
            self.addr = addr
        
        def buffer(self) -> int:
            buffer_ptr = self.addr + 0x4
            return memory.read_u32(buffer_ptr)
        
        def sequence_count(self) -> int:
            sequence_count_ref = self.addr + 0x8
            return memory.read_u32(sequence_count_ref)
        
        def size(self) -> int:
            size_ref = self.addr + 0xC
            return memory.read_u32(size_ref)
        
        def read_sequence_frames(self) -> int:
            read_sequence_frames_ref = self.addr + 0x10
            return memory.read_u16(read_sequence_frames_ref)

        def state(self) -> int:
            state_ref = self.addr + 0x14
            return memory.read_u32(state_ref)