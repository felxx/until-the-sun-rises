import pygame
import math
import os
from src.entities.dynamic_object import DynamicObject

class PlayerObject(DynamicObject):
    def __init__(self, x, y, speed, color, radius=15):
        super().__init__(x, y, speed, color, radius)

        self.frames = []
        for i in range(1, 10):
            path = f"assets/rifle{i}.png"
            try:
                img = pygame.image.load(path).convert_alpha()
                img = pygame.transform.scale(img, (64, 64))
                self.frames.append(img)
            except pygame.error:
                surf = pygame.Surface((64, 64))
                surf.fill((255, 0, 255))
                self.frames.append(surf)

        self.frame_index = 0
        self.angle = 0
        self.original_image = self.frames[self.frame_index]
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))

    def resolve_behavior(self, dt):
        keys = pygame.key.get_pressed()
        self.velocity.x = keys[pygame.K_d] - keys[pygame.K_a]
        self.velocity.y = keys[pygame.K_s] - keys[pygame.K_w]
        
        if self.velocity.length() > 0:
            self.velocity = self.velocity.normalize()

    def update(self, dt):
        super().update(dt)
        
        if self.velocity.length() > 0:
            self.frame_index += 12 * dt
            if self.frame_index >= len(self.frames):
                self.frame_index = 0
        else:
            self.frame_index = 0

        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.position.x, mouse_y - self.position.y
        self.angle = math.degrees(math.atan2(-rel_y, rel_x)) - 90

        self.original_image = self.frames[int(self.frame_index)]
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.position)

    def draw(self, screen):
        screen.blit(self.image, self.rect)