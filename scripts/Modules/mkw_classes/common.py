from dolphin import memory, utils

from dataclasses import dataclass
from enum import Enum
import math
import struct

class RegionError(Exception):
    def __init__(self, message=f"Expected Mario Kart Wii game ID (RMCX01), " \
                                 f"got {utils.get_game_id()}"):
        super().__init__(message)

@dataclass
class vec2:
    x: float = 0.0
    y: float = 0.0

    def __add__(self, other):
        return vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return vec2(self.x - other.x, self.y - other.y)

    @staticmethod
    def read(ptr) -> "vec2":
        bytes = memory.read_bytes(ptr, 0x8)
        return vec2(*struct.unpack('>' + 'f'*2, bytes))

@dataclass
class vec3:
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

    def __add__(self, other):
        return vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def norm_xyz(self) -> float:
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def norm_xz(self) -> float:
        return math.sqrt(self.x**2 + self.z**2)

    @staticmethod
    def read(ptr) -> "vec3":
        bytes = memory.read_bytes(ptr, 0xC)
        return vec3(*struct.unpack('>' + 'f'*3, bytes))

@dataclass
class mat34:
    e00: float = 0.0
    e01: float = 0.0
    e02: float = 0.0
    e03: float = 0.0
    e10: float = 0.0
    e11: float = 0.0
    e12: float = 0.0
    e13: float = 0.0
    e20: float = 0.0
    e21: float = 0.0
    e22: float = 0.0
    e23: float = 0.0

    @staticmethod
    def read(ptr) -> "mat34":
        bytes = memory.read_bytes(ptr, 0x30)
        return mat34(*struct.unpack('>' + 'f'*12, bytes))

@dataclass
class quatf:
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    w: float = 0.0

    @staticmethod
    def read(ptr) -> "quatf":
        bytes = memory.read_bytes(ptr, 0x10)
        return quatf(*struct.unpack('>' + 'f'*4, bytes))

@dataclass
class ExactTimer:
    """This is used in conjunction with the Exact Finish Code.
       This is not the internal timer class. For that, see timer.py"""
    min: int
    sec: int
    mil: float

    def __add__(self, rhs):
        ret = ExactTimer(self.min, self.sec, self.mil)
        ret.min += rhs.min
        ret.sec += rhs.sec
        ret.mil += rhs.mil
        ret.normalize()
        return ret

    def __sub__(self, rhs):
        ret = ExactTimer(self.min, self.sec, self.mil)
        ret.min -= rhs.min
        ret.sec -= rhs.sec
        ret.mil -= rhs.mil
        ret.normalize()
        return ret

    def normalize(self) -> None:
        carry, self.mil = divmod(self.mil, 1000)
        self.sec += carry
        carry, self.sec = divmod(self.sec, 60)
        self.min += int(carry)

    def __str__(self):
        return "{:02d}:{:012.9f}".format(self.min, self.sec + self.mil)

class CupId(Enum):
    MUSHROOM_CUP = 0
    FLOWER_CUP = 1
    STAR_CUP = 2
    SPECIAL_CUP = 3
    SHELL_CUP = 4
    BANANA_CUP = 5
    LEAF_CUP = 6
    LIGHTNING_CUP = 7

class CourseId(Enum):
    MARIO_CIRCUIT = 0
    MOO_MOO_MEADOWS = 1
    MUSHROOM_GORGE = 2
    GRUMBLE_VOLCANO = 3
    TOADS_FACTORY = 4
    COCONUT_MALL = 5
    DK_SNOWBOARD_CROSS = 6
    WARIOS_GOLD_MINE = 7
    LUIGI_CIRCUIT = 8
    DAISY_CIRCUIT = 9
    MOONVIEW_HIGHWAY = 10
    MAPLE_TREEWAY = 11
    BOWSERS_CASTLE = 12
    RAINBOW_ROAD = 13
    DRY_DRY_RUINS = 14
    KOOPA_CAPE = 15
    GCN_PEACH_BEACH = 16
    GCN_MARIO_CIRCUIT = 17
    GCN_WALUIGI_STADIUM = 18
    GCN_DK_MOUNTAIN = 19
    DS_YOSHI_FALLS = 20
    DS_DESERT_HILLS = 21
    DS_PEACH_GARDENS = 22
    DS_DELFINO_SQUARE = 23
    SNES_MARIO_CIRCUIT_3 = 24
    SNES_GHOST_VALLEY_2 = 25
    N64_MARIO_RACEWAY = 26
    N64_SHERBET_LAND = 27
    N64_BOWSERS_CASTLE = 28
    N64_DKS_JUNGLE_PARKWAY = 29
    GBA_BOWSER_CASTLE_3 = 30
    GBA_SHY_GUY_BEACH = 31
    DELFINO_PIER = 32
    BLOCK_PLAZA = 33
    CHAIN_CHOMP_ROULETTE = 34
    FUNKY_STADIUM = 35
    THWOMP_DESERT = 36
    GCN_COOKIE_LAND = 37
    DS_TWILIGHT_HOUSE = 38
    SNES_BATTLE_COURSE_4 = 39
    GBA_BATTLE_COURSE_3 = 40
    N64_SKYSCRAPER = 41

class VehicleId(Enum):
    STANDARD_KART_S = 0
    STANDARD_KART_M = 1
    STANDARD_KART_L = 2
    BOOSTER_SEAT = 3
    CLASSIC_DRAGSTER = 4
    OFFROADER = 5
    MINI_BEAST = 6
    WILD_WING = 7
    FLAME_FLYER = 8
    CHEEP_CHARGER = 9
    SUPER_BLOOPER = 10
    PIRANHA_PROWLER = 11
    TINY_TITAN = 12
    DAYTRIPPER = 13
    JETSETTER = 14
    BLUE_FALCON = 15
    SPRINTER = 16
    HONEYCOUPE = 17
    STANDARD_BIKE_S = 18
    STANDARD_BIKE_M = 19
    STANDARD_BIKE_L = 20
    BULLET_BIKE = 21
    MACH_BIKE = 22
    FLAME_RUNNER = 23
    BIT_BIKE = 24
    SUGARSCOOT = 25
    WARIO_BIKE = 26
    QUACKER = 27
    ZIP_ZIP = 28
    SHOOTING_STAR = 29
    MAGIKRUISER = 30
    SNEAKSTER = 31
    SPEAR = 32
    JET_BUBBLE = 33
    DOLPHIN_DASHER = 34
    PHANTOM = 35

class CharacterId(Enum):
    MARIO = 0
    BABY_PEACH = 1
    WALUIGI = 2
    BOWSER = 3
    BABY_DAISY = 4
    DRY_BONES = 5
    BABY_MARIO = 6
    LUIGI = 7
    TOAD = 8
    DONKEY_KONG = 9
    YOSHI = 10
    WARIO = 11
    BABY_LUIGI = 12
    TOADETTE = 13
    KOOPA_TROOPA = 14
    DAISY = 15
    PEACH = 16
    BIRDO = 17
    DIDDY_KONG = 18
    KING_BOO = 19
    BOWSER_JR = 20
    DRY_BOWSER = 21
    FUNKY_KONG = 22
    ROSALINA = 23
    SMALL_MII_A_MALE = 24
    SMALL_MII_A_FEMALE = 25
    SMALL_MII_B_MALE = 26
    SMALL_MII_B_FEMALE = 27
    SMALL_MII_C_MALE = 28
    SMALL_MII_C_FEMALE = 29
    MEDIUM_MII_A_MALE = 30
    MEDIUM_MII_A_FEMALE = 31
    MEDIUM_MII_B_MALE = 32
    MEDIUM_MII_B_FEMALE = 33
    MEDIUM_MII_C_MALE = 34
    MEDIUM_MII_C_FEMALE = 35
    LARGE_MII_A_MALE = 36
    LARGE_MII_A_FEMALE = 37
    LARGE_MII_B_MALE = 38
    LARGE_MII_B_FEMALE = 39
    LARGE_MII_C_MALE = 40
    LARGE_MII_C_FEMALE = 41
    MEDIUM_MII = 42
    SMALL_MII = 43
    LARGE_MII = 44
    PEACH_MENU = 45  # biker outfit
    DAISY_MENU = 46  # biker outfit
    ROSALINA_MENU = 47  # biker outfit
    
class WheelCount(Enum):
    _4_WHEELS = 0
    _2_WHEELS = 1
    _2_WHEELS_QUACKER = 2
    _3_WHEELS_BLUE_FALCON = 3

class VehicleType(Enum):
    OUTSIDE_DRIFTING_KART = 0
    OUTSIDE_DRIFTING_BIKE = 1
    INSIDE_DRIFTING_BIKE = 2

class RaceConfigPlayerType(Enum):
    REAL_LOCAL = 0
    CPU = 1
    UNKNOWN = 2  # Most likely never set
    GHOST = 3
    REMOTE = 4
    NONE = 5

class SpecialFloor(Enum):
    BOOST_PANEL = 1
    BOOST_RAMP = 2
    JUMP_PAD = 4

class TrickType(Enum):
    STUNT_TRICK_BASIC = 0
    BIKE_FLIP_TRICK_NOSE = 1
    BIKE_FLIP_TRICK_TAIL = 2
    FLIP_TRICK_Y_LEFT = 3
    FLIP_TRICK_Y_RIGHT = 4
    KART_FLIP_TRICK_Z = 5
    BIKE_SIDE_STUNT_TRICK = 6

class SurfaceProperties():
    def __init__(self, value):
        self.value = value

    WALL = 0x1
    SOLID_OOB = 0x2
    BOOST_RAMP = 0x10
    OFFROAD = 0x40
    BOOST_PANEL_OR_RAMP = 0x100
    TRICKABLE = 0x800
