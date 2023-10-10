from dolphin import memory
from enum import Enum

class ControllerInfo:
    class ControlSource(Enum):
        CONTROL_SOURCE_UNKNOWN = -1
        CONTROL_SOURCE_CORE = 0  # WiiMote
        CONTROL_SOURCE_FREESTYLE = 1  # WiiMote + Nunchuk
        CONTROL_SOURCE_CLASSIC = 2  # Classic Controller
        CONTROL_SOURCE_GAMECUBE = 3
        CONTROL_SOURCE_GHOST = 4
        CONTROL_SOURCE_AI = 5
    
    def __init__(self, addr):
        """There are multiple instances of this class (likely just copies).
           To create an instance, enforce that the caller passes in its address."""
        self.addr = addr

    def control_source(self) -> "ControllerInfo.ControlSource":
        control_source_ref = self.addr + 0x0
        return ControllerInfo.ControlSource(memory.read_u32(control_source_ref))
    
    def wiimote_address(self) -> bytearray:
        wiimote_address_ref = self.addr + 0x4
        return memory.read_bytes(wiimote_address_ref, 0x6)
    
    def channel(self) -> int:
        channel_ref = self.addr + 0xC
        return memory.read_u32(channel_ref)