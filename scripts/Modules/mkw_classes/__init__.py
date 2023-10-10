# Import all class objects so that they are accessible just by importing
# from mkw_classes rather than each individual file.

# Imports are ordered in terms of dependency.
# Improper ordering can lead to circular dependencies.

# Ignore unused import warnings from the linter
# noqa: F401

from .common import RegionError
from .common import vec2, vec3, mat34, quatf
from .common import ExactTimer
from .common import CupId, CourseId, VehicleId, CharacterId, WheelCount, VehicleType
from .common import SpecialFloor, TrickType, SurfaceProperties, RaceConfigPlayerType

from .input_mgr import InputMgr
from .player_input import PlayerInput
from .kart_input import KartInput
from .controller import Controller
from .race_input_state import RaceInputState, ButtonActions
from .ui_input_state import UIInputState
from .controller_info import ControllerInfo
from .ghost_writer import GhostWriter
from .ghost_buttons_stream import GhostButtonsStream
from .ai_input import AiInput
from .ghost_controller import GhostController

from .race_config import RaceConfig
from .race_config_scenario import RaceConfigScenario
from .race_config_player import RaceConfigPlayer
from .race_config_settings import RaceConfigSettings, RaceConfigEngineClass
from .race_config_settings import RaceConfigGameMode, RaceConfigGameType
from .race_config_settings import RaceConfigModeFlags
from .competition_settings import CompetitionSettings

from .kart_object_manager import KartObjectManager
from .kart_object import KartObject
from .kart_sub import KartSub
from .kart_settings import KartSettings
from .kart_move import KartMove
from .kart_boost import KartBoost, BoostType
from .kart_jump import KartJump
from .kart_half_pipe import KartHalfPipe
from .kart_action import KartAction
from .kart_collide import KartCollide
from .kart_state import KartState
from .kart_param import KartParam
from .player_stats import PlayerStats
from .gp_stats import GpStats
from .race_stats import RaceStats
from .bsp import BSP
from .kart_body import KartBody
from .vehicle_dynamics import VehicleDynamics
from .vehicle_physics import VehiclePhysics

from .race_manager import RaceManager, RaceState
from .time_manager import TimerManager
from .timer import Timer
from .race_manager_player import RaceManagerPlayer