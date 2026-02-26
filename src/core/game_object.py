from abc import ABC, abstractmethod
import pygame

class GameObject(ABC):
    def __init__(self, x, y): 
        self.position = pygame.math.Vector2(float(x), float(y))
        self.active = True

    @abstractmethod
    def update(self, dt):
        pass

    @abstractmethod
    def draw(self, dt):
        pass