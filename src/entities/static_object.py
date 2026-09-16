from src.entities.game_object import GameObject
import pygame

class StaticObject(GameObject): 
    def __init__(self, position):
        super().__init__(position)

    def update(self, dt):
        pass

    def draw(self, screen):
        pass