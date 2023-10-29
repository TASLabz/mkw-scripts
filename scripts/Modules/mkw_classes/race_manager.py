from dolphin import memory, utils
from enum import Enum

from . import RaceConfig, RaceConfigScenario, RegionError

class RaceState(Enum):
    INTRO_CAMERA = 0  # Course preview
    COUNTDOWN = 1  # including starting pan
    RACE = 2
    FINISHED_RACE = 3

class RaceManager:
    def __init__(self):
        self.addr = RaceManager.chain()

        self.random_1 = self.inst_random_1
        self.random_2 = self.inst_random_2
        self.race_manager_player = self.inst_race_manager_player
        self.race_mode = self.inst_race_mode
        self.timer_manager = self.inst_timer_manager
        self.player_id_in_position = self.inst_player_id_in_position
        self.finished_player_count = self.inst_finished_player_count
        self.disconnected_player_count = self.inst_disconnected_player_count
        self.intro_timer = self.inst_intro_timer
        self.timer = self.inst_timer
        self.battle_kartpoint_start = self.inst_battle_kartpoint_start
        self.state = self.inst_state
        self.intro_was_skipped = self.inst_intro_was_skipped
        self.spectator_mode = self.inst_spectator_mode
        self.can_countdown_start = self.inst_can_countdown_start
        self.cutscene_mode = self.inst_cutscene_mode
        self.lap_counting_enabled = self.inst_lap_counting_enabled
        self.water_height_check = self.inst_water_height_check
        self.disable_lower_respawns = self.inst_disable_lower_respawns

    @staticmethod
    def chain() -> int:
        id = utils.get_game_id()
        try:
            address = {"RMCE01": 0x809B8F70, "RMCP01": 0x809BD730,
                    "RMCJ01": 0x809BC790, "RMCK01": 0x809ABD70}
            return memory.read_u32(address[id])
        except KeyError:
            raise RegionError

    @staticmethod
    def random_1() -> int:
        race_manager_ref = RaceManager.chain()
        random_1_ptr = race_manager_ref + 0x4
        return memory.read_u32(random_1_ptr)
    
    def inst_random_1(self) -> int:
        random_1_ptr = self.addr + 0x4
        return memory.read_u32(random_1_ptr)
    
    @staticmethod
    def random_2() -> int:
        race_manager_ref = RaceManager.chain()
        random_2_ptr = race_manager_ref + 0x8
        return memory.read_u32(random_2_ptr)
    
    def inst_random_2(self) -> int:
        random_2_ptr = self.addr + 0x8
        return memory.read_u32(random_2_ptr)
    
    @staticmethod
    def race_manager_player(player_idx=0) -> int:
        # Assert player_idx is within the number of current players
        race_scenario_ref = RaceConfigScenario(RaceConfig.race_scenario())
        assert(0 <= player_idx < race_scenario_ref.player_count())

        race_manager_ref = RaceManager.chain()
        player_array = race_manager_ref + 0xC
        player_ptr = memory.read_u32(player_array) + (player_idx * 0x4)
        return memory.read_u32(player_ptr)
    
    def inst_race_manager_player(self, player_idx=0) -> int:
        # Assert player_idx is within the number of current players
        race_scenario_ref = RaceConfigScenario(RaceConfig.race_scenario())
        assert(0 <= player_idx < race_scenario_ref.player_count())

        player_array = self.addr + 0xC
        player_ptr = memory.read_u32(player_array) + (player_idx * 0x4)
        return memory.read_u32(player_ptr)
    
    @staticmethod
    def race_mode() -> int:
        race_manager_ref = RaceManager.chain()
        race_mode_ptr = race_manager_ref + 0x10
        return memory.read_u32(race_mode_ptr)
    
    def inst_race_mode(self) -> int:
        race_mode_ptr = self.addr + 0x10
        return memory.read_u32(race_mode_ptr)
    
    @staticmethod
    def timer_manager() -> int:
        race_manager_ref = RaceManager.chain()
        timer_manager_ptr = race_manager_ref + 0x14
        return memory.read_u32(timer_manager_ptr)
    
    def inst_timer_manager(self) -> int:
        timer_manager_ptr = self.addr + 0x14
        return memory.read_u32(timer_manager_ptr)
    
    @staticmethod
    def player_id_in_position(position=0) -> int:
        # Assert player_idx is within the number of current players
        race_scenario_ref = RaceConfigScenario(RaceConfig.race_scenario())
        assert(0 <= position < race_scenario_ref.player_count())

        race_manager_ref = RaceManager.chain()
        player_id_position_ptr = race_manager_ref + 0x18
        player_id_position_ref = memory.read_u32(player_id_position_ptr) + position
        return memory.read_u8(player_id_position_ref)
    
    def inst_player_id_in_position(self, position=0) -> int:
        # Assert player_idx is within the number of current players
        race_scenario_ref = RaceConfigScenario(RaceConfig.race_scenario())
        assert(0 <= position < race_scenario_ref.player_count())

        player_id_position_ptr = self.addr + 0x18
        player_id_position_ref = memory.read_u32(player_id_position_ptr) + position
        return memory.read_u8(player_id_position_ref)
    
    @staticmethod
    def finished_player_count() -> int:
        race_manager_ref = RaceManager.chain()
        finished_player_count_ref = race_manager_ref + 0x1C
        return memory.read_u8(finished_player_count_ref)
    
    def inst_finished_player_count(self) -> int:
        finished_player_count_ref = self.addr + 0x1C
        return memory.read_u8(finished_player_count_ref)
    
    @staticmethod
    def disconnected_player_count() -> int:
        race_manager_ref = RaceManager.chain()
        disconnected_player_count_ref = race_manager_ref + 0x1D
        return memory.read_u8(disconnected_player_count_ref)
    
    def inst_disconnected_player_count(self) -> int:
        disconnected_player_count_ref = self.addr + 0x1D
        return memory.read_u8(disconnected_player_count_ref)
    
    @staticmethod
    def intro_timer() -> int:
        """Begins counting frames immediately when entering a race"""
        race_manager_ref = RaceManager.chain()
        intro_timer_ref = race_manager_ref + 0x1E
        return memory.read_u16(intro_timer_ref)
    
    def inst_intro_timer(self) -> int:
        """Begins counting frames immediately when entering a race"""
        intro_timer_ref = self.addr + 0x1E
        return memory.read_u16(intro_timer_ref)
    
    @staticmethod
    def timer() -> int:
        """Begins counting frames when race countdown starts"""
        race_manager_ref = RaceManager.chain()
        timer_ref = race_manager_ref + 0x20
        return memory.read_u16(timer_ref)
    
    def inst_timer(self) -> int:
        """Begins counting frames when race countdown starts"""
        timer_ref = self.addr + 0x20
        return memory.read_u16(timer_ref)
    
    @staticmethod
    def battle_kartpoint_start() -> int:
        race_manager_ref = RaceManager.chain()
        battle_kartpoint_start_ref = race_manager_ref + 0x24
        return memory.read_u8(battle_kartpoint_start_ref)
    
    def inst_battle_kartpoint_start(self) -> int:
        battle_kartpoint_start_ref = self.addr + 0x24
        return memory.read_u8(battle_kartpoint_start_ref)
    
    @staticmethod
    def state() -> RaceState:
        race_manager_ref = RaceManager.chain()
        state_ref = race_manager_ref + 0x28
        return RaceState(memory.read_u32(state_ref))
    
    def inst_state(self) -> RaceState:
        state_ref = self.addr + 0x28
        return RaceState(memory.read_u32(state_ref))
    
    @staticmethod
    def intro_was_skipped() -> bool:
        race_manager_ref = RaceManager.chain()
        intro_was_skipped_ref = race_manager_ref + 0x2C
        return memory.read_u8(intro_was_skipped_ref) > 0
    
    def inst_intro_was_skipped(self) -> bool:
        intro_was_skipped_ref = self.addr + 0x2C
        return memory.read_u8(intro_was_skipped_ref) > 0
    
    @staticmethod
    def spectator_mode() -> bool:
        race_manager_ref = RaceManager.chain()
        spectator_mode_ref = race_manager_ref + 0x2D
        return memory.read_u8(spectator_mode_ref) > 0
    
    def inst_spectator_mode(self) -> bool:
        spectator_mode_ref = self.addr + 0x2D
        return memory.read_u8(spectator_mode_ref) > 0
    
    @staticmethod
    def can_countdown_start() -> bool:
        race_manager_ref = RaceManager.chain()
        can_countdown_start_ref = race_manager_ref + 0x2E
        return memory.read_u8(can_countdown_start_ref) > 0
    
    def inst_can_countdown_start(self) -> bool:
        can_countdown_start_ref = self.addr + 0x2E
        return memory.read_u8(can_countdown_start_ref) > 0
    
    @staticmethod
    def cutscene_mode() -> bool:
        race_manager_ref = RaceManager.chain()
        cutscene_mode_ref = race_manager_ref + 0x2F
        return memory.read_u8(cutscene_mode_ref) > 0
    
    def inst_cutscene_mode(self) -> bool:
        cutscene_mode_ref = self.addr + 0x2F
        return memory.read_u8(cutscene_mode_ref) > 0
    
    @staticmethod
    def lap_counting_enabled() -> bool:
        race_manager_ref = RaceManager.chain()
        lap_counting_enabled_ref = race_manager_ref + 0x30
        return memory.read_u8(lap_counting_enabled_ref) > 0
    
    def inst_lap_counting_enabled(self) -> bool:
        lap_counting_enabled_ref = self.addr + 0x30
        return memory.read_u8(lap_counting_enabled_ref) > 0
    
    # Skipping implementation of the following classes:
    # MovingMask - related to slipstreams possibly?
    # RaceMinigameParam - related to battle mode
    # ElinControlManager - I couldn't tell you

    @staticmethod
    def water_height_check() -> float:
        race_manager_ref = RaceManager.chain()
        water_height_check_ref = race_manager_ref + 0x44
        return memory.read_f32(water_height_check_ref)
    
    def inst_water_height_check(self) -> float:
        water_height_check_ref = self.addr + 0x44
        return memory.read_f32(water_height_check_ref)
    
    @staticmethod
    def disable_lower_respawns() -> bool:
        """Delfino Plaza?"""
        race_manager_ref = RaceManager.chain()
        disable_lower_respawns_ref = race_manager_ref + 0x48
        return memory.read_u8(disable_lower_respawns_ref) > 0
    
    def inst_disable_lower_respawns(self) -> bool:
        """Delfino Plaza?"""
        disable_lower_respawns_ref = self.addr + 0x48
        return memory.read_u8(disable_lower_respawns_ref) > 0