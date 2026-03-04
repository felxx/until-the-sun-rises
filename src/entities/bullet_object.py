import pygame
from src.entities.dynamic_object import DynamicObject
from src.core.constants import SCREEN_WIDTH, SCREEN_HEIGHT

class BulletObject(DynamicObject):
    def __init__(self, x, y, target_pos):
        super().__init__(x, y, 500, (255, 255, 0), radius=5)
        
        direction = target_pos - self.position
        if direction.length_squared() > 0:
            direction = direction.normalize()
        
        self.velocity = direction * self.speed

    def resolve_behavior(self, dt):
        pass

    def is_off_screen(self):
        return (self.position.x < 0 or self.position.x > SCREEN_WIDTH or
                self.position.y < 0 or self.position.y > SCREEN_HEIGHT)