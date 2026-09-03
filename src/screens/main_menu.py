import pygame
from src.core.constants import *
from src.core.game_scene import GameScene

class MainMenuScreen(GameScene):
    def __init__(self, manager, paused_world=None):
        super().__init__(manager)
        self.paused_world = paused_world
        self.selected_index = 0
        if self.paused_world:
            self.options = ["CONTINUAR", "NOVO JOGO", "HISTÓRICO", "CRÉDITOS", "SAIR"]
        else:
            self.options = ["JOGAR", "HISTÓRICO", "CRÉDITOS", "SAIR"]

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_w):
                    self.selected_index = (self.selected_index - 1) % len(self.options)
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    self.selected_index = (self.selected_index + 1) % len(self.options)
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    self.execute_option()
                elif event.key == pygame.K_ESCAPE and self.paused_world:
                    self.manager.change_scene(self.paused_world)
                    
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                mx = mx * (SCREEN_WIDTH / WINDOW_WIDTH)
                my = my * (SCREEN_HEIGHT / WINDOW_HEIGHT)
                start_y = 120 if len(self.options) > 4 else 140
                for idx in range(len(self.options)):
                    rect = pygame.Rect(SCREEN_WIDTH // 2 - 120, start_y + (idx * 40), 240, 35)
                    if rect.collidepoint(mx, my):
                        self.selected_index = idx
                        self.execute_option()

    def execute_option(self):
        from src.core.game_world import GameWorld
        from src.screens.leaderboard import LeaderboardScreen
        from src.screens.credits import CreditsScreen
        
        opt = self.options[self.selected_index]
        if opt == "CONTINUAR":
            self.manager.change_scene(self.paused_world)
        elif opt in ("NOVO JOGO", "JOGAR"):
            self.manager.change_scene(GameWorld(self.manager))
        elif opt == "HISTÓRICO":
            self.manager.change_scene(LeaderboardScreen(self.manager, self.paused_world))
        elif opt == "CRÉDITOS":
            self.manager.change_scene(CreditsScreen(self.manager, self.paused_world))
        elif opt == "SAIR":
            self.manager.quit_game()

    def update(self, dt): 
        pass

    def render(self, screen):
        if self.paused_world: 
            self.paused_world.render(screen)
        self.draw_overlay(screen)
        
        title_txt = "PAUSA" if self.paused_world else "UNTIL THE SUN RISES"
        title_surf = self.font_title.render(title_txt, True, (255, 55, 25))
        screen.blit(title_surf, title_surf.get_rect(center=(SCREEN_WIDTH // 2, 70)))

        start_y = 120 if len(self.options) > 4 else 140
        for idx, option in enumerate(self.options):
            is_selected = (idx == self.selected_index)
            color = (255, 255, 255) if is_selected else (160, 160, 160)
            rect = pygame.Rect(SCREEN_WIDTH // 2 - 120, start_y + (idx * 40), 240, 35)
            if is_selected:
                pygame.draw.rect(screen, (255, 255, 255), rect, 2, border_radius=5)
            text_surf = self.font_medium.render(option, True, color)
            screen.blit(text_surf, text_surf.get_rect(center=rect.center))