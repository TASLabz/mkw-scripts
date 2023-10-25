from dolphin import memory
from enum import Enum

from . import Timer, RaceManager

class RaceInfoPlayerFlags(Enum):
    IN_RACE = 1
    FINISHED = 2
    DRIVING_WRONG_WAY = 4
    FINISHED_REMOTE = 8
    DISCONNECTED = 16
    STOPPED = 32
    COMING_LAST_ANIMATION = 64

class RaceManagerPlayer:
    def __init__(self, player_idx=0, addr=None):
        self.addr = addr if addr else RaceManagerPlayer.chain(player_idx)

        self.idx = self.inst_idx
        self.checkpoint_id = self.inst_checkpoint_id
        self.race_completion = self.inst_race_completion
        self.race_completion_max = self.inst_race_completion_max
        self.checkpoint_factor = self.inst_checkpoint_factor
        self.checkpoint_start_lap_completion = self.inst_checkpoint_start_lap_completion
        self.lap_completion = self.inst_lap_completion
        self.position = self.inst_position
        self.respawn = self.inst_respawn
        self.battle_score = self.inst_battle_score
        self.current_lap = self.inst_current_lap
        self.max_lap = self.inst_max_lap
        self.current_kcp = self.inst_current_kcp
        self.max_kcp = self.inst_max_kcp
        self.frame_counter = self.inst_frame_counter
        self.frames_in_first = self.inst_frames_in_first
        self.flags = self.inst_flags
        self.lap_finish_time = self.inst_lap_finish_time
        self.race_finish_time = self.inst_race_finish_time
        self.kart_input = self.inst_kart_input
        self.players_ahead_flags = self.inst_players_ahead_flags
        self.finishing_position = self.inst_finishing_position

    @staticmethod
    def chain(player_idx=0) -> int:
        return RaceManager.race_manager_player(player_idx)
    
    @staticmethod
    def idx(player_idx=0) -> int:
        race_manager_player_ref = RaceManagerPlayer.chain(player_idx)
        idx_ref = race_manager_player_ref + 0x8
        return memory.read_u8(idx_ref)
    
    def inst_idx(self) -> int:
        idx_ref = self.addr + 0x8
        return memory.read_u8(idx_ref)
    
    @staticmethod
    def checkpoint_id(player_idx=0) -> int:
        race_manager_player_ref = RaceManagerPlayer.chain(player_idx)
        checkpoint_id_ref = race_manager_player_ref + 0xA
        return memory.read_u16(checkpoint_id_ref)
    
    def inst_checkpoint_id(self) -> int:
        checkpoint_id_ref = self.addr + 0xA
        return memory.read_u16(checkpoint_id_ref)
    
    @staticmethod
    def race_completion(player_idx=0) -> float:
        race_manager_player_ref = RaceManagerPlayer.chain(player_idx)
        race_completion_ref = race_manager_player_ref + 0xC
        return memory.read_f32(race_completion_ref)
    
    def inst_race_completion(self) -> float:
        race_completion_ref = self.addr + 0xC
        return memory.read_f32(race_completion_ref)
    
    @staticmethod
    def race_completion_max(player_idx=0) -> float:
        race_manager_player_ref = RaceManagerPlayer.chain(player_idx)
        race_completion_max_ref = race_manager_player_ref + 0x10
        return memory.read_f32(race_completion_max_ref)
    
    def inst_race_completion_max(self) -> float:
        race_completion_max_ref = self.addr + 0x10
        return memory.read_f32(race_completion_max_ref)
    
    @staticmethod
    def checkpoint_factor(player_idx=0) -> float:
        race_manager_player_ref = RaceManagerPlayer.chain(player_idx)
        checkpoint_factor_ref = race_manager_player_ref + 0x14
        return memory.read_f32(checkpoint_factor_ref)
    
    def inst_checkpoint_factor(self) -> float:
        checkpoint_factor_ref = self.addr + 0x14
        return memory.read_f32(checkpoint_factor_ref)
    
    @staticmethod
    def checkpoint_start_lap_completion(player_idx=0) -> float:
        race_manager_player_ref = RaceManagerPlayer.chain(player_idx)
        checkpoint_start_lap_completion_ref = race_manager_player_ref + 0x18
        return memory.read_f32(checkpoint_start_lap_completion_ref)
    
    def inst_checkpoint_start_lap_completion(self) -> float:
        checkpoint_start_lap_completion_ref = self.addr + 0x18
        return memory.read_f32(checkpoint_start_lap_completion_ref)
    
    @staticmethod
    def lap_completion(player_idx=0) -> float:
        race_manager_player_ref = RaceManagerPlayer.chain(player_idx)
        lap_completion_ref = race_manager_player_ref + 0x1C
        return memory.read_f32(lap_completion_ref)
    
    def inst_lap_completion(self) -> float:
        lap_completion_ref = self.addr + 0x1C
        return memory.read_f32(lap_completion_ref)
    
    @staticmethod
    def position(player_idx=0) -> int:
        race_manager_player_ref = RaceManagerPlayer.chain(player_idx)
        position_ref = race_manager_player_ref + 0x20
        return memory.read_u8(position_ref)
    
    def inst_position(self) -> int:
        position_ref = self.addr + 0x20
        return memory.read_u8(position_ref)
    
    @staticmethod
    def respawn(player_idx=0) -> int:
        race_manager_player_ref = RaceManagerPlayer.chain(player_idx)
        respawn_ref = race_manager_player_ref + 0x21
        return memory.read_u8(respawn_ref)
    
    def inst_respawn(self) -> int:
        respawn_ref = self.addr + 0x21
        return memory.read_u8(respawn_ref)
    
    @staticmethod
    def battle_score(player_idx=0) -> int:
        race_manager_player_ref = RaceManagerPlayer.chain(player_idx)
        battle_score_ref = race_manager_player_ref + 0x22
        return memory.read_u16(battle_score_ref)
    
    def inst_battle_score(self) -> int:
        battle_score_ref = self.addr + 0x22
        return memory.read_u16(battle_score_ref)
    
    @staticmethod
    def current_lap(player_idx=0) -> int:
        race_manager_player_ref = RaceManagerPlayer.chain(player_idx)
        current_lap_ref = race_manager_player_ref + 0x24
        return memory.read_u16(current_lap_ref)
    
    def inst_current_lap(self) -> int:
        current_lap_ref = self.addr + 0x24
        return memory.read_u16(current_lap_ref)
    
    @staticmethod
    def max_lap(player_idx=0) -> int:
        race_manager_player_ref = RaceManagerPlayer.chain(player_idx)
        max_lap_ref = race_manager_player_ref + 0x26
        return memory.read_u8(max_lap_ref)
    
    def inst_max_lap(self) -> int:
        max_lap_ref = self.addr + 0x26
        return memory.read_u8(max_lap_ref)
    
    @staticmethod
    def current_kcp(player_idx=0) -> int:
        race_manager_player_ref = RaceManagerPlayer.chain(player_idx)
        current_kcp_ref = race_manager_player_ref + 0x27
        return memory.read_u8(current_kcp_ref)
    
    def inst_current_kcp(self) -> int:
        current_kcp_ref = self.addr + 0x27
        return memory.read_u8(current_kcp_ref)
    
    @staticmethod
    def max_kcp(player_idx=0) -> int:
        race_manager_player_ref = RaceManagerPlayer.chain(player_idx)
        max_kcp_ref = race_manager_player_ref + 0x28
        return memory.read_u8(max_kcp_ref)
    
    def inst_max_kcp(self) -> int:
        max_kcp_ref = self.addr + 0x28
        return memory.read_u8(max_kcp_ref)
    
    @staticmethod
    def frame_counter(player_idx=0) -> int:
        race_manager_player_ref = RaceManagerPlayer.chain(player_idx)
        frame_counter_ref = race_manager_player_ref + 0x2C
        return memory.read_u32(frame_counter_ref)
    
    def inst_frame_counter(self) -> int:
        frame_counter_ref = self.addr + 0x2C
        return memory.read_u32(frame_counter_ref)
    
    @staticmethod
    def frames_in_first(player_idx=0) -> int:
        """Number of frames the player is in first place.
           This is probably only useful for GP Mode?"""
        race_manager_player_ref = RaceManagerPlayer.chain(player_idx)
        frames_in_first_ref = race_manager_player_ref + 0x30
        return memory.read_u32(frames_in_first_ref)
    
    def inst_frames_in_first(self) -> int:
        """Number of frames the player is in first place.
           This is probably only useful for GP Mode?"""
        frames_in_first_ref = self.addr + 0x30
        return memory.read_u32(frames_in_first_ref)
    
    @staticmethod
    def flags(player_idx=0) -> RaceInfoPlayerFlags:
        race_manager_player_ref = RaceManagerPlayer.chain(player_idx)
        frames_in_first_ref = race_manager_player_ref + 0x38
        return RaceInfoPlayerFlags(memory.read_u32(frames_in_first_ref))
    
    def inst_flags(self) -> RaceInfoPlayerFlags:
        frames_in_first_ref = self.addr + 0x38
        return RaceInfoPlayerFlags(memory.read_u32(frames_in_first_ref))
    
    @staticmethod
    def lap_finish_time(player_idx=0, lap=0) -> Timer:
        """Accesses the array of Timer objects indexed based on lap count.
           It's hard-coded to always be 3 laps.
           NOTE: This is the sum of all previous laps
           (i.e. lap 2 timer = lap 1 + lap 2 time)"""
        assert(0 <= lap < 3)
        race_manager_player_ref = RaceManagerPlayer.chain(player_idx)
        lap_finish_time_ptr = race_manager_player_ref + 0x3C
        lap_finish_time_ref = memory.read_u32(lap_finish_time_ptr) + (lap * 0xC)
        return Timer(lap_finish_time_ref)
    
    def inst_lap_finish_time(self, lap=0) -> Timer:
        """Accesses the array of Timer objects indexed based on lap count.
           It's hard-coded to always be 3 laps.
           NOTE: This is the sum of all previous laps
           (i.e. lap 2 timer = lap 1 + lap 2 time)"""
        assert(0 <= lap < 3)
        lap_finish_time_ptr = self.addr + 0x3C
        lap_finish_time_ref = memory.read_u32(lap_finish_time_ptr) + (lap * 0xC)
        return Timer(lap_finish_time_ref)
    
    @staticmethod
    def race_finish_time(player_idx=0) -> Timer:
        race_manager_player_ref = RaceManagerPlayer.chain(player_idx)
        race_finish_time_ptr = race_manager_player_ref + 0x40
        race_finish_time_ref = memory.read_u32(race_finish_time_ptr)
        return Timer(race_finish_time_ref)
    
    def inst_race_finish_time(self) -> Timer:
        race_finish_time_ptr = self.addr + 0x40
        race_finish_time_ref = memory.read_u32(race_finish_time_ptr)
        return Timer(race_finish_time_ref)
    
    @staticmethod
    def kart_input(player_idx=0) -> int:
        race_manager_player_ref = RaceManagerPlayer.chain(player_idx)
        kart_input_ptr = race_manager_player_ref + 0x48
        return memory.read_u32(kart_input_ptr)
    
    def inst_kart_input(self) -> int:
        kart_input_ptr = self.addr + 0x48
        return memory.read_u32(kart_input_ptr)
    
    @staticmethod
    def players_ahead_flags(player_idx=0) -> int:
        race_manager_player_ref = RaceManagerPlayer.chain(player_idx)
        players_ahead_flags_ptr = race_manager_player_ref + 0x50
        return memory.read_u16(players_ahead_flags_ptr)
    
    def inst_players_ahead_flags(self) -> int:
        players_ahead_flags_ptr = self.addr + 0x50
        return memory.read_u16(players_ahead_flags_ptr)
    
    @staticmethod
    def finishing_position(player_idx=0) -> int:
        race_manager_player_ref = RaceManagerPlayer.chain(player_idx)
        finishing_position_ptr = race_manager_player_ref + 0x53
        return memory.read_u8(finishing_position_ptr)
    
    def inst_finishing_position(self) -> int:
        finishing_position_ptr = self.addr + 0x53
        return memory.read_u8(finishing_position_ptr)