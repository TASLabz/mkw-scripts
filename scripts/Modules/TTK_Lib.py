from dolphin import gui, memory, utils
from dataclasses import dataclass
from enum import Enum
import math
import os
from typing import Tuple, List, Optional
import zlib

from .framesequence import FrameSequence
from . import TTK_config

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
    
def decodeFaceButton(input):
    A = input % 0x2
    B = (input >> 1) % 0x2
    L = (input >> 2) % 0x2
    
    return [A, B, L]
  
def decodeDirectionInput(input):
    X = input >> 4
    Y = input % 0x10
    
    return [X, Y]
    
def decodeTrickInput(input):
    return input >> 4
    
def encodeFaceButton(A, B, L, prevMask):
    x8Mask = 0x0
    if A and B and prevMask not in (0x0, 0x2, 0x3, 0x7):
        x8Mask = 0x8
    return int(A) + int(B) * 0x2 + int(L) * 0x4 + x8Mask
    
def encodeDirectionInput(X, Y):
    return (X << 4) + Y
    
def encodeTrickInput(input):
    return input * 0x10
    
# Reads binary data in-memory for the specified section
def readRawRKGData(playerType: PlayerType, inputType: ControllerInputType) -> list:
    retList = []
    
    # Determine memory region to access
    if (playerType == PlayerType.PLAYER):
        # This assumes player is index 0
        # For now let's assert this is a player
        race_config = RaceConfig()
        race_scenario = RaceConfigScenario(addr=race_config.race_scenario())
        race_config_player = RaceConfigPlayer(addr=race_scenario.player(playerIdx=0))
        assert(race_config_player.type() == RaceConfigPlayerType.REAL_LOCAL)

        ghost_writer = GhostWriter(addr=PlayerInput.ghost_writer())
        stream_addr = ghost_writer.button_stream(inputType.value)
        button_stream = GhostButtonsStream(addr=stream_addr)
        address = button_stream.buffer()
        endAddrOffset = button_stream.size()
    else:
        # TODO: Ghost is index=1 if you are racing a ghost, but if you watch a replay
        # for example, the ghost is index 0. We want to support this scenario, so
        # we'll need to determine how to set controllerIdx appropriately.
        ghost_addr = InputMgr.ghost_controller(controllerIdx=1)
        ghost_controller = GhostController(addr=ghost_addr)
        stream_addr = ghost_controller.buttons_stream(inputType.value)
        ghost_button_stream = GhostButtonsStream(addr=stream_addr)
        address = ghost_button_stream.buffer()
        endAddrOffset = ghost_button_stream.size()
    
    # Define the address range for the given inputType
    curAddr = address
    endAddr = curAddr + endAddrOffset

    # Begin reading the data
    dataTuple = memory.read_u16(curAddr)
    while True:
        retList += divmod(dataTuple, 0x100)
        curAddr += 0x2
        dataTuple = memory.read_u16(curAddr)
        
        if (dataTuple == 0x0000 or curAddr >= endAddr):
            break
    
    return retList
    
# Expand raw rkg data into a list of frames
def decodeRKGData(data: list, inputType: ControllerInputType) -> List[List[int]]:
    retList = []
    
    if (inputType == ControllerInputType.TRICK):
        trickInput = 0x0
        x100Length = 0x0
        
        for i in range(0, len(data)):
            dataByte = data[i]
            
            if (i %2) == 0:
                trickInput = decodeTrickInput(dataByte)
                x100Length = dataByte % 0x10
            else:
                dataLength = x100Length * 0x100 + dataByte
                retList += [trickInput] * dataLength
    else:
        rawInput = 0x0
        for i in range(0, len(data)):
            dataByte = data[i]
            
            if (i %2) == 0:
                rawInput = dataByte
            else:
                if (inputType == ControllerInputType.FACE):
                    retList += [decodeFaceButton(rawInput)] * dataByte
                else:
                    inputs = decodeDirectionInput(rawInput)
                    retList += [list(map(lambda x: x-7, inputs))] * dataByte
    return retList

# Transform raw RKG data into a FrameSequence
def readFullDecodedRKGData(playerType: PlayerType) -> Optional[FrameSequence]:
    # First make sure we're actually in a race, otherwise we need to bail out
    race_state = RaceManager.state()
    if (race_state.value < RaceState.COUNTDOWN.value):
        gui.add_osd_message("Not in race!")
        return None
    elif (race_state.value == RaceState.FINISHED_RACE.value):
        gui.add_osd_message("Race is over!")
        return None

    # Read each of the input types
    faceData = readRawRKGData(playerType, ControllerInputType.FACE)
    diData = readRawRKGData(playerType, ControllerInputType.DI)
    trickData = readRawRKGData(playerType, ControllerInputType.TRICK)
    if not faceData or not diData or not trickData:
        return None
    
    # Expand into a list where each index is a frame
    faceData = decodeRKGData(faceData, ControllerInputType.FACE)
    diData = decodeRKGData(diData, ControllerInputType.DI)
    trickData = decodeRKGData(trickData, ControllerInputType.TRICK)
    
    # Now transform into a framesequence
    list = [faceData[x] + diData[x] + [trickData[x]] for x in range(len(faceData))]
    sequence = FrameSequence()
    sequence.readFromList(list)
    return sequence

@dataclass
class RKGTuple:
    data: int
    frames: int
    
    def __bytes__(self):
        return bytes([self.data, self.frames])

def encodeTuple(input: int, frames: int, inputType: ControllerInputType) -> RKGTuple:
    if (inputType == ControllerInputType.TRICK):
        return RKGTuple(input + (frames >> 8), frames % 0x100)
    else:
        return RKGTuple(input, frames)

def encodeRKGDataType(inputList: FrameSequence,
                      inputType: ControllerInputType) -> List[RKGTuple]:
    retData = []
    prevInput = 0
    bytes = 0
    currFrames = 0
    isFace = (inputType == ControllerInputType.FACE)
    isDI = (inputType == ControllerInputType.DI)
    isTrick = (inputType == ControllerInputType.TRICK)
    
    input = inputList[0]
    if (isFace):
        prevInput = encodeFaceButton(input.accel, input.brake, input.item, 0x0)
    elif (isDI):
        prevInput = encodeDirectionInput(input.stick_x + 7, input.stick_y + 7)
    else:
        prevInput = encodeTrickInput(input.dpad_raw())
    
    for input in inputList:
        currInput = 0
        if (isFace):
            currInput = encodeFaceButton(input.accel, input.brake,
                                         input.item, prevInput)
        elif (isDI):
            currInput = encodeDirectionInput(input.stick_x + 7, input.stick_y + 7)
        else:
            currInput = encodeTrickInput(input.dpad_raw())
        
        frameLimit = 0xFFF if isTrick else 0xFF
        if (prevInput != currInput or currFrames >= frameLimit):
            retData.append(encodeTuple(prevInput, currFrames, inputType))
            currFrames = 1
            bytes += 1
            prevInput = currInput
        else:
            currFrames += 1
    retData.append(encodeTuple(prevInput, currFrames, inputType))
    bytes += 1
    
    return retData

def encodeRKGData(inputList: FrameSequence) -> Tuple[List[int], List[int]]:
    faceTuples = encodeRKGDataType(inputList, ControllerInputType.FACE)
    diTuples = encodeRKGDataType(inputList, ControllerInputType.DI)
    trickTuples = encodeRKGDataType(inputList, ControllerInputType.TRICK)
    
    allTuples = faceTuples+diTuples+trickTuples
    tupleLengths = [len(x) for x in (faceTuples, diTuples, trickTuples)]
    return allTuples, tupleLengths
    
def createRKGFile(input_data: FrameSequence, trackID: int,
                  vehicleID: int, characterID: int, driftID: int) -> bytearray:
    tuples, lengths = encodeRKGData(input_data)
    tuplesFace, tuplesDI, tuplesTrick = lengths
    dataIndex = sum(lengths) * 2
    inputLength = dataIndex + 8
    byteNr8 = (vehicleID << 2) + ((characterID >> 4) & 0x3)
    byteNr9 = (characterID << 4) & 0xFF
    byteNrD = 0x4 + (driftID << 1)
    
    # TODO: Read from timer classes (referencing has_finished()) in order to set the
    # lap times in the header. Right now they are hard-coded.
    headerData = \
        [0x54, 0xA8, 0x2A, trackID << 2, byteNr8, byteNr9, 0x02, 0x10, 0x00, byteNrD,
        *divmod(inputLength, 0x100) ,0x03, 0x54, 0x00, 0x00, 0x00, 0xA8, 0x00, 0x00,
        0x00, 0x2A, 0x00, 0x00 ,0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0xAA, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xC0, 0x10, 0x00,
        0x54, 0x00, 0x41, 0x00, 0x53, 0x00, 0x54, 0x00, 0x6F, 0x00, 0x6F, 0x00, 0x6C,
        0x00, 0x6B, 0x00, 0x69, 0x00, 0x74, 0x00, 0x22, 0x87, 0x30, 0x89, 0x66, 0xC2,
        0xC4, 0xED, 0xC3, 0x20, 0x44, 0x3C, 0x40, 0x28, 0x38, 0x0C, 0x84, 0x48, 0xCF,
        0x0E, 0x00, 0x08, 0x00, 0xB9, 0x09, 0x00, 0x8A, 0x81, 0x06, 0xC4, 0x10, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x7A, 0x6E, *divmod(tuplesFace, 0x100),
        *divmod(tuplesDI, 0x100), *divmod(tuplesTrick, 0x100), 0x00, 0x00]
    
    try:
        idBytes = bytearray("RKGD", "utf-8")
        headerBytes = bytearray(headerData)
        tupleBytes = bytearray()
        for tuple in tuples:
            tupleBytes += bytes(tuple)
        # Pad the rest of the file
        padBytes = bytearray(0x276C - dataIndex)
        
        fileBytes = idBytes + headerBytes + tupleBytes + padBytes
        
        crc = zlib.crc32(fileBytes)
        arg1 = math.floor(crc / 0x1000000)
        arg2 = math.floor((crc & 0x00FF0000) / 0x10000)
        arg3 = math.floor((crc & 0x0000FF00) / 0x100)
        arg4 = math.floor(crc % 0x100)
        
        
        fileBytes += bytearray([arg1, arg2, arg3, arg4])
    
        return fileBytes
    except ValueError:
        gui.add_osd_message("Attempted to parse byte > 0xFF! Aborting RKG write.")
        return bytearray()
    
# This is a tiny helper function that prevents slight repetition in filepath lookups
def writeToCSV(inputs: FrameSequence, playerType: PlayerType) -> None:
    # Get csv file path
    playerStr = "Player" if playerType == PlayerType.PLAYER else "Ghost"
    relativePath = TTK_config.textFilePath(playerStr)
    absolutePath = os.path.join(utils.get_script_dir(), relativePath)
    
    # Write to csv, error if cannot write
    if inputs.writeToFile(absolutePath):
        gui.add_osd_message("{} inputs written to {}".format(playerStr, relativePath))
    else:
        gui.add_osd_message(
            "{} is currently locked by another program.".format(relativePath)
        )
        
def writeToBackupCSV(inputs: FrameSequence, backupNumber: int) -> None:
    relativePath = TTK_config.textFilePath("Backup")
    relativePath = relativePath.replace("##", "{:02d}".format(backupNumber))
    inputs.writeToFile(os.path.join(utils.get_script_dir(), relativePath))
        
def getMetadataAndWriteToRKG(inputs: FrameSequence, playerType: PlayerType) -> None:
    # Get metadata
    race_config_scenario = RaceConfigScenario(addr=RaceConfig.race_scenario())
    race_config_settings = RaceConfigSettings(addr=race_config_scenario.settings())
    race_config_player = RaceConfigPlayer(addr=race_config_scenario.player(playerIdx=0))
    player_input = PlayerInput(playerIdx=0)
    kart_input = KartInput(player_input.kart_input())
    controller = Controller(addr=kart_input.race_controller())

    trackID = race_config_settings.course_id().value
    vehicleID = race_config_player.vehicle_id().value
    characterID = race_config_player.character_id().value
    driftID = int(controller.drift_is_auto())
    
    # Get bytes to write
    fileBytes = createRKGFile(inputs, trackID, vehicleID, characterID, driftID)
    
    if (len(fileBytes)):
        # Write bytes to appropriate file
        writeToRKG(fileBytes, playerType)
    else:
        gui.add_osd_message("No bytes to write to RKG file.")
        
def writeToRKG(fileBytes: bytearray, playerType: PlayerType) -> None:
    # Get csv file path
    playerStr = "Player" if playerType == PlayerType.PLAYER else "Ghost"
    relativePath = TTK_config.rkgFilePath[playerStr]
    absolutePath = os.path.join(utils.get_script_dir(), relativePath)
    
    try:
        with open(absolutePath, "wb") as f:
            f.write(fileBytes)
        gui.add_osd_message("{} inputs written to {}".format(playerStr, relativePath))
    except IOError:
        gui.add_osd_message(
            "{} is currently locked by another program.".format(relativePath)
        )
        
def getInputSequenceFromCSV(playerType: PlayerType) -> FrameSequence:
    # Get csv file path
    playerStr = "Player" if playerType == PlayerType.PLAYER else "Ghost"
    relativePath = TTK_config.textFilePath(playerStr)
    absolutePath = os.path.join(utils.get_script_dir(), relativePath)
    
    # Get the frame sequence
    return FrameSequence(absolutePath)

def getControllerCalc():
    address = {"RMCE01": 0x8051a8a0, "RMCP01": 0x8051ed14,
               "RMCJ01": 0x8051e694, "RMCK01": 0x8050cd38}
    return address[utils.get_game_id()]

def getMemcpyBranch():
    instr = {"RMCE01": 0x4bcb6c91, "RMCP01": 0x4bcb28bd,
             "RMCJ01": 0x4bcb2e5d, "RMCK01": 0x4bcc4bf5}
    return instr[utils.get_game_id()]

controller_calc = getControllerCalc()
memcpy_branch = getMemcpyBranch()

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

def writeGhostInputs(inputs: FrameSequence) -> None:
    controller_patch()
    # TODO: This assumes the ghost is index 1, which is only true when racing a ghost
    controller = Controller(addr=InputMgr.ghost_controller(controllerIdx=1))
    set_buttons(inputs, controller)

def writePlayerInputs(inputs: FrameSequence) -> None:
    controller_patch()
    kart_input = KartInput(addr=PlayerInput.kart_input(playerIdx=0))
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
