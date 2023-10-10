from dolphin import memory

from . import vec2

class ButtonActions:
    def __init__(self, value):
        self.value = value

    A = 0x1
    B = 0x2
    L = 0x4
    R_UNUSED = 0x8
    LOOK_BACKWARDS = 0x20
    

class RaceInputState:
        """There are multiple instances of this class (likely just copies).
           To create an instance, enforce that the caller passes in its address."""
        def __init__(self, addr):
            self.addr = addr

        def buttons(self) -> ButtonActions:
            buttons_ref = self.addr + 0x4
            return ButtonActions(memory.read_u16(buttons_ref))

        def raw_buttons(self) -> int:
            raw_buttons_ref = self.addr + 0x6
            return memory.read_u16(raw_buttons_ref)

        def stick(self) -> vec2:
            stick_ref = self.addr + 0x8
            return vec2.read(stick_ref)

        def raw_stick_x(self) -> int:
            raw_stick_x_ref = self.addr + 0x10
            return memory.read_u8(raw_stick_x_ref)
        
        def raw_stick_y(self) -> int:
            raw_stick_y_ref = self.addr + 0x11
            return memory.read_u8(raw_stick_y_ref)

        def trick(self) -> int:
            trick_ref = self.addr + 0x12
            return memory.read_u8(trick_ref)

        def raw_trick(self) -> int:
            raw_trick_ref = self.addr + 0x13
            return memory.read_u8(raw_trick_ref)

        def is_valid(self) -> int:
            is_valid_ref = self.addr + 0x14
            return memory.read_u8(is_valid_ref)