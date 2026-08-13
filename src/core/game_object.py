from abc import ABC, abstractmethod
import pygame


class GameObject(ABC):
    def __init__(self, position):
        self.active = True
        self.position = pygame.math.Vector2(position)
        self.angle = 0

    def kill(self):
        self.active = False

    @abstractmethod
    def update(self, dt, *args, **kwargs):
        pass

    @abstractmethod
    def render(self, dt) -> pygame.Surface:
        pass