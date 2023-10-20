from dolphin import memory

from . import KartObject

class KartAction:
    def __init__(self, playerIdx=0, addr=None):
        self.addr = addr if addr else KartAction.chain()

        self.frame = self.inst_frame

    @staticmethod
    def chain(playerIdx=0) -> int:
        return KartObject.kart_action(playerIdx)

    @staticmethod
    def frame(playerIdx=0) -> int:
        kart_action_ref = KartAction.chain(playerIdx)
        frame_ref = kart_action_ref + 0xC4
        return memory.read_u32(frame_ref)

    def inst_frame(self) -> int:
        frame_ref = self.addr + 0xC4
        return memory.read_u32(frame_ref)