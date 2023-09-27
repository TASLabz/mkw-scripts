from dolphin import event, gui, utils
from Modules import TTK_Lib
from Modules import mkw_classes as classes
from Modules import mkw_core as core
from Modules import mkw_translations as translate
from Modules.framesequence import FrameSequence
import os

flame_slide_bikes = ("Flame Runner", "Mach Bike", "Sugarscoot", "Zip Zip")
spear_slide_bikes = ("Jet Bubble", "Phantom", "Spear", "Sneakster", "Wario Bike")
star_slide_bikes  = ("Bit Bike", "Bullet Bike", "Dolphin Dasher", "Magikruiser",
                     "Quacker", "Shooting Star", "Standard Bike L", "Standard Bike M",
                     "Standard Bike S")

@event.on_savestateload
def onStateLoad(is_slot, slot):
    playerInputs.readFromFile()

@event.on_frameadvance
def onFrameAdvance():
    frame = core.get_frame_of_input()
    
    playerInput = playerInputs[frame]
    if (playerInput and classes.RaceInfo.stage() == 1):
        TTK_Lib.writePlayerInputs(playerInput)

def main() -> None:
    global playerInputs
    playerInputs = FrameSequence(check_vehicle(translate.vehicle_id()))
    
    gui.add_osd_message("Startslide: {} ".format(len(playerInputs) > 0))
    
# Ensures the right slide for the currently selected bike is being loaded,
# even through savestates and vehicle swaps.
def check_vehicle(vehicle):

    # Returns True if the player is using a bike.
    if bool(classes.KartParam.is_bike()):

        path = utils.get_script_dir()

        if vehicle in flame_slide_bikes:
            return os.path.join(path, "MKW_Inputs", "Startslides", "flame_left.csv")

        elif vehicle in spear_slide_bikes:
            return os.path.join(path, "MKW_Inputs", "Startslides", "spear_left.csv")

        elif vehicle in star_slide_bikes:
            return os.path.join(path, "MKW_Inputs", "Startslides", "star_left.csv")

if __name__ == '__main__':
    main()
