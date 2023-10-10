from dolphin import memory

class Timer:
    def __init__(self, addr):
        """This class has multiple instances.
           Require that the caller provides an address"""
        self.addr = addr

    def minutes(self) -> int:
        minutes_ref = self.addr + 0x4
        return memory.read_u16(minutes_ref)
    
    def seconds(self) -> int:
        seconds_ref = self.addr + 0x6
        return memory.read_u8(seconds_ref)
    
    def milliseconds(self) -> int:
        milliseconds_ref = self.addr + 0x8
        return memory.read_u16(milliseconds_ref)
    
    def has_finished(self) -> bool:
        has_finished_ref = self.addr + 0xA
        return memory.read_u8(has_finished_ref) > 0