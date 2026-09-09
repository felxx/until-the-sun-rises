import pygame
from src.core.constants import *
from src.core.game_scene import GameScene

class CreditsScreen(GameScene):
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
        
        title = self.font_title.render("CRÉDITOS", True, (255, 0, 0))
        screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 50)))

        credits_lines = ["Desenvolvimento:", "Eduardo Cruz", "Andrey Jodar", "Arthur Teruel", "Igor Felipe", " ", "Beta Testers:", "Caio Moreira", "Camila Prado", "Geovanny Fernando"]
        for idx, line in enumerate(credits_lines):
            color = 255, 255, 255
            surf = self.font_medium.render(line, True, color)
            screen.blit(surf, surf.get_rect(center=(SCREEN_WIDTH // 2, 110 + (idx * 20))))

        back_txt = self.font_small.render("Pressione ENTER ou ESC para voltar", True, (200, 200, 200))
        screen.blit(back_txt, back_txt.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20)))