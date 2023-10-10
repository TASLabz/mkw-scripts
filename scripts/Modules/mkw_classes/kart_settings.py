from dolphin import memory

from . import KartObject, VehicleId, CharacterId

class KartSettings:
    def __init__(self, playerIdx=0, addr=None):
        self.addr = addr if addr else KartSettings.chain(playerIdx)

        self.is_bike = self.inst_is_bike
        self.vehicle = self.inst_vehicle
        self.character = self.inst_character
        self.susp_count = self.inst_susp_count
        self.tire_count = self.inst_tire_count
        self.kart_param = self.inst_kart_param
        self.gp_stats = self.inst_gp_stats
        self.race_stats = self.inst_race_stats

    @staticmethod
    def chain(playerIdx=0) -> int:
        return KartObject.kart_settings(playerIdx)

    @staticmethod
    def is_bike(playerIdx=0) -> int:
        kart_settings_ref = KartSettings.chain(playerIdx)
        is_bike_ref = kart_settings_ref + 0x0
        return memory.read_u32(is_bike_ref)

    def inst_is_bike(self) -> int:
        is_bike_ref = self.addr + 0x0
        return memory.read_u32(is_bike_ref)

    @staticmethod
    def vehicle(playerIdx=0) -> VehicleId:
        """It's fewer computations to use RaceConfig.vehicle() instead"""
        kart_settings_ref = KartSettings.chain(playerIdx)
        vehicle_id_ref = kart_settings_ref + 0x4
        return VehicleId(memory.read_u32(vehicle_id_ref))

    def inst_vehicle(self) -> VehicleId:
        """It's fewer computations to use RaceConfig.vehicle() instead"""
        vehicle_id_ref = self.addr + 0x4
        return VehicleId(memory.read_u32(vehicle_id_ref))

    @staticmethod
    def character(playerIdx=0) -> CharacterId:
        """It's fewer computations to use RaceConfig.character() instead"""
        kart_settings_ref = KartSettings.chain(playerIdx)
        character_id_ref = kart_settings_ref + 0x8
        return CharacterId(memory.read_u32(character_id_ref))

    def inst_character(self) -> CharacterId:
        """It's fewer computations to use RaceConfig.character() instead"""
        character_id_ref = self.addr + 0x8
        return CharacterId(memory.read_u32(character_id_ref))

    @staticmethod
    def susp_count(playerIdx=0) -> int:
        """Number of kart suspensions (length of KartPointers->suspensions array)"""
        kart_settings_ref = KartSettings.chain(playerIdx)
        susp_count_ref = kart_settings_ref + 0xC
        return memory.read_u16(susp_count_ref)

    def inst_susp_count(self) -> int:
        """Number of kart suspensions (length of KartPointers->suspensions array)"""
        susp_count_ref = self.addr + 0xC
        return memory.read_u16(susp_count_ref)

    @staticmethod
    def tire_count(playerIdx=0) -> int:
        kart_settings_ref = KartSettings.chain(playerIdx)
        tire_count_ref = kart_settings_ref + 0xE
        return memory.read_u16(tire_count_ref)

    def inst_tire_count(self) -> int:
        tire_count_ref = self.addr + 0xE
        return memory.read_u16(tire_count_ref)

    @staticmethod
    def kart_param(playerIdx=0) -> int:
        kart_settings_ref = KartSettings.chain(playerIdx)
        kart_param_ptr = kart_settings_ref + 0x14
        return memory.read_u32(kart_param_ptr)

    def inst_kart_param(self) -> int:
        kart_param_ptr = self.addr + 0x14
        return memory.read_u32(kart_param_ptr)

    @staticmethod
    def gp_stats(playerIdx=0) -> int:
        kart_settings_ref = KartSettings.chain(playerIdx)
        gp_stats_ptr = kart_settings_ref + 0x34
        return memory.read_u32(gp_stats_ptr)

    def inst_gp_stats(self) -> int:
        gp_stats_ptr = self.addr + 0x34
        return memory.read_u32(gp_stats_ptr)

    @staticmethod
    def race_stats(playerIdx=0) -> int:
        kart_settings_ref = KartSettings.chain(playerIdx)
        race_stats_ptr = kart_settings_ref + 0x38
        return memory.read_u32(race_stats_ptr)

    def inst_race_stats(self) -> int:
        race_stats_ptr = self.addr + 0x38
        return memory.read_u32(race_stats_ptr)