from dolphin import memory

from . import vec2

class UIInputState:
        def __init__(self, addr):
            """There are multiple instances of this class (likely just copies).
           To create an instance, enforce that the caller passes in its address."""
            self.addr = addr

        def buttons(self) -> int:
            buttons_ref = self.addr + 0x4
            return buttons_ref

        def raw_buttons(self) -> int:
            raw_buttons_ref = self.addr + 0x6
            return memory.read_u16(raw_buttons_ref)

        def stick(self) -> int:
            stick_ref = self.addr + 0x8
            return memory.read_u16(stick_ref)

        def discrete_stick_x(self) -> int:
            discrete_stick_x_ref = self.addr + 0x18
            return memory.read_u8(discrete_stick_x_ref)

        def discrete_stick_y(self) -> int:
            discrete_stick_y_ref = self.addr + 0x19
            return memory.read_u8(discrete_stick_y_ref)

        def pointer_pos(self) -> vec2:
            pointer_pos_ref = self.addr + 0x1C
            return vec2.read(pointer_pos_ref)

        def pointer_horizon(self) -> vec2:
            pointer_horizon_ref = self.addr + 0x24
            return vec2.read(pointer_horizon_ref)

        def pointer_dist(self) -> float:
            pointer_dist_ref = self.addr + 0x2C
            return memory.read_f32(pointer_dist_ref)