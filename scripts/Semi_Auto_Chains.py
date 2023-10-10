from dolphin import controller, event

from Modules.mkw_classes import KartMove

@event.on_frameadvance
def main():
    pressing_up = controller.get_gc_buttons(0)["Up"]
    if pressing_up and KartMove.wheelie_frames(playerIdx=0) == 180:
        controller.set_gc_buttons(
            0, {"A": True,
                "Up": False,
                "StickX": controller.get_gc_buttons(0)["StickX"]})
