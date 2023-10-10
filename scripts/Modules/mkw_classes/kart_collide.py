from dolphin import memory

from . import KartObject, SurfaceProperties, vec3

class KartCollide:
    def __init__(self, playerIdx=0, addr=None):
        self.addr = addr if addr else KartCollide.chain(playerIdx)

        self.some_timer = self.inst_some_timer
        self.surface_properties = self.inst_surface_properties
        self.movement = self.inst_movement
        self.time_before_respawn = self.inst_time_before_reaspawn
        self.solid_oob_timer = self.inst_solid_oob_timer

    @staticmethod
    def chain(playerIdx=0) -> int:
        return KartObject.kart_collide(playerIdx)
    
    @staticmethod
    def some_timer(playerIdx=0) -> int:
        kart_collide_ref = KartCollide.chain(playerIdx)
        some_timer_ref = kart_collide_ref + 0x18
        return memory.read_u16(some_timer_ref)
    
    def inst_some_timer(self) -> int:
        some_timer_ref = self.addr + 0x18
        return memory.read_u16(some_timer_ref)
    
    @staticmethod
    def surface_properties(playerIdx=0) -> SurfaceProperties:
        kart_collide_ref = KartCollide.chain(playerIdx)
        surface_properties_ref = kart_collide_ref + 0x2C
        return SurfaceProperties(memory.read_u32(surface_properties_ref))
    
    def inst_surface_properties(self) -> SurfaceProperties:
        surface_properties_ref = self.addr + 0x2C
        return SurfaceProperties(memory.read_u32(surface_properties_ref))
    
    @staticmethod
    def movement(playerIdx=0) -> vec3:
        kart_collide_ref = KartCollide.chain(playerIdx)
        movement_ref = kart_collide_ref + 0x3C
        return vec3.read(movement_ref)
    
    def inst_movement(self) -> vec3:
        movement_ref = self.addr + 0x3C
        return vec3.read(movement_ref)
    
    @staticmethod
    def time_before_respawn(playerIdx=0) -> int:
        kart_collide_ref = KartCollide.chain(playerIdx)
        time_before_respawn_ref = kart_collide_ref + 0x48
        return memory.read_u16(time_before_respawn_ref)
    
    def inst_time_before_reaspawn(self) -> int:
        time_before_respawn_ref = self.addr + 0x48
        return memory.read_u16(time_before_respawn_ref)
    
    @staticmethod
    def solid_oob_timer(playerIdx=0) -> int:
        kart_collide_ref = KartCollide.chain(playerIdx)
        solid_oob_timer_ref = kart_collide_ref + 0x4A
        return memory.read_u16(solid_oob_timer_ref)
    
    def inst_solid_oob_timer(self) -> int:
        solid_oob_timer_ref = self.addr + 0x4A
        return memory.read_u16(solid_oob_timer_ref)