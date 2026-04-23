from abc import ABC, abstractmethod
from src.core.game_object import GameObject
import pygame

class DynamicObject(GameObject, ABC):
    def __init__(self, x, y, speed, hitbox_size=(12, 12), combat_radius=15):
        super().__init__(x, y)
        self.velocity = pygame.math.Vector2(0, 0)
        self.speed = speed

        self.hitbox = pygame.Rect(0, 0, hitbox_size[0], hitbox_size[1])
        self.hitbox.center = (x, y)

        self.radius = combat_radius
        self._layer = 2

    def update(self, dt, world_mouse=None):
        self.resolve_behavior(dt)
        if self.velocity.length() > 0:
            self.velocity = self.velocity.normalize() * self.speed

        self.position += self.velocity * dt

        self.hitbox.center = (int(self.position.x), int(self.position.y))

        if hasattr(self, 'rect'):
            self.rect.center = self.hitbox.center

    @abstractmethod
    def resolve_behavior(self, dt):
        pass