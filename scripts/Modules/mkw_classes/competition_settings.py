from dolphin import memory
from typing import List
import struct

class CompetitionSettings:
    def __init__(self, addr):
        """This class has multiple instances.
           Require that the caller specifies the address."""
        self.addr = addr

    def resource_id(self) -> int:
        resource_id_ref = self.addr + 0x0
        return memory.read_u16(resource_id_ref)
    
    def objective(self) -> int:
        """Something depending on competition type"""
        objective_ref = self.addr + 0x2
        return memory.read_u16(objective_ref)
    
    def course_id(self) -> int:
        course_id_ref = self.addr + 0x4
        return memory.read_u8(course_id_ref)
    
    def character_id(self) -> int:
        character_id_ref = self.addr + 0x5
        return memory.read_u8(character_id_ref)
    
    def vehicle_id(self) -> int:
        vehicle_id_ref = self.addr + 0x6
        return memory.read_u8(vehicle_id_ref)
    
    def engine_class(self) -> int:
        engine_class_ref = self.addr + 0x7
        return memory.read_u8(engine_class_ref)
    
    def time_limit(self) -> int:
        time_limit_ref = self.addr + 0x2C
        return memory.read_u16(time_limit_ref)
    
    def controller_restriction(self) -> int:
        controller_restriction_ref = self.addr + 0x2F
        return memory.read_u8(controller_restriction_ref)
    
    def rank_scores(self) -> List[int]:
        """Scores required to achieve rank.
           It's an array of uints of length 6"""
        rank_scores_ref = self.addr + 0x30
        bytes = memory.read_bytes(rank_scores_ref, 4 * 6)
        return struct.unpack('>' + 'I'*6, bytes)
    
    def camera_angle(self) -> int:
        camera_angle_ref = self.addr + 0x48
        return memory.read_u16(camera_angle_ref)
    
    def minimap_object(self) -> int:
        minimap_object_ref = self.addr + 0x4A
        return memory.read_u16(minimap_object_ref)
    
    def cannon(self) -> int:
        cannon_ref = self.addr + 0x50
        return memory.read_u16(cannon_ref)
    
    def cpu_count(self) -> int:
        cpu_count_ref = self.addr + 0x58
        return memory.read_u16(cpu_count_ref)
    
    def cpu_combo(self, cpu_idx=0) -> int:
        assert(0 <= cpu_idx < 11)
        cpu_combo_ref = self.addr + 0x5A + (cpu_idx * 0x2)
        return cpu_combo_ref
    
    def cpu_combo_character_id(self, cpu_idx=0) -> int:
        assert(0 <= cpu_idx < 11)
        cpu_combo_ref = self.addr + 0x5A + (cpu_idx * 0x2)
        character_id_ref = cpu_combo_ref + 0x0
        return memory.read_u8(character_id_ref)
    
    def cpu_combo_vehicle_id(self, cpu_idx=0) -> int:
        assert(0 <= cpu_idx < 11)
        cpu_combo_ref = self.addr + 0x5A + (cpu_idx * 0x2)
        vehicle_id_ref = cpu_combo_ref + 0x1
        return memory.read_u8(vehicle_id_ref)