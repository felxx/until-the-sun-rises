import pygame
import math
import os
from src.entities.dynamic_object import DynamicObject
from src.core.constants import SCREEN_WIDTH, SCREEN_HEIGHT


class BulletObject(DynamicObject):
    def __init__(self, x, y, target_pos):
        super().__init__(x, y, speed=800, radius=5)

        direction = target_pos - self.position
        if direction.length_squared() > 0:
            direction = direction.normalize()

        self.velocity = direction * self.speed
        self.angle = math.degrees(math.atan2(-direction.y, direction.x)) - 90

        self.frames = self._load_frames()
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=self.position)

    def _load_frames(self):
        frames = []

        for i in range(1, 5):
            path = f"assets/images/bullet/shot{i}.png"
            try:
                img = pygame.image.load(path).convert_alpha()
                img = pygame.transform.scale(img, (32, 32))
                img = pygame.transform.rotate(img, self.angle)
                frames.append(img)
            except:
                surf = pygame.Surface((10, 10), pygame.SRCALPHA)
                pygame.draw.circle(surf, (255, 255, 0), (5, 5), 5)
                frames.append(surf)
        return frames

    def resolve_behavior(self, dt):
        pass

    def update(self, dt):
        super().update(dt)

        self.frame_index = (self.frame_index + 15 * dt) % len(self.frames)
        self.image = self.frames[int(self.frame_index)]

        if self.is_off_screen():
            self.kill()

    def is_off_screen(self):
        margin = 50
        return (self.position.x < -margin or self.position.x > SCREEN_WIDTH + margin or
                self.position.y < -margin or self.position.y > SCREEN_HEIGHT + margin)