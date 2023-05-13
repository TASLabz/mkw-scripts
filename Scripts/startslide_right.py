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

@event.on_frameadvance
def calc():
    global sequence
    race_frame = core.get_frame_of_input()

    # Checks if the correct slide is being used at the start of the race.
    if race_frame == 0:
        check_vehicle()

    inputs = sequence.get_gc_inputs(race_frame)

    # If there are inputs on this frame and the race is in the countdown phase, send the inputs.
    if inputs and classes.RaceInfo.stage() == 1:
        controller.set_gc_buttons(0, inputs)


@event.on_savestateload
def reload(is_slot, slot):
    global sequence
    check_vehicle()
    if (is_slot):
        sequence.refresh()


# Ensures the right slide for the currently selected bike is being loaded,
# even through savestates and vehicle swaps.
def check_vehicle():
    global sequence

    # Returns True if the player is using a bike.
    if bool(classes.KartParam.is_bike()):
        pianoroll_path = utils.get_script_dir() + r'\MKW_Inputs\Startslides'
        
        if translate.vehicle_id() in flame_slide_bikes:
            pianoroll_path += r'\flame_right.csv'

        elif translate.vehicle_id() in spear_slide_bikes:
            pianoroll_path += r'\spear_right.csv'

        elif translate.vehicle_id() in star_slide_bikes:
            pianoroll_path += r'\star_right.csv'
        
        sequence = FrameSequence(pianoroll_path)

if __name__ == '__main__':
    # Runs on script activation. 'sequence' can not be defined inside 'check_vehicle',
    # so it is done here instead.
    sequence = None
    check_vehicle()
