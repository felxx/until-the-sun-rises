import pygame
import random
from src.core.constants import SCREEN_WIDTH, SCREEN_HEIGHT


class UpgradeManager:
    def __init__(self, player):
        self.player = player
        self.is_paused_for_levelup = False
        self.offered_upgrades = []
        self.upgrade_cards_rects = []

        self.ui_font = pygame.font.Font(None, 28)
        self.ui_font_small = pygame.font.Font(None, 20)

        self.upgrade_pool = [
            {"name": "Botas Rápidas", "desc": "+25 Velocidade", "action": self._upgrade_speed},
            {"name": "Vitalidade", "desc": "+25 Vida Máx", "action": self._upgrade_health},
            {"name": "Cura Total", "desc": "Restaura Vida", "action": self._upgrade_heal},
        ]

        self.level_up_start_time = 0
        self.delay_per_card = 0.4

    def _upgrade_speed(self):
        self.player.speed += 25

    def _upgrade_health(self):
        self.player.max_health += 25
        self.player.current_health += 25

    def _upgrade_heal(self):
        self.player.current_health = self.player.max_health

    def trigger_level_up(self):
        self.is_paused_for_levelup = True
        self.level_up_start_time = pygame.time.get_ticks()
        self._generate_upgrades()

    def _generate_upgrades(self):
        sample_size = min(3, len(self.upgrade_pool))
        self.offered_upgrades = random.sample(self.upgrade_pool, sample_size)

        self.upgrade_cards_rects = []
        card_w = 140
        card_h = 200
        gap = 40
        start_x = (SCREEN_WIDTH - (sample_size * card_w + (sample_size - 1) * gap)) // 2

        for i in range(sample_size):
            x = start_x + i * (card_w + gap)
            y = (SCREEN_HEIGHT // 2) - (card_h // 2)
            self.upgrade_cards_rects.append(pygame.Rect(x, y, card_w, card_h))

    def handle_events(self, events, get_mouse_pos_func):
        if not self.is_paused_for_levelup:
            return

        current_time = pygame.time.get_ticks()
        elapsed_seconds = (current_time - self.level_up_start_time) / 1000.0
        total_animation_time = len(self.offered_upgrades) * self.delay_per_card

        if elapsed_seconds < total_animation_time:
            return

        mouse_point = get_mouse_pos_func()

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i, rect in enumerate(self.upgrade_cards_rects):
                    if rect.collidepoint(mouse_point):
                        upgrade = self.offered_upgrades[i]
                        upgrade["action"]()
                        self.is_paused_for_levelup = False

    def draw(self, screen, get_mouse_pos_func):
        if not self.is_paused_for_levelup:
            return

        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        title = self.ui_font.render("Escolha uma melhoria:", True, (255, 215, 0))
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(title, title_rect)

        mouse_point = get_mouse_pos_func()

        current_time = pygame.time.get_ticks()
        elapsed_seconds = (current_time - self.level_up_start_time) / 1000.0
        visible_cards = int(elapsed_seconds / self.delay_per_card)

        visible_cards = min(visible_cards, len(self.offered_upgrades))

        for i in range(visible_cards):
            rect = self.upgrade_cards_rects[i]
            upgrade = self.offered_upgrades[i]

            bg_color = (80, 80, 80) if rect.collidepoint(mouse_point) else (40, 40, 40)

            pygame.draw.rect(screen, bg_color, rect, border_radius=10)
            pygame.draw.rect(screen, (255, 255, 255), rect, width=2, border_radius=10)

            name_txt = self.ui_font.render(upgrade["name"], True, (0, 255, 255))
            name_rect = name_txt.get_rect(center=(rect.centerx, rect.top + 30))
            screen.blit(name_txt, name_rect)

            desc_txt = self.ui_font_small.render(upgrade["desc"], True, (200, 200, 200))
            desc_rect = desc_txt.get_rect(center=(rect.centerx, rect.centery))
            screen.blit(desc_txt, desc_rect)