from abc import abstractmethod
from src.entities.static_object import StaticObject
import pygame

class ConsumableObject(StaticObject):
    def __init__(self, position, hitbox_size=(16, 16)):
        super().__init__(position)
        self.hitbox = pygame.Rect(0, 0, hitbox_size[0], hitbox_size[1])
        self.hitbox.center = self.position
        self._layer = 1

    def update(self, dt, player):
        if self.active and self.hitbox.colliderect(player.hitbox):
            self.apply_effect(player)
            self.kill()

    @abstractmethod
    def apply_effect(self, player):
        pass

    @abstractmethod
    def render(self, dt):
        pass