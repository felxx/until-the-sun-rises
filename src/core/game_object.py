from abc import ABC, abstractmethod
import pygame

class GameObject(ABC):
    def __init__(self, x, y, color=(255, 255, 255)): 
        self.position = pygame.math.Vector2(float(x), float(y))
        self.color = color
        self.active = True

    @abstractmethod
    def update(self, dt):
        pass

    @abstractmethod
    def draw(self, screen):
        pass