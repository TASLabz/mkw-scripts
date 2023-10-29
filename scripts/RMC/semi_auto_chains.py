from dolphin import controller, event

from Modules.mkw_classes import KartMove, RaceManager, RaceState

@event.on_frameadvance
def main():
    race_mgr = RaceManager()
    if race_mgr.state().value >= RaceState.COUNTDOWN.value:
        pressing_up = controller.get_gc_buttons(0)["Up"]
        if pressing_up and KartMove.wheelie_frames() == 180:
            controller.set_gc_buttons(
                0, {"A": True,
                    "Up": False,
                    "StickX": controller.get_gc_buttons(0)["StickX"]})
