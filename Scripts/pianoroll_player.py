from dolphin import controller, event, gui, utils
import mkw_core as core
import mkw_classes as classes
from framesequence import FrameSequence


@event.on_frameadvance
def calc():
    global sequence

    inputs = sequence.get_gc_inputs(core.get_frame_of_input())
    if inputs and classes.RaceInfo.stage() >= 1:  # If there are inputs on this frame, send the inputs.
        controller.set_gc_buttons(0, inputs)


@event.on_savestateload
def reload(is_slot, slot):
    global sequence
    if (is_slot):
        sequence.refresh()


if __name__ == '__main__':
    # Run on script start
    # TODO (xi):    eventually automate filepath search (would like saving in place
    #               first before implementing)
    pianoroll_path = utils.open_file()
    sequence = FrameSequence(pianoroll_path)
    gui.add_osd_message(f"{pianoroll_path} successfully loaded!")
