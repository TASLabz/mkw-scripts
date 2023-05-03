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

    inputs = sequence.get_gc_inputs(race_frame)
    if inputs and classes.RaceInfo.stage() == 1:  # If there are inputs on this frame and the race is in the countdown phase, send the inputs.
        controller.set_gc_buttons(0, inputs)


@event.on_savestateload
def reload(is_slot, slot):
    global sequence
    if (is_slot):
        sequence.refresh()


if __name__ == '__main__':
    # Run on script start
    if bool(classes.KartParam.is_bike()):  # Returns True if the player is using a bike.
        pianoroll_path = utils.get_script_dir() + r'\MKW_Inputs\Startslides'
        
        if translate.vehicle_id() in flame_slide_bikes:
            pianoroll_path += r'\flame_right.csv'

        elif translate.vehicle_id() in spear_slide_bikes:
            pianoroll_path += r'\spear_right.csv'

        elif translate.vehicle_id() in star_slide_bikes:
            pianoroll_path += r'\star_right.csv'
        
        sequence = FrameSequence(pianoroll_path)
        gui.add_osd_message("Startslide successfully loaded!")
