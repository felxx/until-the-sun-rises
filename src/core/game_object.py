from abc import ABC, abstractmethod
import pygame

class GameObject(pygame.sprite.Sprite, ABC):
    def __init__(self, x, y):
        super().__init__()

        self.active = True
        self.position = pygame.math.Vector2(float(x), float(y))
        self.image = pygame.Surface((32, 32), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))

    @abstractmethod
    def update(self, dt):
        pass