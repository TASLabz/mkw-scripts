from dolphin import controller, event
import math

from Modules.mkw_classes import PlayerStats, KartMove

@event.on_frameadvance
def onFrameAdvance():
    player_stats = PlayerStats(playerIdx=0)
    kart_move = KartMove(playerIdx=0)

    speed = player_stats.base_speed()
    currentSpeed = kart_move.speed()
    topSpeed = speed * 1.15

    turnSpeed = player_stats.handling_speed_multiplier()
    
    A3 = player_stats.standard_accel_as(3)
    
    wheelie_frames = kart_move.wheelie_frames()

    formula = math.ceil(((1 - ((topSpeed - A3) / topSpeed)) / (1 - turnSpeed)) * 7)

    if (wheelie_frames != 181):
        stick_val = 128
        if topSpeed < currentSpeed * (turnSpeed + (1 - turnSpeed)) + A3:
            if formula == 1:
                stick_val = 152
            elif formula == 2:
                stick_val = 167
        else:
            if formula == 1:
                pass
            elif formula == 2:
                stick_val = 152
        controller.set_gc_buttons(
                0, {"A": True, "StickX": stick_val})
    else:
        controller.set_gc_buttons(
                0, {"A": True,
                    "Up": controller.get_gc_buttons(0)["Up"],
                    "StickX": controller.get_gc_buttons(0)["StickX"]})
