from abc import ABC, abstractmethod
import pygame

class GameObject(ABC):
    def __init__(self, position):
        self.active = True
        self.position = pygame.math.Vector2(position)
        
        self.image = pygame.Surface((32, 32), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=self.position)

    @abstractmethod
    def update(self, dt):
        pass