import pygame
import random
from src.core.constants import SCREEN_WIDTH, SCREEN_HEIGHT

class UpgradeManager:
    def __init__(self, player):
        self.player = player
        self.is_paused_for_levelup = False
        self.offered_upgrades = []
        self.upgrade_cards_rects = []
        
        self.ui_font = pygame.font.Font(None, 24)
        self.ui_font_small = pygame.font.Font(None, 18)
        
        if not hasattr(self.player, 'base_speed'):
            self.player.base_speed = self.player.speed
        if not hasattr(self.player, 'base_damage'):
            self.player.base_damage = self.player.damage

        self.upgrade_pool = [
            {"name": "Agilidade", "desc": "Velocidade(+5%)", "action": self._upgrade_speed},
            {"name": "Vitalidade", "desc": "Vida Max (+15)", "action": self._upgrade_health},
            {"name": "Kit Tático", "desc": "Cura 30% Max HP (+10)", "action": self._upgrade_heal},
            {"name": "Calibre Pesado", "desc": "Dano Extra (+10%)", "action": self._upgrade_damage},
            {"name": "Gatilho Rápido", "desc": "Cadência (+10%)", "action": self._upgrade_fire_rate},
            {"name": "Magnetismo", "desc": "Alcance de XP (+25%)", "action": self._upgrade_magnet},
            {"name": "Pele de Ferro", "desc": "Redução de Dano (+5%)", "action": self._upgrade_armor},
            {"name": "Bala Perfurante", "desc": "Tiros perfuram +1 zumbi", "action": self._upgrade_piercing},
            {"name": "Tiro Múltiplo", "desc": "Dispara +1 projétil", "action": self._upgrade_multishot},
            {"name": "Mira Fatal", "desc": "Chance de Crítico (+10%)", "action": self._upgrade_crit},
            {"name": "Sabedoria", "desc": "Bônus de XP (+15%)", "action": self._upgrade_xp_boost},
            {"name": "Regeneração", "desc": "Cura +0.5 HP / seg", "action": self._upgrade_regen},
            {"name": "Munição Gélida", "desc": "Tiros lentificam (15%)", "action": self._upgrade_cryo}
        ]
        
        self.level_up_start_time = 0
        self.delay_per_card = 0.4

    def _upgrade_speed(self):
        self.player.speed += (self.player.base_speed * 0.05)

    def _upgrade_health(self):
        self.player.max_health += 15
        self.player.current_health += 15

    def _upgrade_heal(self):
        self.player.max_health += 10
        heal_amount = self.player.max_health * 0.30
        self.player.current_health = min(self.player.max_health, self.player.current_health + heal_amount)

    def _upgrade_damage(self):
        self.player.damage += (self.player.base_damage * 0.10)

    def _upgrade_fire_rate(self):
        current_cooldown = getattr(self.player, 'shoot_cooldown', 0.3)
        self.player.shoot_cooldown = max(0.1, current_cooldown * 0.90)

    def _upgrade_magnet(self):
        current_radius = getattr(self.player, 'pickup_radius', 15)
        self.player.pickup_radius = current_radius * 1.25

    def _upgrade_armor(self):
        current_armor = getattr(self.player, 'damage_reduction', 0.0)
        self.player.damage_reduction = min(0.60, current_armor + 0.05)

    def _upgrade_piercing(self):
        current_pierce = getattr(self.player, 'pierce_count', 1)
        self.player.pierce_count = current_pierce + 1

    def _upgrade_multishot(self):
        current_multi = getattr(self.player, 'multishot', 1)
        self.player.multishot = current_multi + 1

    def _upgrade_crit(self):
        current_crit = getattr(self.player, 'crit_chance', 0.0)
        self.player.crit_chance = min(0.50, current_crit + 0.10)

    def _upgrade_xp_boost(self):
        current_boost = getattr(self.player, 'xp_multiplier', 1.0)
        self.player.xp_multiplier = current_boost + 0.15

    def trigger_level_up(self):
        self.is_paused_for_levelup = True
        self.level_up_start_time = pygame.time.get_ticks()
        self._generate_upgrades()

    def _upgrade_regen(self):
        current_regen = getattr(self.player, 'health_regen', 0.0)
        self.player.health_regen = current_regen + 0.5

    def _upgrade_cryo(self):
        current_slow = getattr(self.player, 'cryo_slow', 0.0)
        self.player.cryo_slow = min(0.60, current_slow + 0.15)

    def _generate_upgrades(self):
        sample_size = min(3, len(self.upgrade_pool))
        self.offered_upgrades = random.sample(self.upgrade_pool, sample_size)
        self.upgrade_cards_rects = []
        
        card_w = 180 
        card_h = 220 
        gap = 20     
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