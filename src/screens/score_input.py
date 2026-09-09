import pygame
from src.core.constants import *
from src.core.game_scene import GameScene

class ScoreInputScreen(GameScene):
    def __init__(self, manager, final_score, is_victory=False):
        super().__init__(manager)
        self.final_score = final_score
        self.is_victory = is_victory
        self.player_name_input = ""
        self.score_saved = False

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if not self.score_saved:
                        self.manager.score_manager.save_score(self.player_name_input, self.final_score)
                        self.score_saved = True
                    from src.screens.main_menu import MainMenuScreen
                    self.manager.change_scene(MainMenuScreen(self.manager))
                elif event.key == pygame.K_BACKSPACE:
                    self.player_name_input = self.player_name_input[:-1]
                else:
                    if len(self.player_name_input) < 12 and event.unicode.isprintable():
                        self.player_name_input += event.unicode

    def update(self, dt): 
        pass

    def render(self, screen):
        if self.is_victory:
            screen.fill((255, 255, 200))
            title_text, title_color = "VOCÊ SOBREVIVEU!", (50, 200, 50)
            text_color, box_color = (0, 0, 0), (0, 0, 0)
        else:
            self.draw_overlay(screen, 190)
            title_text, title_color = "FIM DE JOGO", (255, 50, 50)
            text_color, box_color = (255, 255, 255), (255, 255, 255)

        title = self.font_title.render(title_text, True, title_color)
        screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 70)))

        score_txt = self.font_medium.render(f"Pontuação Final: {self.final_score}", True, text_color)
        screen.blit(score_txt, score_txt.get_rect(center=(SCREEN_WIDTH // 2, 130)))

        prompt_txt = self.font_small.render("Digite seu nome e pressione ENTER para salvar:", True, text_color)
        screen.blit(prompt_txt, prompt_txt.get_rect(center=(SCREEN_WIDTH // 2, 180)))

        input_rect = pygame.Rect(SCREEN_WIDTH // 2 - 120, 210, 240, 40)
        pygame.draw.rect(screen, box_color, input_rect, 2, border_radius=5)
        
        display_name = self.player_name_input if self.player_name_input else "_"
        name_surf = self.font_medium.render(display_name, True, (135, 206, 250) if not self.is_victory else (50, 50, 200))
        screen.blit(name_surf, name_surf.get_rect(center=input_rect.center))