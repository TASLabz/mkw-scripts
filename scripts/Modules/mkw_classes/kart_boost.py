from dolphin import memory
from enum import Enum

from . import KartMove

class BoostType(Enum):
    ALL_MT = 0x1
    MUSHROOM_AND_BOOST_PANEL = 0x4
    TRICK_AND_ZIPPER = 0x10

class KartBoost:
    def __init__(self, player_idx=0, addr=None):
        self.addr = addr if addr else KartBoost.chain(player_idx)

        self.all_mt_timer = self.inst_all_mt_timer
        self.mushroom_and_boost_panel_timer = self.inst_mushroom_and_boost_panel_timer
        self.trick_and_zipper_timer = self.inst_trick_and_zipper_timer
        self.boost_type = self.inst_boost_type
        self.boost_multiplier = self.inst_boost_multiplier
        self.boost_acceleration = self.inst_boost_acceleration
        self.boost_speed_limit = self.inst_boost_speed_limit

    @staticmethod
    def chain(player_idx=0) -> int:
        return KartMove.kart_boost(player_idx)
    
    @staticmethod
    def all_mt_timer(player_idx=0) -> int:
        """This is a decrementing frame counter for the remaining
           duration of start boosts, mini-turbos, and stand-still mini-turbos."""
        kart_boost_ref = KartBoost.chain(player_idx)
        all_mt_timer_ref = kart_boost_ref + 0x4
        return memory.read_u16(all_mt_timer_ref)
    
    def inst_all_mt_timer(self) -> int:
        """This is a decrementing frame counter for the remaining
           duration of start boosts, mini-turbos, and stand-still mini-turbos."""
        all_mt_timer_ref = self.addr + 0x4
        return memory.read_u16(all_mt_timer_ref)
    
    @staticmethod
    def mushroom_and_boost_panel_timer(player_idx=0) -> int:
        kart_boost_ref = KartBoost.chain(player_idx)
        mushroom_and_boost_panel_timer_ref = kart_boost_ref + 0x8
        return memory.read_u16(mushroom_and_boost_panel_timer_ref)
    
    def inst_mushroom_and_boost_panel_timer(self) -> int:
        mushroom_and_boost_panel_timer_ref = self.addr + 0x8
        return memory.read_u16(mushroom_and_boost_panel_timer_ref)
    
    @staticmethod
    def trick_and_zipper_timer(player_idx=0) -> int:
        kart_boost_ref = KartBoost.chain(player_idx)
        trick_and_zipper_timer_ref = kart_boost_ref + 0xC
        return memory.read_u16(trick_and_zipper_timer_ref)
    
    def inst_trick_and_zipper_timer(self) -> int:
        trick_and_zipper_timer_ref = self.addr + 0xC
        return memory.read_u16(trick_and_zipper_timer_ref)
    
    @staticmethod
    def boost_type(player_idx=0) -> BoostType:
        kart_boost_ref = KartBoost.chain(player_idx)
        boost_type_ref = kart_boost_ref + 0x10
        return memory.read_u16(boost_type_ref)
    
    def inst_boost_type(self) -> BoostType:
        boost_type_ref = self.addr + 0x10
        return memory.read_u16(boost_type_ref)
    
    @staticmethod
    def boost_multiplier(player_idx=0) -> float:
        kart_boost_ref = KartBoost.chain(player_idx)
        boost_multiplier_ref = kart_boost_ref + 0x14
        return memory.read_f32(boost_multiplier_ref)
    
    def inst_boost_multiplier(self) -> float:
        boost_multiplier_ref = self.addr + 0x14
        return memory.read_f32(boost_multiplier_ref)
    
    @staticmethod
    def boost_acceleration(player_idx=0) -> float:
        kart_boost_ref = KartBoost.chain(player_idx)
        boost_acceleration_ref = kart_boost_ref + 0x18
        return memory.read_f32(boost_acceleration_ref)
    
    def inst_boost_acceleration(self) -> float:
        boost_acceleration_ref = self.addr + 0x18
        return memory.read_f32(boost_acceleration_ref)
    
    @staticmethod
    def boost_speed_limit(player_idx=0) -> float:
        kart_boost_ref = KartBoost.chain(player_idx)
        boost_speed_limit_ref = kart_boost_ref + 0x20
        return memory.read_f32(boost_speed_limit_ref)
    
    def inst_boost_speed_limit(self) -> float:
        boost_speed_limit_ref = self.addr + 0x20
        return memory.read_f32(boost_speed_limit_ref)