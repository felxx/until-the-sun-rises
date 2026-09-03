import pygame
from src.core.constants import *
from src.core.game_scene import GameScene

class LeaderboardScreen(GameScene):
    def __init__(self, manager, paused_world=None):
        super().__init__(manager)
        self.paused_world = paused_world

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_SPACE):
                from src.screens.main_menu import MainMenuScreen
                self.manager.change_scene(MainMenuScreen(self.manager, self.paused_world))

    def update(self, dt): 
        pass

    def render(self, screen):
        if self.paused_world: self.paused_world.render(screen)
        self.draw_overlay(screen, 180)
        
        title = self.font_title.render("HISTÓRICO", True, (255, 55, 25))
        screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 50)))

        scores = self.manager.score_manager.load_scores()
        if not scores:
            empty_txt = self.font_medium.render("Nenhuma pontuação registrada.", True, (255, 55, 25))
            screen.blit(empty_txt, empty_txt.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
        else:
            for idx, item in enumerate(scores):
                txt = f"{idx + 1}. {item['name']} - {item['score']} pts"
                surf = self.font_medium.render(txt, True, (255, 255, 255))
                screen.blit(surf, (SCREEN_WIDTH // 2 - 100, 90 + (idx * 22)))

        back_txt = self.font_small.render("Pressione ENTER ou ESC para voltar", True, (255, 255, 255))
        screen.blit(back_txt, back_txt.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20)))