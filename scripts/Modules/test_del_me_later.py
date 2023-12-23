import math
import struct

class vec3:
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

    def __add__(self, other):
        return vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        """ vec3 * vec3 -> float (dot product)
            vec3 * float -> vec3 (scalar multiplication)"""
        if type(other) == vec3:
            return self.x * other.x + self.y * other.y + self.z * other.z
        else:
            return vec3(self.x * other, self.y * other, self.z * other)

    def __matmul__(self, other):
        """ vec3 @ vec3 -> vec3 (cross product)
            vec3 @ float -> vec3 (scalar multiplication)"""        
        if type(other) == vec3:
            x = self.y*other.z - self.z*other.y
            y = self.z*other.x - self.x*other.z
            z = self.x*other.y - self.y*other.x
            return vec3(x,y,z)
        else:
            return vec3(self.x * other, self.y * other, self.z * other)
        
    def length(self) -> float:
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def length_xz(self) -> float:
        return math.sqrt(self.x**2 + self.z**2)

    def forward(self, facing_yaw) -> float:
        speed_yaw = -180/math.pi * math.atan2(self.x, self.z)
        diff_angle_rad = (facing_yaw - speed_yaw)*math.pi/180
        return math.sqrt(self.x**2 + self.z**2)*math.cos(diff_angle_rad)

    def sideway(self, facing_yaw) -> float:
        speed_yaw = -180/math.pi * math.atan2(self.x, self.z)
        diff_angle_rad = (facing_yaw - speed_yaw)*math.pi/180
        return math.sqrt(self.x**2 + self.z**2)*math.sin(diff_angle_rad)

    @staticmethod
    def read(ptr) -> "vec3":
        bytes = memory.read_bytes(ptr, 0xC)
        return vec3(*struct.unpack('>' + 'f'*3, bytes))

    @staticmethod
    def from_bytes(bts) -> "vec3":
        return vec3(*struct.unpack('>' + 'f'*3, bts))

    def to_bytes(self) -> bytearray:
        return bytearray(struct.pack('>fff', self.x, self.y, self.z))
