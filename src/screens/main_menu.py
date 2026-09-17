import pygame
from src.core.constants import *
from src.core.game_scene import GameScene
from src.core.resource_manager import ResourceManager
from src.core.video_player import VideoPlayer

BACKGROUND_VIDEO_PATH = "assets/videos/background-menu.mp4"
MENU_MUSIC_PATH = "assets/sounds/menu-music.ogg"


class MainMenuScreen(GameScene):
    _background_video = None

    def __init__(self, manager, paused_world=None):
        super().__init__(manager)
        self.paused_world = paused_world
        self.selected_index = 0
        if self.paused_world:
            self.options = ["CONTINUAR", "NOVO JOGO", "HISTÓRICO", "CRÉDITOS", "SAIR"]
        else:
            self.options = ["JOGAR", "HISTÓRICO", "CRÉDITOS", "SAIR"]

            if MainMenuScreen._background_video is None:
                MainMenuScreen._background_video = VideoPlayer(
                    BACKGROUND_VIDEO_PATH, SCREEN_WIDTH, SCREEN_HEIGHT
                )

            ResourceManager.play_music(MENU_MUSIC_PATH)

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

                if self.paused_world:
                    for idx, rect in enumerate(self._paused_button_rects()):
                        if rect.collidepoint(mx, my):
                            self.selected_index = idx
                            self.execute_option()
                else:
                    for idx, rect in enumerate(self._button_rects()):
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
        if not self.paused_world:
            MainMenuScreen._background_video.update(dt)

    def _button_rects(self):
        rects = []
        start_y = 150
        for idx, option in enumerate(self.options):
            color = BRIGHT_TEXT if idx == self.selected_index else DIM_TEXT
            text_surf = self.font_medium.render(option, True, color)
            text_rect = text_surf.get_rect(topleft=(40, start_y + idx * 40))
            rects.append(text_rect.inflate(16, 10))
        return rects

    def _paused_button_rects(self):
        rects = []
        start_y = 120 if len(self.options) > 4 else 140
        for idx, option in enumerate(self.options):
            color = BRIGHT_TEXT if idx == self.selected_index else DIM_TEXT
            text_surf = self.font_medium.render(option, True, color)
            center = (SCREEN_WIDTH // 2, start_y + idx * 40 + 17)
            text_rect = text_surf.get_rect(center=center)
            rects.append(text_rect.inflate(16, 10))
        return rects

    def render(self, screen):
        if self.paused_world:
            self.paused_world.render(screen)
            self.draw_overlay(screen)

            title_txt = "PAUSA"
            title_surf = self.font_title.render(title_txt, True, BLOOD_RED)
            screen.blit(title_surf, title_surf.get_rect(center=(SCREEN_WIDTH // 2, 70)))

            button_rects = self._paused_button_rects()
            start_y = 120 if len(self.options) > 4 else 140
            for idx, option in enumerate(self.options):
                is_selected = (idx == self.selected_index)
                color = BRIGHT_TEXT if is_selected else DIM_TEXT
                text_surf = self.font_medium.render(option, True, color)
                center = (SCREEN_WIDTH // 2, start_y + idx * 40 + 17)
                text_rect = text_surf.get_rect(center=center)

                if is_selected:
                    pygame.draw.rect(screen, BLOOD_RED, button_rects[idx], 2, border_radius=3)

                screen.blit(text_surf, text_rect)
        else:
            screen.blit(MainMenuScreen._background_video.get_frame(), (0, 0))
            self.draw_overlay(screen)

            title_surf = self.font_title.render("UNTIL THE SUN RISES", True, BLOOD_RED)
            screen.blit(title_surf, title_surf.get_rect(topleft=(40, 60)))

            start_y = 150
            button_rects = self._button_rects()
            for idx, option in enumerate(self.options):
                is_selected = (idx == self.selected_index)
                color = BRIGHT_TEXT if is_selected else DIM_TEXT
                text_surf = self.font_medium.render(option, True, color)
                text_rect = text_surf.get_rect(topleft=(40, start_y + idx * 40))

                if is_selected:
                    pygame.draw.rect(screen, BLOOD_RED, button_rects[idx], 2, border_radius=3)

                screen.blit(text_surf, text_rect)
