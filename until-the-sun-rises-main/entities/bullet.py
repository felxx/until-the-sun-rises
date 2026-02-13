import pygame
from settings import *
from entities.game_object import GameObject

class Bullet(GameObject):
    def __init__(self, x, y, target_pos):
        
        super().__init__(x, y, 5, 5, (255, 255, 0))
        self.speed = 500
        
        direction = target_pos - self.position
        if direction.length_squared() > 0:
            direction = direction.normalize()
        
        self.velocity = direction * self.speed

    def is_off_screen(self):
        return (self.position.x < 0 or self.position.x > SCREEN_WIDTH or
                self.position.y < 0 or self.position.y > SCREEN_HEIGHT)