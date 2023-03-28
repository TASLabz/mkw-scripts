from dolphin import controller, event, gui
import mkw_core as core
import mkw_classes as classes
from framesequence import FrameSequence


@event.on_frameadvance
def on_frame_advance():
    race_frame = core.get_frame_of_input()
    global last_race_frame, sequence
    if 0 < race_frame == last_race_frame:
        race_frame += 1
    if last_race_frame > race_frame:
        sequence.refresh()
    inputs = sequence.get_controller_inputs(race_frame)
    if inputs and classes.RaceInfo.stage() >= 1:  # If there are inputs on this frame, send the inputs
        controller.set_gc_buttons(0, inputs)
    last_race_frame = race_frame


@event.on_savestateload
def on_savestate_load(is_slot, slot):
    global sequence
    if (is_slot):
        sequence.refresh()
        on_frame_advance()


if __name__ == '__main__':
    global sequence
    # Run on script start
    race_frame = core.get_frame_of_input()
    last_race_frame = race_frame - 1
    # TODO (xi):    eventually automate filepath search (would like saving in place
    #               first before implementing)
    pianoroll_path = r'filepath'
    sequence = FrameSequence(pianoroll_path)
    gui.add_osd_message(f"{pianoroll_path} successfully loaded!")
