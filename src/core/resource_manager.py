import pygame
import os

class ResourceManager:
    _images = {}
    _sounds = {}
    _fonts = {}
    _current_music = None

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

    @classmethod
    def get_font(cls, path, size):
        key = (path, size)
        if key not in cls._fonts:
            try:
                cls._fonts[key] = pygame.font.Font(path, size)
            except (pygame.error, FileNotFoundError):
                cls._fonts[key] = pygame.font.Font(None, size)
        return cls._fonts[key]

    @classmethod
    def play_music(cls, path, loops=-1, volume=None):
        if cls._current_music == path:
            return
        if not os.path.exists(path):
            return
        try:
            pygame.mixer.music.load(path)
            if volume is not None:
                pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(loops)
            cls._current_music = path
        except pygame.error:
            pass