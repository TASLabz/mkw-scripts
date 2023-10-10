from dolphin import memory

class RaceConfigScenario:
    def __init__(self, addr):
        """This class has multiple instances.
           Require that the caller specifies the address."""
        self.addr = addr

    def player_count(self) -> int:
        player_count_ref = self.addr + 0x4
        return memory.read_u8(player_count_ref)
    
    def screen_count(self) -> int:
        screen_count_ref = self.addr + 0x5
        return memory.read_u8(screen_count_ref)
    
    def local_player_count(self) -> int:
        local_player_count_ref = self.addr + 0x6
        return memory.read_u8(local_player_count_ref)
    
    def hud_count_2(self) -> int:
        """'A better name can be found'"""
        hud_count_2_ref = self.addr + 0x7
        return memory.read_u8(hud_count_2_ref)
    
    def player(self, playerIdx=0) -> int:
        assert(0 <= playerIdx < 12)
        player_ref = self.addr + 0x8 + (playerIdx * 0xF0)
        return player_ref
    
    def settings(self) -> int:
        settings_ref = self.addr + 0xB48
        return settings_ref
    
    def competition_settings(self) -> int:
        competition_settings_ref = self.addr + 0xB7C
        return competition_settings_ref
    
    def ghost(self) -> int:
        ghost_ptr = self.addr + 0xBEC
        return memory.read_u32(ghost_ptr)