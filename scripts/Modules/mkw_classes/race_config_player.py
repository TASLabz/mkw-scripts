from dolphin import memory

from . import CharacterId, VehicleId, RaceConfigPlayerType

class RaceConfigPlayer:
    def __init__(self, addr):
        """This class has multiple instances.
           Require that the caller specify the address."""
        self.addr = addr

    def screen_id(self):
        screen_id_ref = self.addr + 0x5
        return memory.read_u8(screen_id_ref)
    
    def player_input_idx(self):
        player_input_idx_ref = self.addr + 0x6
        return memory.read_u8(player_input_idx_ref)
    
    def vehicle_id(self):
        vehicle_id_ref = self.addr + 0x8
        return VehicleId(memory.read_u32(vehicle_id_ref))
    
    def character_id(self):
        character_id_ref = self.addr + 0xC
        return CharacterId(memory.read_u32(character_id_ref))
    
    def type(self):
        type_ref = self.addr + 0x10
        return RaceConfigPlayerType(memory.read_u32(type_ref))
    
    def mii(self):
        """This struct isn't useful for populating the Mii in RKG header.
           Not all fields are populated here."""
        mii_ref = self.addr + 0x14
        return mii_ref
    
    def team(self):
        team_ref = self.addr + 0xCC
        return memory.read_u32(team_ref)
    
    def controller_id(self):
        controller_id_ref = self.addr + 0xD0
        return memory.read_u32(controller_id_ref)
    
    def previous_score(self):
        previous_score_ref = self.addr + 0xD8
        return memory.read_u16(previous_score_ref)
    
    def gp_score(self):
        gp_score_ref = self.addr + 0xDA
        return memory.read_u16(gp_score_ref)
    
    def gp_star_rank_score(self):
        gp_star_rank_score_ref = self.addr + 0xDE
        return memory.read_u16(gp_star_rank_score_ref)
    
    def gp_rank(self):
        gp_rank_ref = self.addr + 0xE0
        return memory.read_u8(gp_rank_ref)
    
    def player_order(self):
        player_order_ref = self.addr + 0xE1
        return memory.read_u8(player_order_ref)
    
    def finish_pos(self):
        finish_pos_ref = self.addr + 0xE2
        return memory.read_u8(finish_pos_ref)
    
    def rating(self):
        """This is really an 8 byte struct,
           but for our purposes we just want the actual rating."""
        rating_ref = self.addr + 0xE4 + 0x4
        return memory.read_u16(rating_ref)