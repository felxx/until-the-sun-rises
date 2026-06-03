import pygame

class LandmineObject(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.position = position
        self.timer = 5.0
        self.blast_radius = 60
        self.damage = 3
        
        self.image = pygame.Surface((14, 14), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=self.position)
        self._layer = 1
        self._draw_mine(False)

    def _draw_mine(self, is_lit):
        self.image.fill((0, 0, 0, 0))
        
        center = (7, 7)
        pygame.draw.circle(self.image, (50, 50, 50), center, 6)
        pygame.draw.circle(self.image, (30, 30, 30), center, 3)
        
        led_color = (255, 0, 0) if is_lit else (60, 0, 0)
        pygame.draw.circle(self.image, led_color, center, 1)

    def update(self, dt, world_mouse=None):
        self.timer -= dt
        
        flash_speed = 12 if self.timer < 2 else 5
        lit = int(self.timer * flash_speed) % 2 == 0
        
        self._draw_mine(lit)
        return self.timer <= 0