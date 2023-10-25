from dolphin import memory

from . import RaceManager

class TimerManager:
    def __init__(self, addr=None):
        self.addr = addr if addr else TimerManager.chain()

        self.timer = self.inst_timer
        self.race_time_ran_out = self.inst_race_time_ran_out
        self.race_has_started = self.inst_race_has_started
        self.timer_is_reversed = self.inst_timer_is_reversed
        self.race_duration_milliseconds = self.inst_race_duration_milliseconds
        self.race_frame_counter = self.inst_race_frame_counter

    @staticmethod
    def chain() -> int:
        return RaceManager.timer_manager()
    
    @staticmethod
    def timer(timer_idx=0) -> int:
        assert(0 <= timer_idx < 3)
        offset = 0x4 + (timer_idx * 0xC)
        timer_manager_ref = TimerManager.chain()
        timer_ref = timer_manager_ref + offset
        return timer_ref
    
    def inst_timer(self, timer_idx=0) -> int:
        assert(0 <= timer_idx < 3)
        offset = 0x4 + (timer_idx * 0xC)
        timer_ref = self.addr + offset
        return timer_ref
    
    @staticmethod
    def race_time_ran_out() -> bool:
        timer_manager_ref = TimerManager.chain()
        race_time_ran_out_ref = timer_manager_ref + 0x40
        return memory.read_u8(race_time_ran_out_ref) > 0
    
    def inst_race_time_ran_out(self) -> bool:
        race_time_ran_out_ref = self.addr + 0x40
        return memory.read_u8(race_time_ran_out_ref) > 0
    
    @staticmethod
    def race_has_started() -> bool:
        timer_manager_ref = TimerManager.chain()
        race_has_started_ref = timer_manager_ref + 0x41
        return memory.read_u8(race_has_started_ref) > 0
    
    def inst_race_has_started(self) -> bool:
        race_has_started_ref = self.addr + 0x41
        return memory.read_u8(race_has_started_ref) > 0
    
    @staticmethod
    def timer_is_reversed() -> bool:
        timer_manager_ref = TimerManager.chain()
        timer_is_reversed_ref = timer_manager_ref + 0x42
        return memory.read_u8(timer_is_reversed_ref) > 0
    
    def inst_timer_is_reversed(self) -> bool:
        timer_is_reversed_ref = self.addr + 0x42
        return memory.read_u8(timer_is_reversed_ref) > 0
    
    @staticmethod
    def race_duration_milliseconds() -> int:
        timer_manager_ref = TimerManager.chain()
        race_duration_milliseconds_ref = timer_manager_ref + 0x44
        return memory.read_u32(race_duration_milliseconds_ref)
    
    def inst_race_duration_milliseconds(self) -> int:
        race_duration_milliseconds_ref = self.addr + 0x44
        return memory.read_u32(race_duration_milliseconds_ref)
    
    @staticmethod
    def race_frame_counter() -> int:
        timer_manager_ref = TimerManager.chain()
        race_frame_counter_ref = timer_manager_ref + 0x48
        return memory.read_u32(race_frame_counter_ref)
    
    def inst_race_frame_counter(self) -> int:
        race_frame_counter_ref = self.addr + 0x48
        return memory.read_u32(race_frame_counter_ref)