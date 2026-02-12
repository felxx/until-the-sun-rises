import pygame
from settings import *
from entities.game_object import GameObject

class Enemy(GameObject):
    def __init__(self, x, y, player_ref):
        super().__init__(x, y, 25, 25, ZOMBIE_COLOR)
        self.player_ref = player_ref
        self.speed = 100

    def update(self, dt):
        direction = self.player_ref.position - self.position
        if direction.length_squared() > 0:
            direction = direction.normalize()
        self.velocity = direction * self.speed
        super().update(dt)