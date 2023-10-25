from dolphin import memory

from . import KartMove, TrickType, quatf

class KartJump:
    class TrickProperties:
        def __init__(self, player_idx=0, addr=None):
            self.addr = addr if addr else KartJump.TrickProperties.chain(player_idx)

            self.initial_angle_diff = self.inst_initial_angle_diff
            self.angle_delta_min = self.inst_angle_delta_min
            self.angle_delta_factor_min = self.inst_angle_delta_factor_min
            self.angle_diff_mul_dec = self.inst_angle_diff_mul_dec

        @staticmethod
        def chain(player_idx=0) -> int:
            return KartJump.trick_properties(player_idx=0)
        
        @staticmethod
        def initial_angle_diff(player_idx=0) -> float:
            trick_properties_ref = KartJump.TrickProperties.chain(player_idx)
            initial_angle_diff_ref = trick_properties_ref + 0x0
            return memory.read_f32(initial_angle_diff_ref)
        
        def inst_initial_angle_diff(self) -> float:
            initial_angle_diff_ref = self.addr + 0x0
            return memory.read_f32(initial_angle_diff_ref)
        
        @staticmethod
        def angle_delta_min(player_idx=0) -> float:
            trick_properties_ref = KartJump.TrickProperties.chain(player_idx)
            angle_delta_min_ref = trick_properties_ref + 0x4
            return memory.read_f32(angle_delta_min_ref)
        
        def inst_angle_delta_min(self) -> float:
            angle_delta_min_ref = self.addr + 0x4
            return memory.read_f32(angle_delta_min_ref)
        
        @staticmethod
        def angle_delta_factor_min(player_idx=0) -> float:
            trick_properties_ref = KartJump.TrickProperties.chain(player_idx)
            angle_delta_factor_min_ref = trick_properties_ref + 0x8
            return memory.read_f32(angle_delta_factor_min_ref)
        
        def inst_angle_delta_factor_min(self) -> float:
            angle_delta_factor_min_ref = self.addr + 0x8
            return memory.read_f32(angle_delta_factor_min_ref)
        
        @staticmethod
        def angle_diff_mul_dec(player_idx=0) -> float:
            trick_properties_ref = KartJump.TrickProperties.chain(player_idx)
            angle_delta_factor_min_ref = trick_properties_ref + 0xC
            return memory.read_f32(angle_delta_factor_min_ref)
        
        def inst_angle_diff_mul_dec(self) -> float:
            angle_delta_factor_min_ref = self.addr + 0xC
            return memory.read_f32(angle_delta_factor_min_ref)

    def __init__(self, player_idx=0, addr=None):
        self.addr = addr if addr else KartJump.chain(player_idx)

        self.type = self.inst_type
        self.category = self.inst_category
        self.next_trick_direction = self.inst_next_trick_direction
        self.next_allow_timer = self.inst_next_allow_timer
        self.rotation_sign = self.inst_rotation_sign
        self.trick_properties = self.inst_trick_properties
        self.angle = self.inst_angle
        self.angle_delta = self.inst_angle_delta
        self.angle_delta_factor = self.inst_angle_delta_factor
        self.angle_delta_factor_decrease = self.inst_angle_delta_factor_decrease
        self.final_angle = self.inst_final_angle
        self.cooldown = self.inst_cooldown
        self.boost_ramp_enabled = self.inst_boost_ramp_enabled
        self.rotation = self.inst_rotation

    @staticmethod
    def chain(player_idx=0) -> int:
        return KartMove.kart_jump(player_idx)

    @staticmethod
    def type(player_idx=0) -> TrickType:
        kart_jump_ref = KartJump.chain(player_idx)
        type_ref = kart_jump_ref + 0x10
        return TrickType(memory.read_u32(type_ref))
    
    def inst_type(self) -> TrickType:
        type_ref = self.addr + 0x10
        return TrickType(memory.read_u32(type_ref))
    
    @staticmethod
    def category(player_idx=0) -> int:
        kart_jump_ref = KartJump.chain(player_idx)
        category_ref = kart_jump_ref + 0x14
        return memory.read_u32(category_ref)
    
    def inst_category(self) -> int:
        category_ref = self.addr + 0x14
        return memory.read_u32(category_ref)
    
    @staticmethod
    def next_trick_direction(player_idx=0) -> int:
        """1=UP,2=DOWN,3=LEFT,4=RIGHT"""
        kart_jump_ref = KartJump.chain(player_idx)
        next_trick_direction_ref = kart_jump_ref + 0x18
        return memory.read_u8(next_trick_direction_ref)
    
    def inst_next_trick_direction(self) -> int:
        """1=UP,2=DOWN,3=LEFT,4=RIGHT"""
        next_trick_direction_ref = self.addr + 0x18
        return memory.read_u8(next_trick_direction_ref)
    
    @staticmethod
    def next_allow_timer(player_idx=0) -> int:
        kart_jump_ref = KartJump.chain(player_idx)
        next_allow_timer_ref = kart_jump_ref + 0x1A
        return memory.read_u16(next_allow_timer_ref)
    
    def inst_next_allow_timer(self) -> int:
        next_allow_timer_ref = self.addr + 0x1A
        return memory.read_u16(next_allow_timer_ref)
    
    @staticmethod
    def rotation_sign(player_idx=0) -> float:
        """+1 or -1"""
        kart_jump_ref = KartJump.chain(player_idx)
        rotation_sign_ref = kart_jump_ref + 0x1C
        return memory.read_f32(rotation_sign_ref)
    
    def inst_rotation_sign(self) -> float:
        """+1 or -1"""
        rotation_sign_ref = self.addr + 0x1C
        return memory.read_f32(rotation_sign_ref)
    
    @staticmethod
    def trick_properties(player_idx=0) -> int:
        kart_jump_ref = KartJump.chain(player_idx)
        trick_properties_ref = kart_jump_ref + 0x20
        return memory.read_u32(trick_properties_ref)
    
    def inst_trick_properties(self) -> int:
        trick_properties_ref = self.addr + 0x20
        return memory.read_u32(trick_properties_ref)
    
    @staticmethod
    def angle(player_idx=0) -> float:
        kart_jump_ref = KartJump.chain(player_idx)
        angle_ref = kart_jump_ref + 0x24
        return memory.read_f32(angle_ref)
    
    def inst_angle(self) -> float:
        angle_ref = self.addr + 0x24
        return memory.read_f32(angle_ref)
    
    @staticmethod
    def angle_delta(player_idx=0) -> float:
        kart_jump_ref = KartJump.chain(player_idx)
        angle_delta_ref = kart_jump_ref + 0x28
        return memory.read_f32(angle_delta_ref)
    
    def inst_angle_delta(self) -> float:
        angle_delta_ref = self.addr + 0x28
        return memory.read_f32(angle_delta_ref)
    
    @staticmethod
    def angle_delta_factor(player_idx=0) -> float:
        kart_jump_ref = KartJump.chain(player_idx)
        angle_delta_factor_ref = kart_jump_ref + 0x2C
        return memory.read_f32(angle_delta_factor_ref)
    
    def inst_angle_delta_factor(self) -> float:
        angle_delta_factor_ref = self.addr + 0x2C
        return memory.read_f32(angle_delta_factor_ref)
    
    @staticmethod
    def angle_delta_factor_decrease(player_idx=0) -> float:
        kart_jump_ref = KartJump.chain(player_idx)
        angle_delta_factor_decrease_ref = kart_jump_ref + 0x30
        return memory.read_f32(angle_delta_factor_decrease_ref)
    
    def inst_angle_delta_factor_decrease(self) -> float:
        angle_delta_factor_decrease_ref = self.addr + 0x30
        return memory.read_f32(angle_delta_factor_decrease_ref)
    
    @staticmethod
    def final_angle(player_idx=0) -> float:
        kart_jump_ref = KartJump.chain(player_idx)
        final_angle_ref = kart_jump_ref + 0x34
        return memory.read_f32(final_angle_ref)
    
    def inst_final_angle(self) -> float:
        final_angle_ref = self.addr + 0x34
        return memory.read_f32(final_angle_ref)
    
    @staticmethod
    def cooldown(player_idx=0) -> int:
        kart_jump_ref = KartJump.chain(player_idx)
        cooldown_ref = kart_jump_ref + 0x38
        return memory.read_u16(cooldown_ref)
    
    def inst_cooldown(self) -> int:
        cooldown_ref = self.addr + 0x38
        return memory.read_u16(cooldown_ref)
    
    @staticmethod
    def boost_ramp_enabled(player_idx=0) -> bool:
        kart_jump_ref = KartJump.chain(player_idx)
        boost_ramp_enabled_ref = kart_jump_ref + 0x3A
        return memory.read_u8(boost_ramp_enabled_ref) > 0
    
    def inst_boost_ramp_enabled(self) -> bool:
        boost_ramp_enabled_ref = self.addr + 0x3A
        return memory.read_u8(boost_ramp_enabled_ref) > 0
    
    @staticmethod
    def rotation(player_idx=0) -> quatf:
        kart_jump_ref = KartJump.chain(player_idx)
        rotation_ref = kart_jump_ref + 0x3C
        return quatf.read(rotation_ref)
    
    def inst_rotation(self) -> quatf:
        rotation_ref = self.addr + 0x3C
        return quatf.read(rotation_ref)