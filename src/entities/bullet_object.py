import pygame
import math
import os
from src.entities.dynamic_object import DynamicObject
from src.core.constants import SCREEN_WIDTH, SCREEN_HEIGHT

class BulletObject(DynamicObject):
    def __init__(self, x, y, target_pos):
        super().__init__(x, y, 800, (255, 255, 0), radius=5)
        
        direction = target_pos - self.position
        if direction.length_squared() > 0:
            direction = direction.normalize()
        
        self.velocity = direction * self.speed
        self.angle = math.degrees(math.atan2(-direction.y, direction.x)) - 90
        
        self.frames = []
        base_dir = os.path.dirname(os.path.abspath(__file__))
        assets_dir = os.path.join(base_dir, "..", "..", "assets")

        for i in range(1, 5):
            img_path = os.path.join(assets_dir, f"Shot{i}.png")
            try:
                img = pygame.image.load(img_path).convert_alpha()
                img = pygame.transform.scale(img, (32, 32))
                img = pygame.transform.rotate(img, self.angle)
                self.frames.append(img)
            except:
                surf = pygame.Surface((10, 10))
                surf.fill((255, 255, 0))
                self.frames.append(surf)

        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=(x, y))

    def resolve_behavior(self, dt):
        pass

    def update(self, dt):
        super().update(dt)
        self.rect.center = self.position
        
        self.frame_index += 15 * dt
        if self.frame_index < len(self.frames):
            self.image = self.frames[int(self.frame_index)]

    def is_off_screen(self):
        margin = 100
        return (self.position.x < -margin or self.position.x > SCREEN_WIDTH + margin or
                self.position.y < -margin or self.position.y > SCREEN_HEIGHT + margin)

    def draw(self, screen):
        screen.blit(self.image, self.rect)