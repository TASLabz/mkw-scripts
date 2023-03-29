from dolphin import memory
from dataclasses import dataclass
import math
import mkw_classes as classes
import mkw_translations as translate

# NOTE (xi): wait for get_game_id() to be put in dolphin.memory before clearing
#  these commented-out lines:

# class RegionError(Exception):
#    def __init__(self, message=f"Expected Mario Kart Wii game ID (RMCX01), got {get_game_id()}"):
#        super().__init__(message)

# TODO: put in dolphin.memory


def get_game_id():
    game_id = ""
    for i in range(6):
        game_id += chr(memory.read_u8(0x80000000 + i))
    return game_id


def is_mkw() -> bool:
    game = get_game_id()
    valid_ids = ["RMCE01", "RMCP01", "RMCJ01", "RMCK01"]
    return game in valid_ids

# TODO: put in dolphin.memory
# chase pointer chains


def chase_pointer(base_address, offsets, data_type):
    current_address = memory.read_u32(base_address)
    for offset in offsets:
        value_address = current_address + offset
        current_address = memory.read_u32(current_address + offset)
    data_types = {
        'u8': memory.read_u8,
        'u16': memory.read_u16,
        'u32': memory.read_u32,
        'u64': memory.read_u64,
        's8': memory.read_s8,
        's16': memory.read_s16,
        's32': memory.read_s32,
        's64': memory.read_s64,
        'f32': memory.read_f32,
        'f64': memory.read_f64
    }
    return data_types[data_type](value_address)

# used in input display


def calc_stick_pos(center, bounding_radius, stick_x, stick_y, move_radius):
    x = 0
    y = 0
    stick_x -= 127
    stick_y -= 127
    x, y = (center[0] + (bounding_radius * (stick_x / 127)),
            center[1] - (bounding_radius * (stick_y / 127)))

    if (x < center[0] - bounding_radius - move_radius):
        x = center[0] - bounding_radius - move_radius
    elif (x > center[0] + bounding_radius + move_radius):
        x = center[0] + bounding_radius + move_radius
    if (y < center[1] - bounding_radius - move_radius):
        y = center[1] - bounding_radius - move_radius
    elif (y > center[1] + bounding_radius + move_radius):
        y = center[1] + bounding_radius + move_radius

    return (x, y)


def get_frame_of_input():
    id = get_game_id()
    address = {"RMCE01": 0x809BF0B8, "RMCP01": 0x809C38C0,
               "RMCJ01": 0x809C2920, "RMCK01": 0x809B1F00}
    return memory.read_u32(address[id])


@dataclass
class speed:
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    xz: float = 0.0
    xyz: float = 0.0


def get_speed(playerIdx=0):
    x = classes.VehiclePhysics.pos().x - classes.VehicleDynamics.pos().x
    y = classes.VehiclePhysics.pos().y - classes.VehicleDynamics.pos().y
    z = classes.VehiclePhysics.pos().z - classes.VehicleDynamics.pos().z
    xz = math.sqrt(x ** 2 + z ** 2)
    xyz = math.sqrt(x ** 2 + y ** 2 + z ** 2)

    return speed(x, y, z, xz, xyz)
