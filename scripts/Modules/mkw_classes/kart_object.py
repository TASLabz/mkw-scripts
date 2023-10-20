from dolphin import memory

from . import KartObjectManager

class KartObject:
    def __init__(self, playerIdx=0, addr=None):
        self.addr = addr if addr else KartObject.chain(playerIdx)

        self.kart_sub = self.inst_kart_sub
        self.kart_settings = self.inst_kart_settings
        self.kart_pointers = self.inst_kart_pointers
        self.kart_state = self.inst_kart_state
        self.kart_body = self.inst_kart_body
        self.kart_move = self.inst_kart_move
        self.kart_action = self.inst_kart_action
        self.kart_collide = self.inst_kart_collide
    
    @staticmethod
    def chain(playerIdx=0) -> int:
        return KartObjectManager.kart_object(playerIdx)

    @staticmethod
    def kart_sub(playerIdx=0) -> int:
        kart_obj_ref = KartObject.chain(playerIdx)
        kart_sub_ptr = kart_obj_ref + 0x10
        return memory.read_u32(kart_sub_ptr)
    
    def inst_kart_sub(self) -> int:
        kart_sub_ptr = self.addr + 0x10
        return memory.read_u32(kart_sub_ptr)

    @staticmethod
    def kart_settings(playerIdx=0) -> int:
        kart_obj_ref = KartObject.chain(playerIdx)
        kart_settings_ptr = kart_obj_ref + 0x14
        return memory.read_u32(kart_settings_ptr)
    
    def inst_kart_settings(self) -> int:
        kart_settings_ptr = self.addr + 0x14
        return memory.read_u32(kart_settings_ptr)

    @staticmethod
    def kart_pointers(playerIdx=0) -> int:
        kart_obj_ref = KartObject.chain(playerIdx)
        return kart_obj_ref + 0x1C
    
    def inst_kart_pointers(self) -> int:
        return self.addr + 0x1C

    @staticmethod
    def kart_state(playerIdx=0) -> int:
        kart_pointers_ref = KartObject.kart_pointers(playerIdx)
        kart_state_ptr = kart_pointers_ref + 0x4
        return memory.read_u32(kart_state_ptr)
    
    def inst_kart_state(self) -> int:
        kart_pointers_ref = self.kart_pointers()
        kart_state_ptr = kart_pointers_ref + 0x4
        return memory.read_u32(kart_state_ptr)
    
    @staticmethod
    def kart_body(playerIdx=0) -> int:
        kart_pointers_ref = KartObject.kart_pointers(playerIdx)
        kart_state_ptr = kart_pointers_ref + 0x8
        return memory.read_u32(kart_state_ptr)
    
    def inst_kart_body(self) -> int:
        kart_pointers_ref = self.kart_pointers()
        kart_state_ptr = kart_pointers_ref + 0x8
        return memory.read_u32(kart_state_ptr)

    @staticmethod
    def kart_move(playerIdx=0) -> int:
        kart_pointers_ref = KartObject.kart_pointers(playerIdx)
        kart_move_ptr = kart_pointers_ref + 0x28
        return memory.read_u32(kart_move_ptr)
    
    def inst_kart_move(self) -> int:
        kart_pointers_ref = self.kart_pointers()
        kart_move_ptr = kart_pointers_ref + 0x28
        return memory.read_u32(kart_move_ptr)

    @staticmethod
    def kart_action(playerIdx=0) -> int:
        kart_pointers_ref = KartObject.kart_pointers(playerIdx)
        kart_action_ptr = kart_pointers_ref + 0x2C
        return memory.read_u32(kart_action_ptr)
    
    def inst_kart_action(self) -> int:
        kart_pointers_ref = self.kart_pointers()
        kart_action_ptr = kart_pointers_ref + 0x2C
        return memory.read_u32(kart_action_ptr)
    
    @staticmethod
    def kart_collide(playerIdx=0) -> int:
        kart_pointers_ref = KartObject.kart_pointers(playerIdx)
        kart_collide_ptr = kart_pointers_ref + 0x30
        return memory.read_u32(kart_collide_ptr)
    
    def inst_kart_collide(self) -> int:
        kart_pointers_ref = self.kart_pointers()
        kart_collide_ptr = kart_pointers_ref + 0x30
        return memory.read_u32(kart_collide_ptr)