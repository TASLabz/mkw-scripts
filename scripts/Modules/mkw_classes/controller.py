from dolphin import memory

class Controller:
    def __init__(self, addr):
        """There are multiple instances of this class.
           To create an instance, enforce that the caller passes in its address."""
        self.addr = addr

    def race_input_state(self) -> int:
        race_input_state_ref = self.addr + 0x4
        return race_input_state_ref

    def ui_input_state(self) -> int:
        ui_input_state_ref = self.addr + 0x1C
        return ui_input_state_ref

    def is_connected(self) -> bool:
        is_connected_ref = self.addr + 0x50
        return memory.read_u8(is_connected_ref) != 0

    def drift_is_auto(self) -> bool:
        drift_is_auto_ref = self.addr + 0x51
        return memory.read_u8(drift_is_auto_ref) != 0

    def battery(self) -> int:
        battery_ref = self.addr + 0x54
        return memory.read_u32(battery_ref)

    def out_of_battery(self) -> bool:
        out_of_battery_ref = self.addr + 0x58
        return memory.read_u8(out_of_battery_ref) != 0

    def prev_ui_input_state(self) -> int:
        prev_ui_input_state_ref = self.addr + 0x5C
        return memory.read_u32(prev_ui_input_state_ref)
