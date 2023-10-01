from dolphin import controller, event
import math
from Modules import mkw_classes as classes


@event.on_frameadvance
def onFrameAdvance():
    speed = classes.PlayerStats.base_speed()
    currentSpeed = classes.KartMove.speed()
    topSpeed = speed * 1.15

    turnSpeed = classes.PlayerStats.turning_speed()
    
    A3 = classes.PlayerStats.accel_standard_a3()
    
    wheelie_frames = classes.KartMove.wheelie_frames()

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
