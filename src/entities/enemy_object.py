from src.entities.dynamic_object import DynamicObject
import pygame

class EnemyObject(DynamicObject):
    def __init__(self, x, y, speed, color, radius, target):
        super().__init__(x, y, speed, color, radius)
        self.target = target 

    def resolve_behavior(self, dt):
        direction = self.target.position - self.position
        
        if direction.length() > 0:
            self.velocity = direction 
        else:
            self.velocity = pygame.math.Vector2(0, 0)