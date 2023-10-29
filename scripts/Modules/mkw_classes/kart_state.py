from dolphin import memory

from . import KartObject, vec3

class KartState:
    def __init__(self, player_idx=0, addr=None):
        self.addr = addr if addr else KartState.chain(player_idx)

        self.bitfield = self.inst_bitfield
        self.airtime = self.inst_airtime
        self.top = self.inst_top
        self.hwg_timer = self.inst_hwg_timer
        self.boost_ramp_type = self.inst_boost_ramp_type
        self.jump_pad_type = self.inst_jump_pad_type
        self.cnpt_id = self.inst_cnpt_id
        self.stick_x = self.inst_stick_x
        self.stick_y = self.inst_stick_y
        self.oob_wipe_state = self.inst_oob_wipe_state
        self.oob_wipe_frame = self.inst_oob_wipe_frame
        self.start_boost_charge = self.inst_start_boost_charge
        self.start_boost_idx = self.inst_start_boost_idx
        self.trickable_timer = self.inst_trickable_timer
    
    @staticmethod
    def chain(player_idx=0) -> int:
        return KartObject.kart_state(player_idx)

    @staticmethod
    def bitfield(player_idx=0, field_idx=0) -> int:
        assert(0 <= field_idx < 5)
        kart_state_ref = KartState.chain(player_idx)
        bitfield_ref = kart_state_ref + 0x4 + (field_idx * 0x4)
        return memory.read_u32(bitfield_ref)

    def inst_bitfield(self, field_idx=0) -> int:
        assert(0 <= field_idx < 5)
        bitfield_ref = self.addr + 0x4 + (field_idx * 0x4)
        return memory.read_u32(bitfield_ref)

    @staticmethod
    def airtime(player_idx=0) -> int:
        kart_state_ref = KartState.chain(player_idx)
        airtime_ref = kart_state_ref + 0x1C
        return memory.read_u32(airtime_ref)

    def inst_airtime(self) -> int:
        airtime_ref = self.addr + 0x1C
        return memory.read_u32(airtime_ref)

    @staticmethod
    def top(player_idx=0) -> vec3:
        """Significance unknown?"""
        kart_state_ref = KartState.chain(player_idx)
        top_ref = kart_state_ref + 0x28
        return vec3.read(top_ref)

    def inst_top(self) -> int:
        top_ref = self.addr + 0x28
        return vec3.read(top_ref)

    @staticmethod
    def hwg_timer(player_idx=0) -> int:
        kart_state_ref = KartState.chain(player_idx)
        hwg_timer_ref = kart_state_ref + 0x6C
        return memory.read_u32(hwg_timer_ref)

    def inst_hwg_timer(self) -> int:
        hwg_timer_ref = self.addr + 0x6C
        return memory.read_u32(hwg_timer_ref)

    @staticmethod
    def boost_ramp_type(player_idx=0) -> int:
        kart_state_ref = KartState.chain(player_idx)
        boost_ramp_type_ref = kart_state_ref + 0x74
        return memory.read_u32(boost_ramp_type_ref)

    def inst_boost_ramp_type(self) -> int:
        boost_ramp_type_ref = self.addr + 0x74
        return memory.read_u32(boost_ramp_type_ref)

    @staticmethod
    def jump_pad_type(player_idx=0) -> int:
        kart_state_ref = KartState.chain(player_idx)
        jump_pad_type_ref = kart_state_ref + 0x78
        return memory.read_u32(jump_pad_type_ref)

    def inst_jump_pad_type(self) -> int:
        jump_pad_type_ref = self.addr + 0x78
        return memory.read_u32(jump_pad_type_ref)

    @staticmethod
    def cnpt_id(player_idx=0) -> int:
        kart_state_ref = KartState.chain(player_idx)
        cnpt_id_ref = kart_state_ref + 0x80
        return memory.read_u32(cnpt_id_ref)

    def inst_cnpt_id(self) -> int:
        cnpt_id_ref = self.addr + 0x80
        return memory.read_u32(cnpt_id_ref)

    @staticmethod
    def stick_x(player_idx=0) -> float:
        kart_state_ref = KartState.chain(player_idx)
        stick_x_ref = kart_state_ref + 0x88
        return memory.read_f32(stick_x_ref)

    def inst_stick_x(self) -> float:
        stick_x_ref = self.addr + 0x88
        return memory.read_f32(stick_x_ref)

    @staticmethod
    def stick_y(player_idx=0) -> float:
        kart_state_ref = KartState.chain(player_idx)
        stick_y_ref = kart_state_ref + 0x8C
        return memory.read_f32(stick_y_ref)

    def inst_stick_y(self) -> float:
        stick_y_ref = self.addr + 0x8C
        return memory.read_f32(stick_y_ref)

    @staticmethod
    def oob_wipe_state(player_idx=0) -> int:
        kart_state_ref = KartState.chain(player_idx)
        oob_wipe_state_ref = kart_state_ref + 0x90
        return memory.read_u32(oob_wipe_state_ref)

    def inst_oob_wipe_state(self) -> int:
        oob_wipe_state_ref = self.addr + 0x90
        return memory.read_u32(oob_wipe_state_ref)

    @staticmethod
    def oob_wipe_frame(player_idx=0) -> int:
        kart_state_ref = KartState.chain(player_idx)
        oob_wipe_frame_ref = kart_state_ref + 0x94
        return memory.read_u32(oob_wipe_frame_ref)

    def inst_oob_wipe_frame(self) -> int:
        oob_wipe_frame_ref = self.addr + 0x94
        return memory.read_u32(oob_wipe_frame_ref)

    @staticmethod
    def start_boost_charge(player_idx=0) -> float:
        kart_state_ref = KartState.chain(player_idx)
        start_boost_charge_ref = kart_state_ref + 0x9C
        return memory.read_f32(start_boost_charge_ref)

    def inst_start_boost_charge(self) -> float:
        start_boost_charge_ref = self.addr + 0x9C
        return memory.read_f32(start_boost_charge_ref)

    @staticmethod
    def start_boost_idx(player_idx=0) -> float:
        kart_state_ref = KartState.chain(player_idx)
        start_boost_idx_ref = kart_state_ref + 0xA0
        return memory.read_f32(start_boost_idx_ref)

    def inst_start_boost_idx(self) -> float:
        start_boost_idx_ref = self.addr + 0xA0
        return memory.read_f32(start_boost_idx_ref)

    @staticmethod
    def trickable_timer(player_idx=0) -> int:
        kart_state_ref = KartState.chain(player_idx)
        trickable_timer_ref = kart_state_ref + 0xA6
        return memory.read_u16(trickable_timer_ref)

    def inst_trickable_timer(self) -> int:
        trickable_timer_ref = self.addr + 0xA6
        return memory.read_u16(trickable_timer_ref)