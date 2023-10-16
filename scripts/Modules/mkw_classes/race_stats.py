from dolphin import memory

from . import KartSettings

class RaceStats:
    def __init__(self, playerIdx=0, addr=None):
        self.addr = addr if addr else RaceStats.chain(playerIdx)

        self.duration_in_first = self.inst_duration_in_first
        self.hit_other_count = self.inst_hit_other_count
        self.got_hit_count = self.inst_got_hit_count
        self.trick_count = self.inst_trick_count

    @staticmethod
    def chain(playerIdx=0) -> int:
        return KartSettings.race_stats(playerIdx)
    
    @staticmethod
    def duration_in_first(playerIdx=0) -> float:
        race_stats_ref = RaceStats.chain(playerIdx)
        duration_in_first_ref = race_stats_ref + 0x4
        return memory.read_f32(duration_in_first_ref)
    
    def inst_duration_in_first(self) -> float:
        duration_in_first_ref = self.addr + 0x4
        return memory.read_f32(duration_in_first_ref)
    
    @staticmethod
    def hit_other_count(playerIdx=0) -> int:
        race_stats_ref = RaceStats.chain(playerIdx)
        hit_other_count_ref = race_stats_ref + 0x8
        return memory.read_u32(hit_other_count_ref)
    
    def inst_hit_other_count(self) -> int:
        hit_other_count_ref = self.addr + 0x8
        return memory.read_u32(hit_other_count_ref)
    
    @staticmethod
    def got_hit_count(playerIdx=0) -> int:
        race_stats_ref = RaceStats.chain(playerIdx)
        got_hit_count_ref = race_stats_ref + 0xC
        return memory.read_u32(got_hit_count_ref)
    
    def inst_got_hit_count(self) -> int:
        got_hit_count_ref = self.addr + 0xC
        return memory.read_u32(got_hit_count_ref)
    
    @staticmethod
    def trick_count(playerIdx=0) -> int:
        race_stats_ref = RaceStats.chain(playerIdx)
        trick_count_ref = race_stats_ref + 0x10
        return memory.read_u32(trick_count_ref)
    
    def inst_trick_count(self) -> int:
        trick_count_ref = self.addr + 0x10
        return memory.read_u32(trick_count_ref)