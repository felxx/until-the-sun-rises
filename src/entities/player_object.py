from src.entities.dynamic_object import DynamicObject
import pygame 

class PlayerObject(DynamicObject):
    def resolve_behavior(self, dt):
        keys = pygame.key.get_pressed()
        self.velocity.x = keys[pygame.K_d] - keys[pygame.K_a]
        self.velocity.y = keys[pygame.K_w] - keys[pygame.K_s]