from abc import ABC, abstractmethod
from src.core.game_object import GameObject
import pygame

class DynamicObject(GameObject, ABC):
    def __init__(self, position, speed, hitbox_size=(12, 12), combat_radius=15):
        super().__init__(position)
        self.velocity = pygame.math.Vector2(0, 0)
        self.speed = speed

        self.hitbox = pygame.Rect(0, 0, hitbox_size[0], hitbox_size[1])
        self.hitbox.center = self.position

        self.radius = combat_radius
        self._layer = 2

    def update(self, dt, world_mouse=None):
        self.resolve_behavior(dt)
        if self.velocity.length() > 0:
            self.velocity = self.velocity.normalize() * self.speed

        self.position += self.velocity * dt
        self.hitbox.center = self.position

    @abstractmethod
    def resolve_behavior(self, dt):
        pass