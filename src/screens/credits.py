import pygame
from src.core.constants import *
from src.core.game_scene import GameScene

class CreditsScreen(GameScene):
    def __init__(self, manager, paused_world=None, final_score=None):
        super().__init__(manager)
        self.paused_world = paused_world
        self.final_score = final_score
        self.scroll_y = SCREEN_HEIGHT
        
        self.credits_lines = [
            "Desenvolvimento:", 
            "Eduardo Cruz", "Andrey Jodar", "Arthur Teruel", "Igor Felipe", 
            " ", 
            "Beta Testers:", 
            "Caio Moreira", "Camila Prado", "Geovanny Fernando", "Thales Jodar", "Victor Yamanari", "Eduardo Kaneko", "Amanda Garcia",
            " ",
            " ",
            " ",
            "Obrigado por jogar!"
        ]
        
        pygame.mixer.music.load("assets/sounds/credits.mp3")
        pygame.mixer.music.play(-1)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_SPACE):
                self.finish_credits()

    def update(self, dt):
        self.scroll_y -= 45 * dt
        
        if self.scroll_y < - (len(self.credits_lines) * 40):
            self.finish_credits()

    def finish_credits(self):
        pygame.mixer.music.stop()
        if self.final_score is not None:
            from src.screens.score_input import ScoreInputScreen
            self.manager.change_scene(ScoreInputScreen(self.manager, self.final_score, is_victory=True))
        else:
            from src.screens.main_menu import MainMenuScreen
            self.manager.change_scene(MainMenuScreen(self.manager, self.paused_world))

    def render(self, screen):
        if self.paused_world: 
            self.paused_world.render(screen)
            self.draw_overlay(screen, 180)
        else:
            screen.fill((0, 0, 0))
            
        title = self.font_title.render("UNTIL THE SUN RISES", True, (255, 50, 50))
        screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, self.scroll_y - 80)))
        
        for idx, line in enumerate(self.credits_lines):
            color = (255, 255, 255)
            if line in ("Desenvolvimento:", "Beta Testers:", "Agradecimentos Especiais:", "Músicas e Efeitos:"):
                color = (255, 215, 0)
                
            surf = self.font_medium.render(line, True, color)
            screen.blit(surf, surf.get_rect(center=(SCREEN_WIDTH // 2, self.scroll_y + (idx * 40))))
            
        back_txt = self.font_small.render("Pressione ENTER ou ESC para pular", True, (100, 100, 100))
        screen.blit(back_txt, back_txt.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20)))