import json
import os
import random
import pygame

from src.core.constants import *
from src.core.game_world import GameWorld

SCORES_FILE = "scores.json"

def load_scores():
    if os.path.exists(SCORES_FILE):
        try:
            with open(SCORES_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Erro ao carregar pontuações: {e}")
            return []
    return []

def save_score(player_name, score):
    scores = load_scores()
    name = player_name.strip() if player_name.strip() else "Jogador"
    scores.append({"name": name, "score": score})
    scores.sort(key=lambda x: x["score"], reverse=True)
    scores = scores[:10]
    try:
        with open(SCORES_FILE, "w", encoding="utf-8") as f:
            json.dump(scores, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Erro ao salvar pontuação: {e}")

class GameManager:
    def __init__(self):
        pygame.init()
        
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Until the Sun Rises")
        self.screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "MENU"

        self.font_death = pygame.font.Font(None, 64)
        self.font_title = pygame.font.Font(None, 50)
        self.font_medium = pygame.font.Font(None, 28)
        self.font_small = pygame.font.Font(None, 20)

        self.selected_index = 0
        self.player_name_input = ""
        self.current_score = 0
        self.score_saved = False
        self.game_world = None

        self.death_timer = 0.0
        self.death_duration = 3.5  

    @property
    def menu_options(self):
        if self.game_world is not None:
            return ["CONTINUAR", "NOVO JOGO", "HISTÓRICO", "CRÉDITOS", "SAIR"]
        return ["JOGAR", "HISTÓRICO", "CRÉDITOS", "SAIR"]

    def start_game(self):
        try:
            self.game_world = GameWorld()
            self.state = "PLAYING"
        except Exception as e:
            print(f"Erro ao criar GameWorld: {e}")

    def resume_game(self):
        if self.game_world:
            self.state = "PLAYING"
        else:
            self.start_game()

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            events = pygame.event.get()
            
            self.handle_events(events)

            if self.state == "MENU":
                self.draw_menu()

            elif self.state == "PLAYING":
                if self.game_world:
                    self.game_world.update(dt, events)
                    self.game_world.draw(self.screen)

                    if hasattr(self.game_world, 'player') and not self.game_world.player.is_alive:
                        self.current_score = getattr(self.game_world.player, 'score', 0)
                        self.player_name_input = ""
                        self.score_saved = False
                        self.death_timer = 0.0
                        self.state = "DIED_ANIMATION"
                    elif getattr(self.game_world, 'is_victorious', False):
                        self.current_score = getattr(self.game_world.player, 'score', 0) + 5000
                        self.player_name_input = ""
                        self.score_saved = False
                        self.state = "VICTORY"

            elif self.state == "DIED_ANIMATION":
                self.death_timer += dt
                if self.death_timer >= self.death_duration:
                    self.game_world = None  
                    self.state = "GAMEOVER"
                else:
                    self.draw_death_screen()

            elif self.state == "GAMEOVER":
                self.draw_game_over_screen()
                
            elif self.state == "VICTORY":
                self.draw_victory()

            elif self.state == "SCORES":
                self.draw_scores_screen()

            elif self.state == "CREDITS":
                self.draw_credits_screen()

            scaled = pygame.transform.scale(self.screen, (WINDOW_WIDTH, WINDOW_HEIGHT))
            self.window.blit(scaled, (0, 0))
            
            pygame.display.flip()
            
        pygame.quit()

    def handle_events(self, events):
        options = self.menu_options

        for event in events:
            if event.type == pygame.QUIT:
                self.running = False

            elif self.state == "MENU":
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_UP, pygame.K_w):
                        self.selected_index = (self.selected_index - 1) % len(options)
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        self.selected_index = (self.selected_index + 1) % len(options)
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        self.execute_menu_option()
                    elif event.key == pygame.K_ESCAPE and self.game_world is not None:
                        self.resume_game()

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mx, my = event.pos
                    mx = mx * (SCREEN_WIDTH / WINDOW_WIDTH)
                    my = my * (SCREEN_HEIGHT / WINDOW_HEIGHT)
                    
                    start_y = SCREEN_HEIGHT // 2 - 10
                    for idx in range(len(options)):
                        rect = pygame.Rect(SCREEN_WIDTH // 2 - 120, start_y + (idx * 40), 240, 35)
                        if rect.collidepoint(mx, my):
                            self.selected_index = idx
                            self.execute_menu_option()

            elif self.state == "PLAYING":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.selected_index = 0
                        self.state = "MENU"

            elif self.state == "DIED_ANIMATION":
                if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_ESCAPE, pygame.K_SPACE):
                    self.game_world = None
                    self.state = "GAMEOVER"

            elif self.state in ("SCORES", "CREDITS"):
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_SPACE):
                        self.state = "MENU"

            elif self.state in ("GAMEOVER", "VICTORY"):
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if not self.score_saved:
                            save_score(self.player_name_input, self.current_score)
                            self.score_saved = True
                        if self.state == "VICTORY":
                            self.game_world = None
                        self.state = "MENU"
                    elif event.key == pygame.K_BACKSPACE:
                        self.player_name_input = self.player_name_input[:-1]
                    else:
                        if len(self.player_name_input) < 12 and event.unicode.isprintable():
                            self.player_name_input += event.unicode

    def execute_menu_option(self):
        if self.game_world is not None:
            if self.selected_index == 0:
                self.resume_game()
            elif self.selected_index == 1:
                self.start_game()
            elif self.selected_index == 2:
                self.state = "SCORES"
            elif self.selected_index == 3:
                self.state = "CREDITS"
            elif self.selected_index == 4:
                self.running = False
        else:
            if self.selected_index == 0:
                self.start_game()
            elif self.selected_index == 1:
                self.state = "SCORES"
            elif self.selected_index == 2:
                self.state = "CREDITS"
            elif self.selected_index == 3:
                self.running = False

    def draw_menu(self):
        dark_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        dark_overlay.fill((0, 0, 0, 130))
        self.screen.blit(dark_overlay, (0, 0))

        title_txt = "PAUSA" if self.game_world is not None else "UNTIL THE SUN RISES"
        title_surf = self.font_title.render(title_txt, True, (255, 55, 25))
        self.screen.blit(title_surf, title_surf.get_rect(center=(SCREEN_WIDTH // 2, 70)))

        options = self.menu_options
        start_y = SCREEN_HEIGHT // 2 - 10

        for idx, option in enumerate(options):
            is_selected = (idx == self.selected_index)
            color = (255, 255, 255) if is_selected else (160, 160, 160)
            
            rect = pygame.Rect(SCREEN_WIDTH // 2 - 120, start_y + (idx * 40), 240, 35)
            if is_selected:
                pygame.draw.rect(self.screen, (255, 255, 255), rect, 2, border_radius=5)
            
            text_surf = self.font_medium.render(option, True, color)
            self.screen.blit(text_surf, text_surf.get_rect(center=rect.center))

    def draw_death_screen(self):
        if self.game_world:
            self.game_world.draw(self.screen)

        progress = min(1.0, self.death_timer / (self.death_duration * 0.7))
        alpha = int(progress * 220)
        
        dark_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        dark_overlay.fill((0, 0, 0, alpha))
        self.screen.blit(dark_overlay, (0, 0))

        banner_height = 130
        banner = pygame.Surface((SCREEN_WIDTH, banner_height), pygame.SRCALPHA)
        banner.fill((10, 0, 0, min(230, alpha)))
        self.screen.blit(banner, (0, (SCREEN_HEIGHT // 2) - (banner_height // 2)))

        text_alpha = int(min(255, (self.death_timer / 1.0) * 255))
        scale = 1.0 + (self.death_timer / self.death_duration) * 0.15
        
        base_surf = self.font_death.render("VOCÊ MORREU", True, (180, 20, 20))
        scaled_w = int(base_surf.get_width() * scale)
        scaled_h = int(base_surf.get_height() * scale)
        text_surf = pygame.transform.smoothscale(base_surf, (scaled_w, scaled_h))
        text_surf.set_alpha(text_alpha)

        rect = text_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 10))
        self.screen.blit(text_surf, rect)

    def draw_scores_screen(self):
        dark_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        dark_overlay.fill((0, 0, 0, 180))
        self.screen.blit(dark_overlay, (0, 0))

        title = self.font_title.render("HISTÓRICO", True, (255, 55, 25))
        self.screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 50)))

        scores = load_scores()
        if not scores:
            empty_txt = self.font_medium.render("Nenhuma pontuação registrada.", True, (255, 55, 25))
            self.screen.blit(empty_txt, empty_txt.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
        else:
            for idx, item in enumerate(scores):
                txt = f"{idx + 1}. {item['name']} - {item['score']} pts"
                surf = self.font_medium.render(txt, True, (255, 255, 255))
                self.screen.blit(surf, (SCREEN_WIDTH // 2 - 100, 90 + (idx * 22)))

        back_txt = self.font_small.render("Pressione ENTER ou ESC para voltar ao Menu", True, (255, 255, 255))
        self.screen.blit(back_txt, back_txt.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20)))

    def draw_credits_screen(self):
        dark_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        dark_overlay.fill((0, 0, 0, 180))
        self.screen.blit(dark_overlay, (0, 0))

        title = self.font_title.render("CRÉDITOS", True, (255, 255, 255))
        self.screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 50)))

        credits_lines = [
            "Until the Sun Rises",
            "",
            "Desenvolvimento:",
            "Equipe do Projeto",
            "",
            "Obrigado por jogar!"
        ]

        for idx, line in enumerate(credits_lines):
            color = (255, 0, 0) if idx == 0 else (255, 255, 255)
            surf = self.font_medium.render(line, True, color)
            self.screen.blit(surf, surf.get_rect(center=(SCREEN_WIDTH // 2, 110 + (idx * 30))))

        back_txt = self.font_small.render("Pressione ENTER ou ESC para voltar", True, (200, 200, 200))
        self.screen.blit(back_txt, back_txt.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20)))

    def draw_game_over_screen(self):
        dark_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        dark_overlay.fill((0, 0, 0, 190))
        self.screen.blit(dark_overlay, (0, 0))

        title = self.font_title.render("FIM DE JOGO", True, (255, 50, 50))
        self.screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 70)))

        score_txt = self.font_medium.render(f"Pontuação Final: {self.current_score}", True, (255, 255, 255))
        self.screen.blit(score_txt, score_txt.get_rect(center=(SCREEN_WIDTH // 2, 130)))

        prompt_txt = self.font_small.render("Digite seu nome e pressione ENTER para salvar:", True, (200, 200, 200))
        self.screen.blit(prompt_txt, prompt_txt.get_rect(center=(SCREEN_WIDTH // 2, 180)))

        input_rect = pygame.Rect(SCREEN_WIDTH // 2 - 120, 210, 240, 40)
        pygame.draw.rect(self.screen, (255, 255, 255), input_rect, 2, border_radius=5)
        
        display_name = self.player_name_input if self.player_name_input else "_"
        name_surf = self.font_medium.render(display_name, True, (135, 206, 250))
        self.screen.blit(name_surf, name_surf.get_rect(center=input_rect.center))

    def draw_victory(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((255, 255, 200, 100))
        self.screen.blit(overlay, (0, 0))
        
        victory_text = self.font_title.render("VOCÊ SOBREVIVEU!", True, (50, 200, 50))
        text_rect = victory_text.get_rect(center=(SCREEN_WIDTH // 2, 70))
        self.screen.blit(victory_text, text_rect)

        score_txt = self.font_medium.render(f"Pontuação Final: {self.current_score}", True, (0, 0, 0))
        self.screen.blit(score_txt, score_txt.get_rect(center=(SCREEN_WIDTH // 2, 130)))
        
        prompt_txt = self.font_small.render("Digite seu nome e pressione ENTER para salvar:", True, (50, 50, 50))
        self.screen.blit(prompt_txt, prompt_txt.get_rect(center=(SCREEN_WIDTH // 2, 180)))

        input_rect = pygame.Rect(SCREEN_WIDTH // 2 - 120, 210, 240, 40)
        pygame.draw.rect(self.screen, (0, 0, 0), input_rect, 2, border_radius=5)
        
        display_name = self.player_name_input if self.player_name_input else "_"
        name_surf = self.font_medium.render(display_name, True, (50, 50, 200))
        self.screen.blit(name_surf, name_surf.get_rect(center=input_rect.center))