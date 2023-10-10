from dolphin import memory

from . import KartSettings

class KartParam:
    def __init__(self, playerIdx=0, addr=None):
        self.addr = addr if addr else KartParam.chain(playerIdx)

        self.player_stats = self.inst_player_stats
        self.bsp = self.inst_bsp
    
    @staticmethod
    def chain(playerIdx=0) -> int:
        return KartSettings.kart_param(playerIdx)

    @staticmethod
    def player_stats(playerIdx=0) -> int:
        kart_param_ref = KartParam.chain(playerIdx)
        player_stats_ptr = kart_param_ref + 0x0
        return memory.read_u32(player_stats_ptr)
    
    def inst_player_stats(self) -> int:
        player_stats_ptr = self.addr + 0x0
        return memory.read_u32(player_stats_ptr)

    @staticmethod
    def bsp(playerIdx=0) -> int:
        kart_param_ref = KartParam.chain(playerIdx)
        bsp_ptr = kart_param_ref + 0x04
        return memory.read_u32(bsp_ptr)
    
    def inst_bsp(self) -> int:
        bsp_ptr = self.addr + 0x04
        return memory.read_u32(bsp_ptr)