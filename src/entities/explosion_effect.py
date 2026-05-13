import pygame
import os

class ExplosionEffect(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.frames = []
        
        for i in range(1, 11):
            path = f"assets/images/explosion/explosion-d{i}.png"
            if os.path.exists(path):
                img = pygame.image.load(path).convert_alpha()
                img = pygame.transform.scale(img, (50, 50)) 
                self.frames.append(img)
        
        if not self.frames:
            self.kill()
            return

        self.frame_index = 0
        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=(x, y))
        self.animation_speed = 25 
        self._layer = 4

    def update(self, dt, world_mouse=None):
        self.frame_index += self.animation_speed * dt
        
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]