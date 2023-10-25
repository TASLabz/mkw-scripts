from dolphin import memory

from . import KartParam, vec3

class BSP:

    class Hitbox:
        def __init__(self, player_idx=0, hitbox_idx=0, addr=None):
            assert(0 <= hitbox_idx < 16)
            self.addr = addr if addr else BSP.Hitbox.chain(player_idx, hitbox_idx)

            self.enable = self.inst_enable
            self.pos = self.inst_pos
            self.radius = self.inst_radius

        @staticmethod
        def chain(player_idx=0, hitbox_idx=0) -> int:
            return BSP.hitbox(player_idx, hitbox_idx)

        @staticmethod
        def enable(player_idx=0, hitbox_idx=0) -> int:
            hitbox_ref = BSP.Hitbox.chain(player_idx, hitbox_idx)
            enable_ref = hitbox_ref + 0x0
            return memory.read_u8(enable_ref)

        def inst_enable(self) -> int:
            enable_ref = self.addr + 0x0
            return memory.read_u8(enable_ref)

        @staticmethod
        def pos(player_idx=0, hitbox_idx=0) -> vec3:
            hitbox_ref = BSP.Hitbox.chain(player_idx, hitbox_idx)
            pos_ref = hitbox_ref + 0x4
            return vec3.read(pos_ref)

        def inst_pos(self) -> vec3:
            pos_ref = self.addr + 0x4
            return vec3.read(pos_ref)

        @staticmethod
        def radius(player_idx=0, hitbox_idx=0) -> float:
            hitbox_ref = BSP.Hitbox.chain(player_idx, hitbox_idx)
            radius_ref = hitbox_ref + 0x10
            return memory.read_f32(radius_ref)

        def inst_radius(self) -> float:
            radius_ref = self.addr + 0x10
            return memory.read_f32(radius_ref)

        @staticmethod
        def walls_only(player_idx=0, hitbox_idx=0) -> int:
            hitbox_ref = BSP.Hitbox.chain(player_idx, hitbox_idx)
            walls_only_ref = hitbox_ref + 0x14
            return memory.read_u8(walls_only_ref)

        def inst_walls_only(self) -> int:
            walls_only_ref = self.addr + 0x14
            return memory.read_u8(walls_only_ref)

    class Wheel:
        def __init__(self, player_idx=0, wheel_idx=0, addr=None):
            assert(0 <= wheel_idx < 4)
            self.addr = addr if addr else BSP.Wheel.chain(player_idx, wheel_idx)

            self.dist_suspension = self.inst_dist_suspension
            self.speed_suspension = self.inst_speed_suspension
            self.slack_y = self.inst_slack_y
            self.rel_pos = self.inst_rel_pos
            self.x_rot = self.inst_x_rot
            self.wheel_radius = self.inst_wheel_radius
            self.sphere_radius = self.inst_sphere_radius

        @staticmethod
        def chain(player_idx=0, wheel_idx=0) -> int:
            return BSP.wheels(player_idx, wheel_idx)

        @staticmethod
        def dist_suspension(player_idx=0, wheel_idx=0) -> float:
            bsp_ref = BSP.Wheel.chain(player_idx, wheel_idx)
            dist_suspension_ref = bsp_ref + 0x4
            return memory.read_f32(dist_suspension_ref)

        def inst_dist_suspension(self) -> float:
            dist_suspension_ref = self.addr + 0x4
            return memory.read_f32(dist_suspension_ref)

        @staticmethod
        def speed_suspension(player_idx=0, wheel_idx=0) -> float:
            bsp_ref = BSP.Wheel.chain(player_idx, wheel_idx)
            speed_suspension_ref = bsp_ref + 0x8
            return memory.read_f32(speed_suspension_ref)

        def inst_speed_suspension(self) -> float:
            speed_suspension_ref = self.addr + 0x8
            return memory.read_f32(speed_suspension_ref)

        @staticmethod
        def slack_y(player_idx=0, wheel_idx=0) -> float:
            bsp_ref = BSP.Wheel.chain(player_idx, wheel_idx)
            slack_y_ref = bsp_ref + 0xC
            return memory.read_f32(slack_y_ref)

        def inst_slack_y(self) -> float:
            slack_y_ref = self.addr + 0xC
            return memory.read_f32(slack_y_ref)

        @staticmethod
        def rel_pos(player_idx=0, wheel_idx=0) -> vec3:
            bsp_ref = BSP.Wheel.chain(player_idx, wheel_idx)
            rel_pos_ref = bsp_ref + 0x10
            return vec3.read(rel_pos_ref)

        def inst_rel_pos(self) -> vec3:
            rel_pos_ref = self.addr + 0x10
            return vec3.read(rel_pos_ref)

        @staticmethod
        def x_rot(player_idx=0, wheel_idx=0) -> float:
            bsp_ref = BSP.Wheel.chain(player_idx, wheel_idx)
            x_rot_ref = bsp_ref + 0x1C
            return memory.read_f32(x_rot_ref)

        def inst_x_rot(self) -> float:
            x_rot_ref = self.addr + 0x1C
            return memory.read_f32(x_rot_ref)

        @staticmethod
        def wheel_radius(player_idx=0, wheel_idx=0) -> float:
            bsp_ref = BSP.Wheel.chain(player_idx, wheel_idx)
            wheel_radius_ref = bsp_ref + 0x20
            return memory.read_f32(wheel_radius_ref)

        def inst_wheel_radius(self) -> float:
            wheel_radius_ref = self.addr + 0x20
            return memory.read_f32(wheel_radius_ref)

        @staticmethod
        def sphere_radius(player_idx=0, wheel_idx=0) -> float:
            bsp_ref = BSP.Wheel.chain(player_idx, wheel_idx)
            sphere_radius_ref = bsp_ref + 0x24
            return memory.read_f32(sphere_radius_ref)

        def inst_sphere_radius(self) -> float:
            sphere_radius_ref = self.addr + 0x24
            return memory.read_f32(sphere_radius_ref)

    def __init__(self, addr=None):
        self.addr = addr if addr else BSP.chain()

        self.initial_y_pos = self.inst_initial_y_pos
        self.hitbox = self.inst_hitbox
        self.cuboid = self.inst_cuboid
        self.rot_speed = self.inst_rot_speed

    @staticmethod
    def chain(player_idx=0) -> int:
        return KartParam.bsp(player_idx)
    
    @staticmethod
    def initial_y_pos(player_idx=0) -> float:
        bsp_ref = BSP.chain(player_idx)
        initial_y_pos_ref = bsp_ref + 0x0
        return memory.read_f32(initial_y_pos_ref)

    def inst_initial_y_pos(self) -> float:
        initial_y_pos_ref = self.addr + 0x0
        return memory.read_f32(initial_y_pos_ref)

    @staticmethod
    def hitbox(player_idx=0, hitbox_idx=0) -> int:
        assert(0 <= hitbox_idx < 16)
        bsp_ref = BSP.chain(player_idx)
        hitbox_ref = bsp_ref + 0x4 + (hitbox_idx * 0x18)
        return hitbox_ref

    def inst_hitbox(self, hitbox_idx=0) -> "BSP.Hitbox":
        assert(0 <= hitbox_idx < 16)
        hitbox_ref = self.addr + 0x4 + (hitbox_idx * 0x18)
        return hitbox_ref

    @staticmethod
    def cuboid(player_idx=0, cuboid_idx=0) -> vec3:
        assert(0 <= cuboid_idx < 2)
        bsp_ref = BSP.chain(player_idx)
        cuboid_ref = bsp_ref + 0x184 + (cuboid_idx * 0xC)
        return vec3.read(cuboid_ref)

    def inst_cuboid(self, cuboid_idx=0) -> vec3:
        assert(0 <= cuboid_idx < 2)
        cuboid_ref = self.addr + 0x184 + (cuboid_idx * 0xC)
        return vec3.read(cuboid_ref)

    @staticmethod
    def rot_speed(player_idx=0) -> float:
        bsp_ref = BSP.chain(player_idx)
        rot_speed_ref = bsp_ref + 0x19C
        return memory.read_f32(rot_speed_ref)

    def inst_rot_speed(self) -> float:
        rot_speed_ref = self.addr + 0x19C
        return memory.read_f32(rot_speed_ref)

    @staticmethod
    def wheels(player_idx=0, wheel_idx=0) -> int:
        assert(0 <= wheel_idx < 4)
        bsp_ref = BSP.chain(player_idx)
        wheel_ref = bsp_ref + 0x1A4 + (wheel_idx * 0x2C)
        return wheel_ref

    def inst_wheels(self, wheel_idx=0) -> int:
        assert(0 <= wheel_idx < 4)
        wheel_ref = self.addr + 0x1A4 + (wheel_idx * 0x2C)
        return wheel_ref