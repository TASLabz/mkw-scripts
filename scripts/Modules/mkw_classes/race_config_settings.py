from dolphin import memory
from enum import Enum

from . import CourseId, CupId

class RaceConfigEngineClass(Enum):
    _50CC = 0
    _100CC = 1
    _150CC = 2
    BATTLE = 3

class RaceConfigGameMode(Enum):
    GRAND_PRIX = 0
    VS_RACE = 1
    TIME_TRIAL = 2
    BATTLE = 3
    MISSION_TOURNAMENT = 4
    GHOST_RACE = 5
    UNKNOWN = 6
    PRIVATE_VS = 7
    PUBLIC_VS = 8
    PUBLIC_BATTLE = 9
    PRIVATE_BATTLE = 10
    AWARDS = 11
    CREDITS = 12

class RaceConfigGameType(Enum):
    GAMEPLAY_NO_INTRO = 0
    REPLAY = 1
    TITLE_ONE_PLAYER = 2  # Race loaded between cutscenes in title screen when idling
    TITLE_TWO_PLAYER = 3
    TITLE_FOUR_PLAYER = 4
    GAMEPLAY_INTRO = 5
    LIVE_VIEW = 6
    GRAND_PRIX_WIN = 7
    SOLO_VS_WIN = 8
    TEAM_VS_WIN = 9
    BATTLE_WIN = 10
    LOSS2 = 11
    LOSS = 12

class RaceConfigModeFlags(Enum):
    MIRROR = 1
    TEAMS = 2
    COMPETITION = 4

class RaceConfigSettings:
    def __init__(self, addr):
        """There are multiple instances of this class.
           Require the caller to provide the address."""
        self.addr = addr

    def course_id(self) -> CourseId:
        course_id_ref = self.addr + 0x0
        return CourseId(memory.read_u32(course_id_ref))
    
    def engine_class(self) -> RaceConfigEngineClass:
        engine_class_ref = self.addr + 0x4
        return RaceConfigEngineClass(memory.read_u32(engine_class_ref))
    
    def game_mode(self):
        game_mode_ref = self.addr + 0x8
        return RaceConfigGameMode(memory.read_u32(game_mode_ref))
    
    def camera_mode(self):
        camera_mode_ref = self.addr + 0xC
        return RaceConfigGameType(memory.read_u32(camera_mode_ref))
    
    def battle_type(self) -> int:
        battle_type_ref = self.addr + 0x10
        return memory.read_u32(battle_type_ref)
    
    def cpu_mode(self) -> int:
        cpu_mode_ref = self.addr + 0x14
        return memory.read_u32(cpu_mode_ref)
    
    def item_mode(self) -> int:
        item_mode_ref = self.addr + 0x18
        return memory.read_u32(item_mode_ref)
    
    def hud_player_ids(self) -> bytearray:
        """char[4]"""
        hud_player_ids_ref = self.addr + 0x1C
        return memory.read_bytes(hud_player_ids_ref)
    
    def cup_id(self) -> CupId:
        cup_id_ref = self.addr + 0x20
        return CupId(memory.read_u32(cup_id_ref))
    
    def race_number(self) -> int:
        race_number_ref = self.addr + 0x24
        return memory.read_u8(race_number_ref)
    
    def lap_count(self) -> int:
        """This is the total number of laps (3 for all RTs)"""
        lap_count_ref = self.addr + 0x25
        return memory.read_u8(lap_count_ref)
    
    def mode_flags(self) -> RaceConfigModeFlags:
        mode_flags_ref = self.addr + 0x28
        return RaceConfigModeFlags(memory.read_u32(mode_flags_ref))
    
    def seed_1(self) -> int:
        seed_1_ref = self.addr + 0x2C
        return memory.read_u32(seed_1_ref)
    
    def seed_2(self) -> int:
        seed_2_ref = self.addr + 0x30
        return memory.read_u32(seed_2_ref)