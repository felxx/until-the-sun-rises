import pygame
from settings import *
from entities.game_object import GameObject

class Player(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 30, 30, PLAYER_COLOR)
        self.speed = 250
        self.flashlight_radius = 150

    def handle_input(self):
        self.velocity = pygame.math.Vector2(0, 0)
        keys = pygame.key.get_pressed()
        
        input_vector = pygame.math.Vector2(0, 0)
        if keys[pygame.K_w]: input_vector.y -= 1
        if keys[pygame.K_s]: input_vector.y += 1
        if keys[pygame.K_a]: input_vector.x -= 1
        if keys[pygame.K_d]: input_vector.x += 1

        if input_vector.length_squared() > 0:
            input_vector = input_vector.normalize()
        
        self.velocity = input_vector * self.speed
