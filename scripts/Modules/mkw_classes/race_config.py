from dolphin import memory, utils

from . import RegionError

class RaceConfig:
    def __init__(self):
        self.addr = RaceConfig.chain()

        self.race_scenario = self.inst_race_scenario
        self.menu_scenario = self.inst_menu_scenario
        self.awards_scenario = self.inst_awards_scenario
        self.ghost = self.inst_ghost

    @staticmethod
    def chain() -> int:
        id = utils.get_game_id()
        try:
            address = {"RMCE01": 0x809B8F68, "RMCP01": 0x809BD728,
                    "RMCJ01": 0x809BC788, "RMCK01": 0x809ABD68}
            return memory.read_u32(address[id])
        except KeyError:
            raise RegionError
        
    @staticmethod
    def race_scenario() -> int:
        race_config_ref = RaceConfig.chain()
        race_scenario_ref = race_config_ref + 0x20
        return race_scenario_ref
    
    def inst_race_scenario(self) -> int:
        race_scenario_ref = self.addr + 0x20
        return race_scenario_ref
    
    @staticmethod
    def menu_scenario() -> int:
        race_config_ref = RaceConfig.chain()
        menu_scenario_ref = race_config_ref + 0xC10
        return menu_scenario_ref
    
    def inst_menu_scenario(self) -> int:
        menu_scenario_ref = self.addr + 0xC10
        return menu_scenario_ref
    
    @staticmethod
    def awards_scenario() -> int:
        race_config_ref = RaceConfig.chain()
        awards_scenario_ref = race_config_ref + 0x1800
        return awards_scenario_ref
    
    def inst_awards_scenario(self) -> int:
        awards_scenario_ref = self.addr + 0x1800
        return awards_scenario_ref
    
    @staticmethod
    def ghost(ghost_idx=0) -> int:
        """The RKG file buffer"""
        assert(0 <= ghost_idx < 2)
        race_config_ref = RaceConfig.chain()
        ghost_ref = race_config_ref + 0x23F0 + (ghost_idx * 0x5000)
        return ghost_ref
    
    def inst_ghost(self, ghost_idx=0) -> int:
        assert(0 <= ghost_idx < 2)
        ghost_ref = self.addr + 0x23F0 + (ghost_idx * 0x5000)
        return ghost_ref
    