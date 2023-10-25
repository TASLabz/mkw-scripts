from dolphin import memory

from . import KartSettings

class GpStats:
    def __init__(self, player_idx=0, addr=None):
        self.addr = addr if addr else GpStats.chain(player_idx)

        self.addr = GpStats.chain(player_idx)

        self.start_boost_successful = self.inst_start_boost_successful
        self.mts = self.inst_mts
        self.offroad = self.inst_offroad
        self.object_collision = self.inst_object_collision

    @staticmethod
    def chain(player_idx=0) -> int:
        return KartSettings.gp_stats(player_idx)
    
    @staticmethod
    def start_boost_successful(player_idx=0) -> bool:
        gp_stats_ref = GpStats.chain(player_idx)
        start_boost_successful_ref = gp_stats_ref + 0x0
        return memory.read_u8(start_boost_successful_ref) > 0
    
    def inst_start_boost_successful(self) -> bool:
        start_boost_successful_ref = self.addr + 0x0
        return memory.read_u8(start_boost_successful_ref) > 0
    
    @staticmethod
    def mts(player_idx=0) -> int:
        gp_stats_ref = GpStats.chain(player_idx)
        mts_ref = gp_stats_ref + 0x4
        return memory.read_u32(mts_ref)
    
    def inst_mts(self) -> int:
        mts_ref = self.addr + 0x4
        return memory.read_u32(mts_ref)
    
    @staticmethod
    def offroad(player_idx=0) -> int:
        gp_stats_ref = GpStats.chain(player_idx)
        offroad_ref = gp_stats_ref + 0x8
        return memory.read_u32(offroad_ref)
    
    def inst_offroad(self) -> int:
        offroad_ref = self.addr + 0x8
        return memory.read_u32(offroad_ref)
    
    @staticmethod
    def object_collision(player_idx=0) -> int:
        gp_stats_ref = GpStats.chain(player_idx)
        object_collision_ref = gp_stats_ref + 0x10
        return memory.read_u32(object_collision_ref)
    
    def inst_object_collision(self) -> int:
        object_collision_ref = self.addr + 0x10
        return memory.read_u32(object_collision_ref)
    
    @staticmethod
    def oob(player_idx=0) -> int:
        gp_stats_ref = GpStats.chain(player_idx)
        oob_ref = gp_stats_ref + 0x14
        return memory.read_u32(oob_ref)
    
    def inst_oob(self) -> int:
        oob_ref = self.addr + 0x14
        return memory.read_u32(oob_ref)