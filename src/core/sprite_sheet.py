import pygame
from src.core.resource_manager import ResourceManager

class SpriteSheet:

    def __init__(self, paths, scale):
        self.original_frames = [ResourceManager.get_image(p, scale) for p in paths]
        self.rotation_cache = {i: {} for i in range(len(self.original_frames))}

    def get_frame(self, index, angle):
        index = int(index) % len(self.original_frames)
        approx_angle = int(angle // 5) * 5

        if approx_angle not in self.rotation_cache[index]:
            rotated = pygame.transform.rotate(self.original_frames[index], approx_angle)
            self.rotation_cache[index][approx_angle] = rotated

        return self.rotation_cache[index][approx_angle]