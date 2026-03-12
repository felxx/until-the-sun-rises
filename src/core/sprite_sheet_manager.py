import pygame

class SpriteSheetManager:
    _cache = {}

    @classmethod
    def get_frames(cls, path, scale_factor=3, frame_count=4):
        key = (path, scale_factor)
        if key not in cls._cache:
            sheet = pygame.image.load(path).convert_alpha()
            w, h = sheet.get_size()
            sheet = pygame.transform.scale(sheet, (w * scale_factor, h * scale_factor))

            f_w = sheet.get_width() // frame_count
            f_h = sheet.get_height()

            cls._cache[key] = [
                sheet.subsurface(pygame.Rect(i * f_w, 0, f_w, f_h))
                for i in range(frame_count)
            ]
        return cls._cache[key]