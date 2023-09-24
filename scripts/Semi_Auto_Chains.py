from dolphin import controller, event
from Modules import mkw_classes as classes


@event.on_frameadvance
def main():
    if controller.get_gc_buttons(0)["Up"] and classes.KartMove.wheelie_frames() == 180:
        controller.set_gc_buttons(
            0, {"A": True,
                "Up": False,
                "StickX": controller.get_gc_buttons(0)["StickX"]})
