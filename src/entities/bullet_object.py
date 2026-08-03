import os
import math
import pygame

from src.core.sprite_sheet import SpriteSheet
from src.entities.dynamic_object import DynamicObject
from src.core.constants import SCREEN_WIDTH, SCREEN_HEIGHT

class BulletObject(DynamicObject):
    _sprite_sheet = None

    def __init__(self, position, target_pos):
        super().__init__(position, speed=800, hitbox_size=(4, 4), combat_radius=5)
        self.start_pos = position
        self.max_range = 1000

        if BulletObject._sprite_sheet is None:
            bullet_paths = [f"assets/images/bullet/shot{i}.png" for i in range(1, 5)]
            BulletObject._sprite_sheet = SpriteSheet(bullet_paths, 32)

        direction = pygame.math.Vector2(target_pos) - self.position
        
        if direction.length() > 0:
            self.velocity = direction.normalize() * self.speed
            self.angle = math.degrees(math.atan2(-self.velocity.y, self.velocity.x)) - 90
        else:
            self.velocity = pygame.math.Vector2(0, 0)
            self.angle = 0
            
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
        
        distance = self.position.distance_to(self.start_pos)
        if distance > self.max_range:
            self.active = False