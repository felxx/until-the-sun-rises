import pygame
from settings import * 

class GameObject:
    def __init__(self, x, y, width, height, color):
        self.position = pygame.math.Vector2(x, y)
        self.velocity = pygame.math.Vector2(0, 0)
        self.width = width
        self.height = height
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)

    def update(self, dt):
        self.position += self.velocity * dt
        self.rect.center = (round(self.position.x), round(self.position.y))

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)