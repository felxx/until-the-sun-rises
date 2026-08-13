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

        except Exception:

            return []

    return []



def save_score(player_name, score):

    scores = load_scores()

    scores.append({"name": player_name.strip() if player_name.strip() else "Jogador", "score": score})

    scores.sort(key=lambda x: x["score"], reverse=True)

    scores = scores[:10]

    with open(SCORES_FILE, "w", encoding="utf-8") as f:

        json.dump(scores, f, ensure_ascii=False, indent=2)





class FlameManager:



    def __init__(self, width=160, height=120):

        self.width = width

        self.height = height



        self.palette = [

            (0, 0, 0), (0, 5, 20), (0, 10, 40), (0, 20, 70),

            (0, 30, 100), (0, 45, 130), (0, 60, 160), (0, 80, 185),

            (0, 100, 210), (0, 120, 230), (0, 140, 245), (10, 160, 250),

            (30, 175, 250), (50, 190, 255), (70, 205, 255), (90, 215, 255),

            (110, 225, 255), (130, 230, 255), (150, 235, 255), (170, 240, 255),

            (190, 245, 255), (210, 250, 255), (225, 252, 255), (240, 254, 255),

            (255, 255, 255)

        ]

       

        self.fire_pixels = [0] * (self.width * self.height)

       

        bottom_row_start = (self.height - 1) * self.width

        for x in range(self.width):

            self.fire_pixels[bottom_row_start + x] = len(self.palette) - 1



        self.surface = pygame.Surface((self.width, self.height))

       

        self.time_acc = 0.0

        self.update_rate = 0.05



    def update(self, dt):



        self.time_acc += dt

        if self.time_acc < self.update_rate:

            return

           

        self.time_acc = 0.0

       

        for x in range(self.width):

            for y in range(1, self.height):

                src_index = y * self.width + x

                pixel_val = self.fire_pixels[src_index]



                if pixel_val == 0:

                    self.fire_pixels[src_index - self.width] = 0

                else:

                    decay = random.randint(0, 2)

                    wind = random.randint(0, 1)

                    dst_x = (x - wind) % self.width

                   

                    dst_index = (y - 1) * self.width + dst_x

                    new_val = max(0, pixel_val - decay)

                    self.fire_pixels[dst_index] = new_val



    def draw(self, target_surface):

        pixels_array = pygame.PixelArray(self.surface)

        for x in range(self.width):

            for y in range(self.height):

                color_idx = self.fire_pixels[y * self.width + x]

                pixels_array[x, y] = self.palette[color_idx]

        del pixels_array



        scaled_surface = pygame.transform.scale(self.surface, target_surface.get_size())

        target_surface.blit(scaled_surface, (0, 0))





class GameManager:

    def __init__(self):

        pygame.init()

       

        self.width = 800

        self.height = 600

        self.window = pygame.display.set_mode((self.width, self.height))

        pygame.display.set_caption("Until the Sun Rises")



        self.screen = pygame.Surface((self.width, self.height))

        self.clock = pygame.time.Clock()

        self.running = True

       

        self.flame_effect = FlameManager(width=160, height=120)

        self.state = "MENU"

       

        self.font_title = pygame.font.Font(None, 64)

        self.font_medium = pygame.font.Font(None, 36)

        self.font_small = pygame.font.Font(None, 24)



        self.menu_options = ["JOGAR", "HISTÓRICO", "CRÉDITOS", "SAIR"]

        self.selected_index = 0



        self.player_name_input = ""

        self.current_score = 0

        self.score_saved = False

        self.game_world = None



    def start_game(self):

        try:

            self.game_world = GameWorld()

            self.state = "PLAYING"

        except Exception as e:

            print(f"Erro ao criar GameWorld: {e}")



    def run(self):

        while self.running:

            dt = self.clock.tick(FPS) / 1000.0

            events = pygame.event.get()



            self.handle_events(events)



            if self.state in ("MENU", "SCORES", "CREDITS", "GAMEOVER"):

                self.flame_effect.update(dt)



            if self.state == "MENU":

                self.draw_menu()



            elif self.state == "PLAYING":

                if self.game_world:

                    self.game_world.update(dt, events)

                    self.game_world.draw(self.screen)



                    if hasattr(self.game_world, 'player') and not self.game_world.player.is_alive:

                        self.current_score = getattr(self.game_world, 'score', 0)

                        self.player_name_input = ""

                        self.score_saved = False

                        self.state = "GAMEOVER"



            elif self.state == "GAMEOVER":

                self.draw_game_over_screen()



            elif self.state == "SCORES":

                self.draw_scores_screen()



            elif self.state == "CREDITS":

                self.draw_credits_screen()



            self.window.blit(self.screen, (0, 0))

            pygame.display.flip()



        pygame.quit()



    def handle_events(self, events):

        for event in events:

            if event.type == pygame.QUIT:

                self.running = False



            if self.state == "MENU":

                if event.type == pygame.KEYDOWN:

                    if event.key in (pygame.K_UP, pygame.K_w):

                        self.selected_index = (self.selected_index - 1) % len(self.menu_options)

                    elif event.key in (pygame.K_DOWN, pygame.K_s):

                        self.selected_index = (self.selected_index + 1) % len(self.menu_options)

                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):

                        self.execute_menu_option()



                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                    mx, my = event.pos

                    for idx in range(len(self.menu_options)):

                        rect = pygame.Rect(self.width // 2 - 120, 240 + (idx * 50), 240, 40)

                        if rect.collidepoint(mx, my):

                            self.selected_index = idx

                            self.execute_menu_option()



            elif self.state in ("SCORES", "CREDITS"):

                if event.type == pygame.KEYDOWN:

                    if event.key in (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_SPACE):

                        self.state = "MENU"



            elif self.state == "GAMEOVER":

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_RETURN:

                        save_score(self.player_name_input, self.current_score)

                        self.score_saved = True

                        self.state = "MENU"

                    elif event.key == pygame.K_BACKSPACE:

                        self.player_name_input = self.player_name_input[:-1]

                    else:

                        if len(self.player_name_input) < 12 and event.unicode.isprintable():

                            self.player_name_input += event.unicode



    def execute_menu_option(self):

        if self.selected_index == 0:

            self.start_game()

        elif self.selected_index == 1:

            self.state = "SCORES"

        elif self.selected_index == 2:

            self.state = "CREDITS"

        elif self.selected_index == 3:

            self.running = False



    def draw_menu(self):

        self.flame_effect.draw(self.screen)



        dark_overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        dark_overlay.fill((0, 0, 0, 130))

        self.screen.blit(dark_overlay, (0, 0))



        title_surf = self.font_title.render("UNTIL THE SUN RISES", True, (255, 55, 25))

        self.screen.blit(title_surf, title_surf.get_rect(center=(self.width // 2, 120)))



        for idx, option in enumerate(self.menu_options):

            is_selected = (idx == self.selected_index)

            color = (255, 255, 255) if is_selected else (160, 160, 160)

           

            rect = pygame.Rect(self.width // 2 - 120, 240 + (idx * 50), 240, 40)

            if is_selected:



                pygame.draw.rect(self.screen, (255, 255, 255), rect, 2, border_radius=5)

           

            text_surf = self.font_medium.render(option, True, color)

            self.screen.blit(text_surf, text_surf.get_rect(center=rect.center))



    def draw_scores_screen(self):

        self.flame_effect.draw(self.screen)

        dark_overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        dark_overlay.fill((0, 0, 0, 180))

        self.screen.blit(dark_overlay, (0, 0))



        title = self.font_title.render("HISTÓRICO DE PONTUAÇÃO", True, (255, 55, 25))

        self.screen.blit(title, title.get_rect(center=(self.width // 2, 80)))



        scores = load_scores()

        if not scores:

            empty_txt = self.font_medium.render("Nenhuma pontuação registrada.", True, (255, 55, 25))

            self.screen.blit(empty_txt, empty_txt.get_rect(center=(self.width // 2, 220)))

        else:

            for idx, item in enumerate(scores):

                txt = f"{idx + 1}. {item['name']} — {item['score']} pts"

                surf = self.font_medium.render(txt, True, (255, 255, 255))

                self.screen.blit(surf, (self.width // 2 - 120, 160 + (idx * 35)))



        back_txt = self.font_small.render("Pressione ENTER ou ESC para voltar ao Menu", True, (255, 255, 255))

        self.screen.blit(back_txt, back_txt.get_rect(center=(self.width // 2, self.height - 50)))



    def draw_credits_screen(self):

        self.flame_effect.draw(self.screen)

        dark_overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        dark_overlay.fill((0, 0, 0, 180))

        self.screen.blit(dark_overlay, (0, 0))



        title = self.font_title.render("CRÉDITOS", True, (255, 255, 255))

        self.screen.blit(title, title.get_rect(center=(self.width // 2, 80)))



        credits_lines = [

            "Until the Sun Rises",

            "",

            "Desenvolvimento & Programação:",

            "Equipe do Projeto",

            "",

            "Fundo do Menu:",

            "Chamas Azuis Algorítmicas",

            "",

            "Obrigado por jogar!"

        ]



        for idx, line in enumerate(credits_lines):

            color = (255, 0, 0) if idx == 0 else (255, 255, 255)

            surf = self.font_medium.render(line, True, color)

            self.screen.blit(surf, surf.get_rect(center=(self.width // 2, 160 + (idx * 35))))



        back_txt = self.font_small.render("Pressione ENTER ou ESC para voltar ao Menu", True, (200, 200, 200))

        self.screen.blit(back_txt, back_txt.get_rect(center=(self.width // 2, self.height - 50)))



    def draw_game_over_screen(self):

        self.flame_effect.draw(self.screen)

        dark_overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        dark_overlay.fill((0, 0, 0, 190))

        self.screen.blit(dark_overlay, (0, 0))



        title = self.font_title.render("FIM DE JOGO", True, (255, 50, 50))

        self.screen.blit(title, title.get_rect(center=(self.width // 2, 120)))



        score_txt = self.font_medium.render(f"Pontuação Final: {self.current_score}", True, (255, 255, 255))

        self.screen.blit(score_txt, score_txt.get_rect(center=(self.width // 2, 200)))



        prompt_txt = self.font_small.render("Digite seu nome e pressione ENTER para salvar:", True, (200, 200, 200))

        self.screen.blit(prompt_txt, prompt_txt.get_rect(center=(self.width // 2, 270)))



        input_rect = pygame.Rect(self.width // 2 - 120, 310, 240, 40)

        pygame.draw.rect(self.screen, (255, 255, 255), input_rect, 2, border_radius=5)

       

        name_surf = self.font_medium.render(self.player_name_input, True, (135, 206, 250))

        self.screen.blit(name_surf, name_surf.get_rect(center=input_rect.center)) 

