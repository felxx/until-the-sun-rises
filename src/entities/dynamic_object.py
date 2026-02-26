from abc import ABC, abstractmethod
from src.core.game_object import GameObject
import pygame

class DynamicObject(GameObject, ABC):
    def __init__(self, x, y, speed):
        super().__init__(x, y)
        self.velocity = pygame.math.Vector2(0, 0)
        self.speed = speed

    def update(self, dt):
        self.resolve_behavior(dt)
        
        if self.velocity.length() > 0:
            self.velocity = self.velocity.normalize() * self.speed
            
        self.position += self.velocity * dt

    def draw(self, screen):
        pass

    @abstractmethod
    def resolve_behavior(self, dt):
        pass