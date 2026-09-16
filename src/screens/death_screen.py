import pygame
from src.core.constants import *
from src.core.game_scene import GameScene

class DeathScreen(GameScene):
    def __init__(self, manager, dead_world):
        super().__init__(manager)
        self.dead_world = dead_world
        self.death_timer = 0.0
        self.death_duration = 3.5

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_ESCAPE, pygame.K_SPACE):
                from src.screens.score_input import ScoreInputScreen
                score = getattr(self.dead_world.player, 'score', 0)
                self.manager.change_scene(ScoreInputScreen(self.manager, score, is_victory=False))

    def update(self, dt):
        self.death_timer += dt
        if self.death_timer >= self.death_duration:
            from src.screens.score_input import ScoreInputScreen
            score = getattr(self.dead_world.player, 'score', 0)
            self.manager.change_scene(ScoreInputScreen(self.manager, score, is_victory=False))

    def render(self, screen):
        self.dead_world.render(screen)
        progress = min(1.0, self.death_timer / (self.death_duration * 0.7))
        alpha = int(progress * 220)
        self.draw_overlay(screen, alpha)
        
        banner_height = 130
        banner = pygame.Surface((SCREEN_WIDTH, banner_height), pygame.SRCALPHA)
        banner.fill((10, 0, 0, min(230, alpha)))
        screen.blit(banner, (0, (SCREEN_HEIGHT // 2) - (banner_height // 2)))

        text_alpha = int(min(255, (self.death_timer / 1.0) * 255))
        scale = 1.0 + (self.death_timer / self.death_duration) * 0.15
        
        base_surf = self.font_death.render("VOCÊ MORREU", True, (180, 20, 20))
        scaled_w = int(base_surf.get_width() * scale)
        scaled_h = int(base_surf.get_height() * scale)
        text_surf = pygame.transform.smoothscale(base_surf, (scaled_w, scaled_h))
        text_surf.set_alpha(text_alpha)

        screen.blit(text_surf, text_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 10)))