from dolphin import controller, event, gui, memory, utils
import mkw_core as core
import mkw_classes as classes
from framesequence import FrameSequence


def set_ghost_buttons(inputs):
    ghostcontrolleraddress = {"RMCE01": 0x809b8f70, "RMCP01": 0x809BD730,
                              "RMCJ01": 0x809bc790, "RMCK01": 0x809abd70}
    ghostcontrollerptr = core.chase_pointer(
        ghostcontrolleraddress[core.get_game_id()], [0xC, 0x4, 0x48, 0x4], 'u32')

    buttons = memory.read_u32(ghostcontrollerptr + 0x94)
    memory.write_u8(buttons + 0x12, inputs.accel + (inputs.brake << 1) +
                    (inputs.item << 2) | ((inputs.accel & inputs.brake) << 3))

    stick = memory.read_u32(ghostcontrollerptr + 0x98)
    memory.write_u8(stick + 0x12, (inputs.stick_y + 7)
                    | ((inputs.stick_x + 7) << 4))

    trickbuttons = memory.read_u32(ghostcontrollerptr + 0x9C)
    if inputs.dpad_up:
        memory.write_u8(trickbuttons + 0x12, 0x1)
    elif inputs.dpad_down:
        memory.write_u8(trickbuttons + 0x12, 0x2)
    elif inputs.dpad_left:
        memory.write_u8(trickbuttons + 0x12, 0x3)
    elif inputs.dpad_right:
        memory.write_u8(trickbuttons + 0x12, 0x4)
    else:
        memory.write_u8(trickbuttons + 0x12, 0x0)


@event.on_frameadvance
def calc():
    global sequence

    dbs_address = {"RMCE01": 0x8051c8d8, "RMCP01": 0x80520d4c,
                   "RMCJ01": 0x805206cc, "RMCK01": 0x8050ed70}
    fbs_address = {"RMCE01": 0x8051eacc, "RMCP01": 0x80522f40,
                   "RMCJ01": 0x805228c0, "RMCK01": 0x80510f64}
    tbs_address = {"RMCE01": 0x8051e7e8, "RMCP01": 0x80522c5c,
                   "RMCJ01": 0x805225dc, "RMCK01": 0x80510c80}
    inputs = sequence.frames[core.get_frame_of_input()]
    if inputs and classes.RaceInfo.stage() >= 1:  # If there are inputs on this frame, send the inputs
        # DirectionButtonsStream_readFrame
        memory.write_u32(dbs_address[core.get_game_id()], 0x88630012) # lbz r3, 0x12 (r3)
        memory.write_u32(
            dbs_address[core.get_game_id()] + 0x4, 0x4e800020)        # blr
        memory.invalidate_icache(dbs_address[core.get_game_id()], 0x8)
        # FaceButtonsStream_readFrame
        memory.write_u32(fbs_address[core.get_game_id()], 0x88630012) # lbz r3, 0x12 (r3)
        memory.write_u32(
            fbs_address[core.get_game_id()] + 0x4, 0x4e800020)        # blr
        memory.invalidate_icache(fbs_address[core.get_game_id()], 0x8)
        # TricksButtonStream_readFrame
        memory.write_u32(tbs_address[core.get_game_id()], 0x88630012) # lbz r3, 0x12 (r3)
        memory.write_u32(
            tbs_address[core.get_game_id()] + 0x4, 0x4e800020)        # blr
        memory.invalidate_icache(tbs_address[core.get_game_id()], 0x8)
        set_ghost_buttons(inputs)
    else:
        # restore instructions if no inputs

        # DirectionButtonsStream_readFrame
        memory.write_u32(dbs_address[core.get_game_id()], 0x9421ffe0) # stwu sp, -0x20 (sp)
        memory.write_u32(
            dbs_address[core.get_game_id()] + 0x4, 0x7c0802a6)         # mflr r0
        memory.invalidate_icache(dbs_address[core.get_game_id()], 0x8)
        # FaceButtonsStream_readFrame
        memory.write_u32(fbs_address[core.get_game_id()], 0x9421ffe0) # stwu sp, -0x20 (sp)
        memory.write_u32(
            fbs_address[core.get_game_id()] + 0x4, 0x7c0802a6)        # mflr r0
        memory.invalidate_icache(fbs_address[core.get_game_id()], 0x8)
        # TricksButtonStream_readFrame
        memory.write_u32(tbs_address[core.get_game_id()], 0x9421ffe0) # stwu sp, -0x20 (sp)
        memory.write_u32(
            tbs_address[core.get_game_id()] + 0x4, 0x7c0802a6)        # mflr r0
        memory.invalidate_icache(tbs_address[core.get_game_id()], 0x8)


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
