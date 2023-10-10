from dolphin import memory

from . import KartSettings

class GpStats:
    def __init__(self, playerIdx=0, addr=None):
        self.addr = addr if addr else GpStats.chain(playerIdx)

        self.addr = GpStats.chain(playerIdx)

        self.start_boost_successful = self.inst_start_boost_successful
        self.mts = self.inst_mts
        self.offroad = self.inst_offroad
        self.object_collision = self.inst_object_collision

    @staticmethod
    def chain(playerIdx=0) -> int:
        return KartSettings.gp_stats(playerIdx)
    
    @staticmethod
    def start_boost_successful(playerIdx=0) -> bool:
        gp_stats_ref = GpStats.chain(playerIdx)
        start_boost_successful_ref = gp_stats_ref + 0x0
        return memory.read_u8(start_boost_successful_ref) > 0
    
    def inst_start_boost_successful(self) -> bool:
        start_boost_successful_ref = self.addr + 0x0
        return memory.read_u8(start_boost_successful_ref) > 0
    
    @staticmethod
    def mts(playerIdx=0) -> int:
        gp_stats_ref = GpStats.chain(playerIdx)
        mts_ref = gp_stats_ref + 0x4
        return memory.read_u32(mts_ref)
    
    def inst_mts(self) -> int:
        mts_ref = self.addr + 0x4
        return memory.read_u32(mts_ref)
    
    @staticmethod
    def offroad(playerIdx=0) -> int:
        gp_stats_ref = GpStats.chain(playerIdx)
        offroad_ref = gp_stats_ref + 0x8
        return memory.read_u32(offroad_ref)
    
    def inst_offroad(self) -> int:
        offroad_ref = self.addr + 0x8
        return memory.read_u32(offroad_ref)
    
    @staticmethod
    def object_collision(playerIdx=0) -> int:
        gp_stats_ref = GpStats.chain(playerIdx)
        object_collision_ref = gp_stats_ref + 0x10
        return memory.read_u32(object_collision_ref)
    
    def inst_object_collision(self) -> int:
        object_collision_ref = self.addr + 0x10
        return memory.read_u32(object_collision_ref)
    
    @staticmethod
    def oob(playerIdx=0) -> int:
        gp_stats_ref = GpStats.chain(playerIdx)
        oob_ref = gp_stats_ref + 0x14
        return memory.read_u32(oob_ref)
    
    def inst_oob(self) -> int:
        oob_ref = self.addr + 0x14
        return memory.read_u32(oob_ref)