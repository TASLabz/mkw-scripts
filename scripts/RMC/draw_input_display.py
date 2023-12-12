from dolphin import gui, event
from Modules import input_display as display

from Modules.mkw_classes import RaceManager, RaceManagerPlayer, RaceState
from Modules.mkw_classes import KartInput, RaceInputState, ButtonActions

stick_dict = {-7: 0, -6: 60, -5: 70, -4: 80, -3: 90, -2: 100, -1: 110,
              0: 128, 1: 155, 2: 165, 3: 175, 4: 185, 5: 195, 6: 200, 7: 255}


@event.on_frameadvance
def on_frame_advance():
    race_mgr = RaceManager()
    if race_mgr.state().value >= RaceState.COUNTDOWN.value:

        # TODO: use masks instead of the values for buttons
        race_mgr_player_addr = race_mgr.race_manager_player()
        race_mgr_player = RaceManagerPlayer(addr=race_mgr_player_addr)
        kart_input = KartInput(addr=race_mgr_player.kart_input())
        current_input_state = RaceInputState(addr=kart_input.current_input_state())
        ablr = current_input_state.buttons()
        dpad = current_input_state.trick()
        xstick = current_input_state.raw_stick_x() - 7
        ystick = current_input_state.raw_stick_y() - 7

        # A Button
        if ablr.value & ButtonActions.A:
            func = display.fill_pressed_button
        else:
            func = display.create_unpressed_button
        func([330, gui.get_display_size()[1] - 95], 35, 0xFFFFFFFF)

        # L Button
        if ablr.value & ButtonActions.L:
            func = display.fill_pressed_bumper
        else:
            func = display.create_unpressed_bumper
        func([30, gui.get_display_size()[1] - 200], 100, 50, 0xFFFFFFFF)
            
        # R Button
        if ablr.value & ButtonActions.B:
            func = display.fill_pressed_bumper
        else:
            func = display.create_unpressed_bumper
        func([280, gui.get_display_size()[1] - 200], 100, 50, 0xFFFFFFFF)

        # D-Pad
        # TODO: fix the module so that -35 does not have to be used here
        display.create_dpad(
            [30, gui.get_display_size()[1] - 32.5], 30, -35, 0xFFFFFFFF)
        
        direction = None
        if dpad == 1:
            direction = ["Up"]
        elif dpad == 2:
            direction = ["Down"]
        elif dpad == 3:
            direction = ["Left"]
        elif dpad == 4:
            direction = ["Right"]
        
        if direction:
            display.fill_dpad([30, gui.get_display_size()[1] - 32.5],
                              30, -35, 0xFFFFFFFF, direction)

        # Control Stick
        display.create_control_stick([210, gui.get_display_size()[1] - 100], 50, 30, 50,
            stick_dict.get(xstick, 0), stick_dict.get(ystick, 0), 0xFFFFFFFF)
