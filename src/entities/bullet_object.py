import os
import math
import pygame

from core.sprite_sheet import SpriteSheet
from src.entities.dynamic_object import DynamicObject
from src.core.constants import SCREEN_WIDTH, SCREEN_HEIGHT

class BulletObject(DynamicObject):
    _sprite_sheet = None

    def __init__(self, x, y, target_pos):
        super().__init__(x, y, speed=800, radius=5)

        if BulletObject._sprite_sheet is None:
            bullet_paths = [f"assets/images/bullet/shot{i}.png" for i in range(1, 5)]
            BulletObject._sprite_sheet = SpriteSheet(bullet_paths, 32)

        direction = target_pos - self.position
        if direction.length_squared() > 0:
            direction = direction.normalize()

        self.angle = math.degrees(math.atan2(-direction.y, direction.x)) - 90

        self.frame_index = 0
        self.image = BulletObject._sprite_sheet.get_frame(self.frame_index, self.angle)
        self.rect = self.image.get_rect(center=self.position)
        self._layer = 3

    def resolve_behavior(self, dt):
        pass

    def update(self, dt, world_mouse=None):
        super().update(dt)

        self.frame_index = (self.frame_index + 15 * dt) % 4
        self.image = BulletObject._sprite_sheet.get_frame(self.frame_index, self.angle)

        if self.is_off_screen():
            self.kill()

    def is_off_screen(self):
        margin = 50
        return (self.position.x < -margin or self.position.x > SCREEN_WIDTH + margin or
                self.position.y < -margin or self.position.y > SCREEN_HEIGHT + margin)