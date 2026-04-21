import pygame
import os

class ResourceManager:
    _images = {}
    _sounds = {}

    @classmethod
    def get_image(cls, path, scale=None):
        key = (path, scale)
        if key not in cls._images:
            try:
                img = pygame.image.load(path).convert_alpha()
                if scale:
                    img = pygame.transform.scale(img, (int(scale), int(scale)))
                cls._images[key] = img
            except pygame.error:
                surf = pygame.Surface((32, 32))
                surf.fill((255, 0, 255))
                cls._images[key] = surf
        return cls._images[key]

    @classmethod
    def get_sound(cls, path):
        if path not in cls._sounds:
            cls._sounds[path] = pygame.mixer.Sound(path)
        return cls._sounds[path]