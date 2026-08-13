import pygame


class GameSprite(pygame.sprite.Sprite):
    def __init__(self, logical_entity, layer=0):
        super().__init__()
        self.logical_entity = logical_entity
        self._layer = getattr(logical_entity, '_layer', layer)

        first_frame = self.logical_entity.render(0)
        self.image = first_frame if first_frame else pygame.Surface((0, 0))

        self.rect = self.image.get_rect(center=logical_entity.position)

    def update(self, dt, *args, **kwargs):
        if not getattr(self.logical_entity, 'active', True):
            self.kill()
            return

        new_image = self.logical_entity.render(dt)
        if new_image:
            self.image = new_image

        self.rect = self.image.get_rect(center=self.logical_entity.position)

        if not getattr(self.logical_entity, 'is_alive', True):
            death_timer = getattr(self.logical_entity, 'death_timer', 0)
            if death_timer > 3.0:
                alpha = max(0, 255 - int((death_timer - 3.0) * 127.5))
                self.image = self.image.copy()
                self.image.set_alpha(alpha)

        if getattr(self.logical_entity, 'damage_flash_timer', 0) > 0:
            self.image = self.image.copy()
            flash_surf = pygame.Surface(self.image.get_size()).convert_alpha()
            flash_surf.fill((255, 0, 0))
            self.image.blit(flash_surf, (0, 0), special_flags=pygame.BLEND_RGB_ADD)