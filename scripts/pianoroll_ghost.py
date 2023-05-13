from dolphin import controller, event, gui, memory, utils
import mkw_core as core
import mkw_classes as classes
from framesequence import FrameSequence


def set_ghost_buttons(inputs):
    # NOTE: Ghost controller index 1 is consistent in the base game
    ghost_controller = memory.read_u32(classes.InputMgr.chain()) + 0x3f08

    buttons = memory.read_u32(ghost_controller + 0x94)
    memory.write_u8(buttons + 0x12, inputs.accel + (inputs.brake << 1) +
                    (inputs.item << 2) | ((inputs.accel & inputs.brake) << 3))

    stick = memory.read_u32(ghost_controller + 0x98)
    memory.write_u8(stick + 0x12, (inputs.stick_y + 7)
                    | ((inputs.stick_x + 7) << 4))

    trickbuttons = memory.read_u32(ghost_controller + 0x9C)
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

    # NOTE: We're getting the Game ID here, but we only need the region from it.
    region = utils.get_game_id()

    dbs_address = {"RMCE01": 0x8051c8d8, "RMCP01": 0x80520d4c,
                   "RMCJ01": 0x805206cc, "RMCK01": 0x8050ed70}
    fbs_address = {"RMCE01": 0x8051eacc, "RMCP01": 0x80522f40,
                   "RMCJ01": 0x805228c0, "RMCK01": 0x80510f64}
    tbs_address = {"RMCE01": 0x8051e7e8, "RMCP01": 0x80522c5c,
                   "RMCJ01": 0x805225dc, "RMCK01": 0x80510c80}

    inputs = sequence.frames[core.get_frame_of_input()]

    if inputs and classes.RaceInfo.stage() >= 1:
        # TODO: Handle on script enter
        # If there are inputs on this frame, send the inputs

        # DirectionButtonsStream_readFrame
        # lbz r3, 0x12 (r3)
        # blr
        memory.write_u32(dbs_address[region], 0x88630012)
        memory.write_u32(
            dbs_address[region] + 0x4, 0x4e800020)
        memory.invalidate_icache(dbs_address[region], 0x8)
        # FaceButtonsStream_readFrame
        # lbz r3, 0x12 (r3)
        # blr
        memory.write_u32(fbs_address[region], 0x88630012)
        memory.write_u32(
            fbs_address[region] + 0x4, 0x4e800020)
        memory.invalidate_icache(fbs_address[region], 0x8)
        # TricksButtonStream_readFrame
        # lbz r3, 0x12 (r3)
        # blr
        memory.write_u32(tbs_address[region], 0x88630012)
        memory.write_u32(
            tbs_address[region] + 0x4, 0x4e800020)
        memory.invalidate_icache(tbs_address[region], 0x8)
        set_ghost_buttons(inputs)
    else:
        # TODO: Handle on script exit
        # Restore instructions if no inputs

        # DirectionButtonsStream_readFrame
        # stwu sp, -0x20 (sp)
        # mflr r0
        memory.write_u32(dbs_address[region], 0x9421ffe0)
        memory.write_u32(
            dbs_address[region] + 0x4, 0x7c0802a6)
        memory.invalidate_icache(dbs_address[region], 0x8)
        # FaceButtonsStream_readFrame
        # stwu sp, -0x20 (sp)
        # mflr r0
        memory.write_u32(fbs_address[region], 0x9421ffe0)
        memory.write_u32(
            fbs_address[region] + 0x4, 0x7c0802a6)
        memory.invalidate_icache(fbs_address[region], 0x8)
        # TricksButtonStream_readFrame
        # stwu sp, -0x20 (sp)
        # mflr r0
        memory.write_u32(tbs_address[region], 0x9421ffe0)
        memory.write_u32(
            tbs_address[region] + 0x4, 0x7c0802a6)
        memory.invalidate_icache(tbs_address[region], 0x8)


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
