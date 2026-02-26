from src.core.game_object import GameObject
import pygame

class StaticObject(GameObject): 
    def __init__(self, x, y):
        super().__init__(x, y)

    def update(self, dt):
        pass

    def draw(self, screen):
        pass