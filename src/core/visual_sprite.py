import pygame

class VisualSprite(pygame.sprite.Sprite):
    def __init__(self, logical_entity, layer=0):
        super().__init__()
        self.logical_entity = logical_entity
        self._layer = getattr(logical_entity, '_layer', layer)
        self.image = logical_entity.image
        self.rect = logical_entity.rect

    def update(self, *args, **kwargs):
        if not getattr(self.logical_entity, 'active', True):
            self.kill()
            return

        self.image = self.logical_entity.image
        self.rect = self.logical_entity.rect