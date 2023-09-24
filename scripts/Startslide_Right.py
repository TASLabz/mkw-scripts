from dolphin import controller, event, gui, utils
import mkw_core as core
import mkw_classes as classes
import mkw_translations as translate
from framesequence import FrameSequence

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
    global playerInputs
    frame = core.get_frame_of_input()
    
    playerInput = playerInputs[frame]
    if (playerInput and classes.RaceInfo.stage() == 1):
        controller.set_gc_buttons(0, playerInput.get_controller_inputs())

def main() -> None:
    global playerInputs
    playerInputs = FrameSequence(check_vehicle())
    
    gui.add_osd_message("Startslide: {} ".format(len(playerInputs) > 0))
    
# Ensures the right slide for the currently selected bike is being loaded,
# even through savestates and vehicle swaps.
def check_vehicle():

    # Returns True if the player is using a bike.
    if bool(classes.KartParam.is_bike()):
        path = utils.get_script_dir() + r'\MKW_Inputs\Startslides'
        
        if translate.vehicle_id() in flame_slide_bikes:
            path += r'\flame_right.csv'

        elif translate.vehicle_id() in spear_slide_bikes:
            path += r'\spear_right.csv'

        elif translate.vehicle_id() in star_slide_bikes:
            path += r'\star_right.csv'
        
        return path

if __name__ == '__main__':
    main()
