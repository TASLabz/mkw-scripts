from dolphin import gui, memory, utils
from dataclasses import dataclass
from enum import Enum
import math
import os
from typing import Tuple, List, Optional
import zlib

from .framesequence import FrameSequence
from . import ttk_config

from .mkw_classes import RaceManager, RaceState
from .mkw_classes import GhostController, GhostButtonsStream
from .mkw_classes import InputMgr, GhostWriter, PlayerInput, KartInput, Controller
from .mkw_classes import RaceConfig, RaceConfigScenario, RaceConfigSettings
from .mkw_classes import RaceConfigPlayer, RaceConfigPlayerType

class ControllerInputType(Enum):
    FACE = 0
    DI = 1
    TRICK = 2

class PlayerType(Enum):
    PLAYER = 0
    GHOST = 1
    
def decode_face_button(input):
    A = input % 0x2
    B = (input >> 1) % 0x2
    L = (input >> 2) % 0x2
    
    return [A, B, L]
  
def decode_direction_input(input):
    X = input >> 4
    Y = input % 0x10
    
    return [X, Y]
    
def decode_trick_input(input):
    return input >> 4
    
def encode_face_button(A, B, L, prev_mask):
    x8_mask = 0x0
    if A and B and prev_mask not in (0x0, 0x2, 0x3, 0x7):
        x8_mask = 0x8
    return int(A) + int(B) * 0x2 + int(L) * 0x4 + x8_mask
    
def encode_direction_input(X, Y):
    return (X << 4) + Y
    
def encode_trick_input(input):
    return input * 0x10
    
# Reads binary data in-memory for the specified section
def read_raw_rkg_data(player_type: PlayerType, input_type: ControllerInputType) -> list:
    ret_list = []
    
    # Determine memory region to access
    if (player_type == PlayerType.PLAYER):
        # This assumes player is index 0
        # For now let's assert this is a player
        race_config = RaceConfig()
        race_scenario = RaceConfigScenario(addr=race_config.race_scenario())
        race_config_player = RaceConfigPlayer(addr=race_scenario.player())
        assert(race_config_player.type() == RaceConfigPlayerType.REAL_LOCAL)

        ghost_writer = GhostWriter(addr=PlayerInput.ghost_writer())
        stream_addr = ghost_writer.button_stream(input_type.value)
        button_stream = GhostButtonsStream(addr=stream_addr)
        address = button_stream.buffer()
        end_addr_offset = button_stream.size()
    else:
        # TODO: Ghost is index=1 if you are racing a ghost, but if you watch a replay
        # for example, the ghost is index 0. We want to support this scenario, so
        # we'll need to determine how to set controller_idx appropriately.
        ghost_addr = InputMgr.ghost_controller(1)
        ghost_controller = GhostController(addr=ghost_addr)
        stream_addr = ghost_controller.buttons_stream(input_type.value)
        ghost_button_stream = GhostButtonsStream(addr=stream_addr)
        address = ghost_button_stream.buffer()
        end_addr_offset = ghost_button_stream.size()
    
    # Define the address range for the given input_type
    cur_addr = address
    end_addr = cur_addr + end_addr_offset

    # Begin reading the data
    data_tuple = memory.read_u16(cur_addr)
    while True:
        ret_list += divmod(data_tuple, 0x100)
        cur_addr += 0x2
        data_tuple = memory.read_u16(cur_addr)
        
        if (data_tuple == 0x0000 or cur_addr >= end_addr):
            break
    
    return ret_list
    
# Expand raw rkg data into a list of frames
def decode_rkg_data(data: list, input_type: ControllerInputType) -> List[List[int]]:
    ret_list = []
    
    if (input_type == ControllerInputType.TRICK):
        trick_input = 0x0
        x100_length = 0x0
        
        for i in range(0, len(data)):
            data_byte = data[i]
            
            if (i %2) == 0:
                trick_input = decode_trick_input(data_byte)
                x100_length = data_byte % 0x10
            else:
                dataLength = x100_length * 0x100 + data_byte
                ret_list += [trick_input] * dataLength
    else:
        rawInput = 0x0
        for i in range(0, len(data)):
            data_byte = data[i]
            
            if (i %2) == 0:
                rawInput = data_byte
            else:
                if (input_type == ControllerInputType.FACE):
                    ret_list += [decode_face_button(rawInput)] * data_byte
                else:
                    inputs = decode_direction_input(rawInput)
                    ret_list += [list(map(lambda x: x-7, inputs))] * data_byte
    return ret_list

# Transform raw RKG data into a FrameSequence
def read_full_decoded_rkg_data(player_type: PlayerType) -> Optional[FrameSequence]:
    # First make sure we're actually in a race, otherwise we need to bail out
    race_state = RaceManager.state()
    if (race_state.value < RaceState.COUNTDOWN.value):
        gui.add_osd_message("Not in race!")
        return None
    elif (race_state.value == RaceState.FINISHED_RACE.value):
        gui.add_osd_message("Race is over!")
        return None

    # Read each of the input types
    face_data = read_raw_rkg_data(player_type, ControllerInputType.FACE)
    di_data = read_raw_rkg_data(player_type, ControllerInputType.DI)
    trick_data = read_raw_rkg_data(player_type, ControllerInputType.TRICK)
    if not face_data or not di_data or not trick_data:
        return None
    
    # Expand into a list where each index is a frame
    face_data = decode_rkg_data(face_data, ControllerInputType.FACE)
    di_data = decode_rkg_data(di_data, ControllerInputType.DI)
    trick_data = decode_rkg_data(trick_data, ControllerInputType.TRICK)
    
    # Now transform into a framesequence
    sequence_list = [face_data[x] + di_data[x] + [trick_data[x]] for x in range(len(face_data))]
    sequence = FrameSequence()
    sequence.read_from_list(sequence_list)
    return sequence

@dataclass
class RKGTuple:
    data: int
    frames: int
    
    def __bytes__(self):
        return bytes([self.data, self.frames])

def encode_tuple(input: int, frames: int, input_type: ControllerInputType) -> RKGTuple:
    if (input_type == ControllerInputType.TRICK):
        return RKGTuple(input + (frames >> 8), frames % 0x100)
    else:
        return RKGTuple(input, frames)

def encode_rkg_data_type(input_list: FrameSequence,
                      input_type: ControllerInputType) -> List[RKGTuple]:
    ret_data = []
    prev_input = 0
    bytes = 0
    curr_frames = 0
    is_face = (input_type == ControllerInputType.FACE)
    is_di = (input_type == ControllerInputType.DI)
    is_trick = (input_type == ControllerInputType.TRICK)
    
    input = input_list[0]
    if (is_face):
        prev_input = encode_face_button(input.accel, input.brake, input.item, 0x0)
    elif (is_di):
        prev_input = encode_direction_input(input.stick_x + 7, input.stick_y + 7)
    else:
        prev_input = encode_trick_input(input.dpad_raw())
    
    for input in input_list:
        curr_input = 0
        if (is_face):
            curr_input = encode_face_button(input.accel, input.brake,
                                         input.item, prev_input)
        elif (is_di):
            curr_input = encode_direction_input(input.stick_x + 7, input.stick_y + 7)
        else:
            curr_input = encode_trick_input(input.dpad_raw())
        
        frameLimit = 0xFFF if is_trick else 0xFF
        if (prev_input != curr_input or curr_frames >= frameLimit):
            ret_data.append(encode_tuple(prev_input, curr_frames, input_type))
            curr_frames = 1
            bytes += 1
            prev_input = curr_input
        else:
            curr_frames += 1
    ret_data.append(encode_tuple(prev_input, curr_frames, input_type))
    bytes += 1
    
    return ret_data

def encode_rkg_data(input_list: FrameSequence) -> Tuple[List[int], List[int]]:
    face_tuples = encode_rkg_data_type(input_list, ControllerInputType.FACE)
    di_tuples = encode_rkg_data_type(input_list, ControllerInputType.DI)
    trick_tuples = encode_rkg_data_type(input_list, ControllerInputType.TRICK)
    
    all_tuples = face_tuples+di_tuples+trick_tuples
    tuple_lengths = [len(x) for x in (face_tuples, di_tuples, trick_tuples)]
    return all_tuples, tuple_lengths
    
def createRKGFile(input_data: FrameSequence, track_id: int,
                  vehicle_id: int, character_id: int, drift_id: int) -> bytearray:
    tuples, lengths = encode_rkg_data(input_data)
    tuples_face, tuples_di, tuples_trick = lengths
    data_index = sum(lengths) * 2
    input_length = data_index + 8
    byte_nr8 = (vehicle_id << 2) + ((character_id >> 4) & 0x3)
    byte_nr9 = (character_id << 4) & 0xFF
    byte_nrd = 0x4 + (drift_id << 1)
    
    # TODO: Read from timer classes (referencing has_finished()) in order to set the
    # lap times in the header. Right now they are hard-coded.
    file_header = \
        [0x54, 0xA8, 0x2A, track_id << 2, byte_nr8, byte_nr9, 0x02, 0x10, 0x00, byte_nrd,
        *divmod(input_length, 0x100) ,0x03, 0x54, 0x00, 0x00, 0x00, 0xA8, 0x00, 0x00,
        0x00, 0x2A, 0x00, 0x00 ,0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0xAA, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
    
    mii_data = memory.read_bytes(0x90000020, 0x4C)
    
    input_header = [*divmod(tuples_face, 0x100), *divmod(tuples_di, 0x100),
                   *divmod(tuples_trick, 0x100), 0x00, 0x00]
    
    try:
        id_bytes = bytearray("RKGD", "utf-8")
        file_header_bytes = bytearray(file_header)
        input_header_bytes = bytearray(input_header)
        tuple_bytes = bytearray()
        for tuple in tuples:
            tuple_bytes += bytes(tuple)
        # Pad the rest of the file
        pad_bytes = bytearray(0x276C - data_index)
        
        file_bytes = id_bytes + file_header_bytes + mii_data
        file_bytes += input_header_bytes + tuple_bytes + pad_bytes
        
        crc = zlib.crc32(file_bytes)
        arg1 = math.floor(crc / 0x1000000)
        arg2 = math.floor((crc & 0x00FF0000) / 0x10000)
        arg3 = math.floor((crc & 0x0000FF00) / 0x100)
        arg4 = math.floor(crc % 0x100)
        
        
        file_bytes += bytearray([arg1, arg2, arg3, arg4])
    
        return file_bytes
    except ValueError:
        gui.add_osd_message("Attempted to parse byte > 0xFF! Aborting RKG write.")
        return bytearray()
    
# This is a tiny helper function that prevents slight repetition in filepath lookups
def write_to_csv(inputs: FrameSequence, player_type: PlayerType) -> None:
    # Get csv file path
    player_str = "Player" if player_type == PlayerType.PLAYER else "Ghost"
    relative_path = ttk_config.text_file_path(player_str)
    absolute_path = os.path.join(utils.get_script_dir(), relative_path)
    
    # Write to csv, error if cannot write
    if inputs.write_to_file(absolute_path):
        gui.add_osd_message("{} inputs written to {}".format(player_str, relative_path))
    else:
        gui.add_osd_message(
            "{} is currently locked by another program.".format(relative_path)
        )
        
def write_to_backup_csv(inputs: FrameSequence, backup_number: int) -> None:
    relative_path = ttk_config.text_file_path("Backup")
    relative_path = relative_path.replace("##", "{:02d}".format(backup_number))
    inputs.write_to_file(os.path.join(utils.get_script_dir(), relative_path))
        
def get_metadata_and_write_to_rkg(inputs: FrameSequence, player_type: PlayerType) -> None:
    # Get metadata
    race_config_scenario = RaceConfigScenario(addr=RaceConfig.race_scenario())
    race_config_settings = RaceConfigSettings(addr=race_config_scenario.settings())
    race_config_player = RaceConfigPlayer(addr=race_config_scenario.player())
    player_input = PlayerInput(player_idx=0)
    kart_input = KartInput(player_input.kart_input())
    controller = Controller(addr=kart_input.race_controller())

    track_id = race_config_settings.course_id().value
    vehicle_id = race_config_player.vehicle_id().value
    character_id = race_config_player.character_id().value
    drift_id = int(controller.drift_is_auto())
    
    # Get bytes to write
    file_bytes = createRKGFile(inputs, track_id, vehicle_id, character_id, drift_id)
    
    if (len(file_bytes)):
        # Write bytes to appropriate file
        write_to_rkg(file_bytes, player_type)
    else:
        gui.add_osd_message("No bytes to write to RKG file.")
        
def write_to_rkg(file_bytes: bytearray, player_type: PlayerType) -> None:
    # Get csv file path
    player_str = "Player" if player_type == PlayerType.PLAYER else "Ghost"
    relative_path = ttk_config.rkg_file_path[player_str]
    absolute_path = os.path.join(utils.get_script_dir(), relative_path)
    
    try:
        with open(absolute_path, "wb") as f:
            f.write(file_bytes)
        gui.add_osd_message("{} inputs written to {}".format(player_str, relative_path))
    except IOError:
        gui.add_osd_message(
            "{} is currently locked by another program.".format(relative_path)
        )
        
def get_input_sequence_from_csv(player_type: PlayerType) -> FrameSequence:
    # Get csv file path
    player_str = "Player" if player_type == PlayerType.PLAYER else "Ghost"
    relative_path = ttk_config.text_file_path(player_str)
    absolute_path = os.path.join(utils.get_script_dir(), relative_path)
    
    # Get the frame sequence
    return FrameSequence(absolute_path)

def get_controller_calc():
    address = {"RMCE01": 0x8051a8a0, "RMCP01": 0x8051ed14,
               "RMCJ01": 0x8051e694, "RMCK01": 0x8050cd38}
    return address[utils.get_game_id()]

def get_memcpy_branch():
    instr = {"RMCE01": 0x4bcb6c91, "RMCP01": 0x4bcb28bd,
             "RMCJ01": 0x4bcb2e5d, "RMCK01": 0x4bcc4bf5}
    return instr[utils.get_game_id()]

controller_calc = get_controller_calc()
memcpy_branch = get_memcpy_branch()

def controller_patch() -> None:
    # lbz r15, 0x18 (r31)
    
    # lbz r14, 0x4d (r31) #buttons
    # addic. r14, r14, -0x80
    # blt donotttk
    # stb r14, 0x4d (r31)
    # sth r14, 0x8 (r31)
    
    # addi r3, r31, 0x4
    # lbz r4, 0x4e (r31)
    # bl InputState_setStickXMirrored
    # addi r3, r31, 0x4
    # lbz r4, 0x4f (r31)
    # bl InputState_setStickY
    # addi r3, r31, 0x4
    # lbz r4, 0x52 (r31)
    # bl RaceInputState_setTrick
    # donotttk:
    # rlwinm. r15, r15, 0x19, 0x1f, 0x1f
    # bne dontignoreeverything
    
    # addi r3, r31, 0x8
    # addi r4, r1, 0xc
    # li r5, 0x10
    # bl NETMemCpy
    
    patch_ptr = controller_calc + 0x1d8
    if (memory.read_u32(patch_ptr) == 0x881f0018):
        memory.write_u32(patch_ptr, 0x89ff0018)
        memory.write_u32(patch_ptr + 0x4, 0x89df004d)
        memory.write_u32(patch_ptr + 0x8, 0x35ceff80)
        memory.write_u32(patch_ptr + 0xc, 0x41800030)
        memory.write_u32(patch_ptr + 0x10, 0x99df004d)
        memory.write_u32(patch_ptr + 0x14, 0xb1df0008)
        memory.write_u32(patch_ptr + 0x18, 0x387f0004)
        memory.write_u32(patch_ptr + 0x1c, 0x889f004e)
        memory.write_u32(patch_ptr + 0x20, 0x4bfffa55)
        memory.write_u32(patch_ptr + 0x24, 0x387f0004)
        memory.write_u32(patch_ptr + 0x28, 0x889f004f)
        memory.write_u32(patch_ptr + 0x2c, 0x4bfffb49)
        memory.write_u32(patch_ptr + 0x30, 0x387f0004)
        memory.write_u32(patch_ptr + 0x34, 0x889f0052)
        memory.write_u32(patch_ptr + 0x38, 0x4bfffc45)
        memory.write_u32(patch_ptr + 0x3c, 0x55efcfff)
        memory.write_u32(patch_ptr + 0x40, 0x40820014)
        memory.write_u32(patch_ptr + 0x44, 0x387f0008)
        memory.write_u32(patch_ptr + 0x48, 0x3881000c)
        memory.write_u32(patch_ptr + 0x4c, 0x38a00010)
        memory.write_u32(patch_ptr + 0x50, memcpy_branch)
        memory.invalidate_icache(patch_ptr, 0x54)

def write_ghost_inputs(inputs: FrameSequence) -> None:
    controller_patch()
    # TODO: This assumes the ghost is index 1, which is only true when racing a ghost
    controller = Controller(addr=InputMgr.ghost_controller(1))
    set_buttons(inputs, controller)

def write_player_inputs(inputs: FrameSequence) -> None:
    controller_patch()
    kart_input = KartInput(addr=PlayerInput.kart_input())
    controller = Controller(addr=kart_input.race_controller())
    set_buttons(inputs, controller)

def set_buttons(inputs, controller : Controller):
    """This writes button data to addresses with implicit padding in structs.
       This must be called only after controller_patch()"""
    addr = controller.addr
    memory.write_u8(addr + 0x4d, inputs.accel + (inputs.brake << 1) +
                    (inputs.item << 2) | ((inputs.accel & inputs.brake) << 3) + 0x80)
    memory.write_u8(addr + 0x4e, inputs.stick_x + 7)
    memory.write_u8(addr + 0x4f, inputs.stick_y + 7)
    memory.write_u8(addr + 0x52, inputs.dpad_raw())
