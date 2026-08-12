from abc import ABC, abstractmethod
import pygame


class GameObject(ABC):
    def __init__(self, position):
        self.active = True
        self.position = pygame.math.Vector2(position)
        self.angle = 0

        self.image = pygame.Surface((32, 32), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=self.position)

    def kill(self):
        self.active = False

    @abstractmethod
    def update(self, dt, *args, **kwargs):
        pass

    def render(self, dt):
        self.rect = self.image.get_rect(center=(int(self.position.x), int(self.position.y)))