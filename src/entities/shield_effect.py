import math
import pygame


class ShieldEffect:
    def __init__(self, target_player):
        self.player = target_player
        self.duration = 3.0  
        self.timer = 0.0
        self.is_active = False

        self.base_radius = 15
        
        self.pulse_time = 0.0
        self.hit_flash_timer = 0.0 

    def activate(self):
        """Ativa a invulnerabilidade e reseta o temporizador."""
        self.timer = self.duration
        self.is_active = True
        self.pulse_time = 0.0
        self.hit_flash_timer = 0.0

    def trigger_hit(self, attacker_position=None):
        """Dispara um flash visual quando um zumbi tenta atacar."""
        if self.is_active:
            self.hit_flash_timer = 0.15  # Brilho

    def update(self, dt):
        if not self.is_active:
            return

        self.timer -= dt
        self.pulse_time += dt * 3.0 

        if self.hit_flash_timer > 0:
            self.hit_flash_timer -= dt

        if self.timer <= 0:
            self.is_active = False

    def draw(self, screen, camera_zoom=1.0, camera_offset=(0, 0)):
        if not self.is_active:
            return

        screen_x = int((self.player.position.x - camera_offset[0]) * camera_zoom)
        screen_y = int((self.player.position.y - camera_offset[1]) * camera_zoom)

        pulse_offset = math.sin(self.pulse_time) * 2.5
        current_radius = int((self.base_radius + pulse_offset) * camera_zoom)

        surf_size = current_radius * 2 + 20
        shield_surf = pygame.Surface((surf_size, surf_size), pygame.SRCALPHA)
        center = (surf_size // 2, surf_size // 2)

        if self.hit_flash_timer > 0:
            fill_color = (150, 255, 220, 110)  
            border_color = (220, 255, 255, 240) 
            glow_color = (0, 255, 200, 70)
        else:
            fill_color = (0, 220, 140, 50)     
            border_color = (100, 255, 180, 200) 
            glow_color = (0, 200, 100, 30)

        pygame.draw.circle(shield_surf, glow_color, center, current_radius + 4)
        
        pygame.draw.circle(shield_surf, fill_color, center, current_radius)
        
        pygame.draw.circle(shield_surf, border_color, center, current_radius, width=3)
        
        pygame.draw.circle(shield_surf, (255, 255, 255, 180), center, max(1, current_radius - 3), width=1)

        rect = shield_surf.get_rect(center=(screen_x, screen_y))
        screen.blit(shield_surf, rect)