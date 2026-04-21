from abc import ABC, abstractmethod
from src.core.game_object import GameObject
import pygame

class DynamicObject(GameObject, ABC):
    def __init__(self, x, y, speed, radius=15):
        super().__init__(x, y)
        self.velocity = pygame.math.Vector2(0, 0)
        self.speed = speed
        self.radius = radius
        self._layer = 2

    def update(self, dt, world_mouse=None):
        self.resolve_behavior(dt)
        if self.velocity.length() > 0:
            self.velocity = self.velocity.normalize() * self.speed

        self.position += self.velocity * dt
        self.rect.center = (int(self.position.x), int(self.position.y))

    @abstractmethod
    def resolve_behavior(self, dt):
        pass