from src.entities.dynamic_object import DynamicObject
import pygame 

class PlayerObject(DynamicObject):
    def __init__(self, x, y, speed, color, radius=15):
        super().__init__(x, y, speed, color, radius)

    def resolve_behavior(self, dt):
        keys = pygame.key.get_pressed()
        self.velocity.x = keys[pygame.K_d] - keys[pygame.K_a]
        self.velocity.y = keys[pygame.K_s] - keys[pygame.K_w]