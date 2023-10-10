from dolphin import memory

class KartInput:
    def __init__(self, addr):
        """There are multiple instances of this class.
           To create an instance, enforce that the caller passes in its address."""
        self.addr = addr

    def race_controller(self) -> int:
        race_controller_ptr = self.addr + 0x4
        return memory.read_u32(race_controller_ptr)

    def ui_controller(self) -> int:
        ui_controller_ptr = self.addr + 0x8
        return memory.read_u32(ui_controller_ptr)

    def rumble_duration(self) -> int:
        rumble_duration_ref = self.addr + 0x14
        return memory.read_s8(rumble_duration_ref)
    
    def rumble_manager(self) -> int:
        rumble_manager_ptr = self.addr + 0x20
        return memory.read_u32(rumble_manager_ptr)

    def rumble_manager_2(self) -> int:
        rumble_manager_2_ptr = self.addr + 0x24
        return memory.read_u32(rumble_manager_2_ptr)

    def current_input_state(self) -> int:
        current_input_state_ref = self.addr + 0x28
        return current_input_state_ref
    
    def last_input_state(self) -> int:
        last_input_state_ref = self.addr + 0x40
        return last_input_state_ref

    def ui_input_state(self) -> int:
        ui_input_state_ref = self.addr + 0x58
        return ui_input_state_ref

    def last_ui_input_state(self) -> int:
        last_ui_input_state_ref = self.addr + 0x8C
        return last_ui_input_state_ref
    
    def num_frames_race_input_idle(self) -> int:
        """Online only?"""
        num_frames_race_input_idle_ref = self.addr + 0xC2
        return memory.read_u16(num_frames_race_input_idle_ref)
    
    def num_frames_disconnected(self) -> int:
        num_frames_disconnected_ref = self.addr + 0xC4
        return memory.read_u16(num_frames_disconnected_ref)
    
    def controller_info(self) -> int:
        controller_info_ref = self.addr + 0xC8
        return controller_info_ref