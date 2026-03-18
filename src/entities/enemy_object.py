import pygame
import math
import os
from src.entities.dynamic_object import DynamicObject

class EnemyObject(DynamicObject):
    def __init__(self, x, y, speed, color, radius, target):
        super().__init__(x, y, speed, color, radius)
        self.target = target
        self.angle = 0
        
        self.frames = []
        base_dir = os.path.dirname(os.path.abspath(__file__))
        assets_dir = os.path.join(base_dir, "..", "..", "assets")

        for i in range(9):
            img_path = os.path.join(assets_dir, f"walk_00{i}.png")
            try:
                img = pygame.image.load(img_path).convert_alpha()
                
                img = pygame.transform.scale(img, (radius * 3, radius * 3))
                self.frames.append(img)
            except:
                surf = pygame.Surface((radius * 2, radius * 2))
                surf.fill(color)
                self.frames.append(surf)

        self.frame_index = 0
        self.animation_speed = 10
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=(x, y))

    def resolve_behavior(self, dt):
        direction = self.target.position - self.position
        
        if direction.length_squared() > 0:
            direction = direction.normalize()
            self.velocity = direction * self.speed

            self.angle = math.degrees(math.atan2(-direction.y, direction.x)) - 250
        else:
            self.velocity = pygame.math.Vector2(0, 0)

    def update(self, dt):
        super().update(dt)
        
        self.frame_index += self.animation_speed * dt
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
            
        current_frame = self.frames[int(self.frame_index)]
        
        self.image = pygame.transform.rotate(current_frame, self.angle)
        
        self.rect = self.image.get_rect(center=self.position)

    def draw(self, screen):
        screen.blit(self.image, self.rect)