from dolphin import memory

from . import KartObject, SurfaceProperties, vec3

class KartCollide:
    def __init__(self, player_idx=0, addr=None):
        self.addr = addr if addr else KartCollide.chain(player_idx)

        self.some_timer = self.inst_some_timer
        self.surface_properties = self.inst_surface_properties
        self.movement = self.inst_movement
        self.time_before_respawn = self.inst_time_before_respawn
        self.solid_oob_timer = self.inst_solid_oob_timer

    @staticmethod
    def chain(player_idx=0) -> int:
        return KartObject.kart_collide(player_idx)
    
    @staticmethod
    def some_timer(player_idx=0) -> int:
        kart_collide_ref = KartCollide.chain(player_idx)
        some_timer_ref = kart_collide_ref + 0x18
        return memory.read_u16(some_timer_ref)
    
    def inst_some_timer(self) -> int:
        some_timer_ref = self.addr + 0x18
        return memory.read_u16(some_timer_ref)
    
    @staticmethod
    def surface_properties(player_idx=0) -> SurfaceProperties:
        kart_collide_ref = KartCollide.chain(player_idx)
        surface_properties_ref = kart_collide_ref + 0x2C
        return SurfaceProperties(memory.read_u32(surface_properties_ref))
    
    def inst_surface_properties(self) -> SurfaceProperties:
        surface_properties_ref = self.addr + 0x2C
        return SurfaceProperties(memory.read_u32(surface_properties_ref))
    
    @staticmethod
    def movement(player_idx=0) -> vec3:
        kart_collide_ref = KartCollide.chain(player_idx)
        movement_ref = kart_collide_ref + 0x3C
        return vec3.read(movement_ref)
    
    def inst_movement(self) -> vec3:
        movement_ref = self.addr + 0x3C
        return vec3.read(movement_ref)
    
    @staticmethod
    def time_before_respawn(player_idx=0) -> int:
        kart_collide_ref = KartCollide.chain(player_idx)
        time_before_respawn_ref = kart_collide_ref + 0x48
        return memory.read_u16(time_before_respawn_ref)
    
    def inst_time_before_respawn(self) -> int:
        time_before_respawn_ref = self.addr + 0x48
        return memory.read_u16(time_before_respawn_ref)
    
    @staticmethod
    def solid_oob_timer(player_idx=0) -> int:
        kart_collide_ref = KartCollide.chain(player_idx)
        solid_oob_timer_ref = kart_collide_ref + 0x4A
        return memory.read_u16(solid_oob_timer_ref)
    
    def inst_solid_oob_timer(self) -> int:
        solid_oob_timer_ref = self.addr + 0x4A
        return memory.read_u16(solid_oob_timer_ref)