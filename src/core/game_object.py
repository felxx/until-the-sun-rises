from abc import ABC, abstractmethod
import pygame


class GameObject(ABC):
    def __init__(self, position):
        self.active = True
        self.position = pygame.math.Vector2(position)
        self.angle = 0

        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = pygame.Surface((0, 0))
        self.sprite.rect = self.sprite.image.get_rect(center=self.position)
        self.sprite._layer = 1

    def kill(self):
        self.active = False
        self.sprite.kill()

    @property
    def _layer(self):
        return self.sprite._layer

    @_layer.setter
    def _layer(self, value):
        self.sprite._layer = value

    @abstractmethod
    def update(self, dt, *args, **kwargs):
        pass

    @abstractmethod
    def render(self, dt):
        pass