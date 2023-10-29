from dolphin import memory, utils

from . import RegionError

class InputMgr:
    def __init__(self):
        self.addr = InputMgr.chain()

        self.player_input = self.inst_player_input
        self.ai_kart_input = self.inst_ai_kart_input
        self.master_input = self.inst_master_input
        self.dummy_controller = self.inst_dummy_controller
        self.wii_controller = self.inst_wii_controller
        self.gc_controller = self.inst_gc_controller
        self.ghost_controller = self.inst_ghost_controller
        self.rumble_settings = self.inst_rumble_settings
        self.pad_status = self.inst_pad_status
        self.is_paused = self.inst_is_paused
        self.is_mirror = self.inst_is_mirror

    @staticmethod
    def chain() -> int:
        id = utils.get_game_id()
        try:
            address = {"RMCE01": 0x809B8F4C, "RMCP01": 0x809BD70C,
                    "RMCJ01": 0x809BC76C, "RMCK01": 0x809ABD4C}
            return memory.read_u32(address[id])
        except KeyError:
            raise RegionError

    @staticmethod
    def player_input(player_idx=0) -> int:
        assert(0 <= player_idx < 4)
        input_mgr_ref = InputMgr.chain()
        player_input_ref = input_mgr_ref + 0x4 + (player_idx * 0xEC)
        return player_input_ref
    
    def inst_player_input(self, player_idx=0) -> int:
        assert(0 <= player_idx < 4)
        player_input_ref = self.addr + 0x4 + (player_idx * 0xEC)
        return player_input_ref
    
    @staticmethod
    def ai_kart_input(kart_idx=0) -> int:
        assert(0 <= kart_idx < 12)
        input_mgr_ref = InputMgr.chain()
        player_input_ref = input_mgr_ref + 0x3B4 + (kart_idx * 0x180)
        return player_input_ref
    
    def inst_ai_kart_input(self, kart_idx=0) -> int:
        assert(0 <= kart_idx < 12)
        player_input_ref = self.addr + 0x3B4 + (kart_idx * 0x180)
        return player_input_ref
    
    @staticmethod
    def master_input() -> int:
        input_mgr_ref = InputMgr.chain()
        master_input_ref = input_mgr_ref + 0x15B4
        return master_input_ref
    
    def inst_master_input(self) -> int:
        master_input_ref = self.addr + 0x15B4
        return master_input_ref
    
    @staticmethod
    def dummy_controller() -> int:
        input_mgr_ref = InputMgr.chain()
        dummy_controller_ref = input_mgr_ref + 0x1690
        return dummy_controller_ref
    
    def inst_dummy_controller(self) -> int:
        dummy_controller_ref = self.addr + 0x1690
        return dummy_controller_ref
    
    @staticmethod
    def wii_controller(controller_idx=0) -> int:
        assert(0 <= controller_idx < 4)
        input_mgr_ref = InputMgr.chain()
        wii_controller_ref = input_mgr_ref + 0x1720 + (controller_idx * 0x920)
        return wii_controller_ref
    
    def inst_wii_controller(self, controller_idx=0) -> int:
        assert(0 <= controller_idx < 4)
        wii_controller_ref = self.addr + 0x1720 + (controller_idx * 0x920)
        return wii_controller_ref
    
    @staticmethod
    def gc_controller(controller_idx=0) -> int:
        assert(0 <= controller_idx < 4)
        input_mgr_ref = InputMgr.chain()
        gc_controller_ref = input_mgr_ref + 0x3BA0 + (controller_idx * 0xB0)
        return gc_controller_ref
    
    def inst_gc_controller(self, controller_idx=0) -> int:
        assert(0 <= controller_idx < 4)
        gc_controller_ref = self.addr + 0x3BA0 + (controller_idx * 0xB0)
        return gc_controller_ref
    
    @staticmethod
    def ghost_controller(controller_idx=0) -> int:
        assert(0 <= controller_idx < 4)
        input_mgr_ref = InputMgr.chain()
        ghost_controller_ref = input_mgr_ref + 0x3E60 + (controller_idx * 0xA8)
        return ghost_controller_ref
    
    def inst_ghost_controller(self, controller_idx=0) -> int:
        assert(0 <= controller_idx < 4)
        ghost_controller_ref = self.addr + 0x3E60 + (controller_idx * 0xA8)
        return ghost_controller_ref
    
    @staticmethod
    def rumble_settings() -> int:
        input_mgr_ref = InputMgr.chain()
        rumble_settings_ref = input_mgr_ref + 0x4100
        return rumble_settings_ref
    
    def inst_rumble_settings(self) -> int:
        rumble_settings_ref = self.addr + 0x4100
        return rumble_settings_ref
    
    @staticmethod
    def pad_status(pad_idx=0) -> int:
        input_mgr_ref = InputMgr.chain()
        pad_status_ref = input_mgr_ref + 0x4120 + (pad_idx * 0xC)
        return pad_status_ref
    
    def inst_pad_status(self, pad_idx=0) -> int:
        pad_status_ref = self.addr + 0x4120 + (pad_idx * 0xC)
        return pad_status_ref
    
    @staticmethod
    def is_paused() -> bool:
        input_mgr_ref = InputMgr.chain()
        is_paused_ref = input_mgr_ref + 0x4154
        return memory.read_u8(is_paused_ref) > 0
    
    def inst_is_paused(self) -> bool:
        is_paused_ref = self.addr + 0x4154
        return memory.read_u8(is_paused_ref) > 0
    
    @staticmethod
    def is_mirror() -> bool:
        input_mgr_ref = InputMgr.chain()
        is_mirror_ref = input_mgr_ref + 0x4155
        return memory.read_u8(is_mirror_ref) > 0
    
    def inst_is_mirror(self) -> bool:
        is_mirror_ref = self.addr + 0x4155
        return memory.read_u8(is_mirror_ref) > 0
    
    # TODO: Implement WiiController, GcController