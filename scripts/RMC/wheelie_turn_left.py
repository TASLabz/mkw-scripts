from dolphin import controller, event
import math

from Modules.mkw_classes import PlayerStats, KartMove

@event.on_frameadvance
def on_frame_advance():
    player_stats = PlayerStats()
    kart_move = KartMove()

    speed = player_stats.base_speed()
    current_speed = kart_move.speed()
    top_speed = speed * 1.15

    turn_speed = player_stats.handling_speed_multiplier()
    
    A3 = player_stats.standard_accel_as(3)
    
    wheelie_frames = kart_move.wheelie_frames()

    formula = math.ceil(((1 - ((top_speed - A3) / top_speed)) / (1 - turn_speed)) * 7)

    if (wheelie_frames != 181):
        stick_val = 128
        if top_speed < current_speed * (turn_speed + (1 - turn_speed)) + A3:
            if formula == 1:
                stick_val = 112
            elif formula == 2:
                stick_val = 104
        else:
            if formula == 1:
                pass
            elif formula == 2:
                stick_val = 112
        controller.set_gc_buttons(
                0, {"A": True, "StickX": stick_val})
    else:
        controller.set_gc_buttons(
                0, {"A": True,
                    "Up": controller.get_gc_buttons(0)["Up"],
                    "StickX": controller.get_gc_buttons(0)["StickX"]})
