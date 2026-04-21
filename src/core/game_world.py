import math
import random
import pygame

from src.core.constants import *
from core.collision_manager import CollisionManager
from src.entities.player_object import PlayerObject
from src.entities.enemy_object import EnemyObject
from src.entities.bullet_object import BulletObject


class GameWorld:
    def __init__(self):
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()

        self.player = PlayerObject(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 250)
        self.all_sprites.add(self.player)

        self.spawn_timer = 0
        self.shoot_timer = 0
        self.game_time = 0

        self.collision_manager = CollisionManager(self.player, self.enemies, self.bullets)

        pygame.mixer.music.load("assets/sounds/ambient_wind.mp3")
        pygame.mixer.music.play(-1)

        self.fog = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.light_radius = 175
        self._setup_light_texture()

    def _setup_light_texture(self):
        self.base_light = pygame.Surface((self.light_radius * 2, self.light_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.base_light, (100, 100, 100), (self.light_radius, self.light_radius), 40)
        cone_points = [(self.light_radius, self.light_radius), (self.light_radius * 2, self.light_radius - 60),
                       (self.light_radius * 2, self.light_radius + 60)]
        pygame.draw.polygon(self.base_light, (255, 255, 255), cone_points)

    def spawn_enemy(self, dt):
        self.game_time += dt
        self.spawn_timer += dt
        if self.spawn_timer > max(0.5, 1.5 - (self.game_time / 60)):
            self.spawn_timer = 0

            spawn_x, spawn_y = self._get_random_spawn_pos()

            lv2 = random.random() < min(0.4, 0.1 + (self.game_time / 120))
            enemy = EnemyObject(spawn_x, spawn_y, 130 if lv2 else 150, 15, self.player,
                                max_health=2 if lv2 else 1, z_level=2 if lv2 else 1)

            self.enemies.add(enemy)
            self.all_sprites.add(enemy)

    def _get_random_spawn_pos(self):
        side = random.choice(['top', 'bottom', 'left', 'right'])
        if side == 'top': return random.randint(0, SCREEN_WIDTH), -50
        if side == 'bottom': return random.randint(0, SCREEN_WIDTH), SCREEN_HEIGHT + 50
        if side == 'left': return -50, random.randint(0, SCREEN_HEIGHT)
        return SCREEN_WIDTH + 50, random.randint(0, SCREEN_HEIGHT)

    def handle_collisions(self, dt):
        hits = pygame.sprite.groupcollide(self.enemies, self.bullets, False, True)
        for enemy in hits:
            enemy.take_damage(1)

        zombies_touching = pygame.sprite.spritecollide(self.player, self.enemies, False)
        for zombie in zombies_touching:
            if not zombie.is_dead:
                self.player.take_damage(30 * dt)

    def update(self, dt, events):
        if not self.player.is_alive:
            pygame.mixer.music.stop()
            return

        self.all_sprites.update(dt)

        self.spawn_enemy(dt)
        self.handle_shoot(dt, events)
        self.collision_manager.update(dt)

    def draw(self, screen):
        screen.fill(DARK_FILTER)
        self.all_sprites.draw(screen)
        self._draw_fog(screen)
        self.draw_ui(screen)

    def _draw_fog(self, screen):
        self.fog.fill((15, 15, 15))
        raw_mouse = pygame.mouse.get_pos()
        dx = (raw_mouse[0] / ZOOM) - self.player.position.x
        dy = (raw_mouse[1] / ZOOM) - self.player.position.y
        angle = math.degrees(math.atan2(-dy, dx))

        rotated_light = pygame.transform.rotate(self.base_light, angle)
        light_rect = rotated_light.get_rect(center=(int(self.player.position.x), int(self.player.position.y)))

        self.fog.blit(rotated_light, light_rect, special_flags=pygame.BLEND_RGBA_ADD)
        screen.blit(self.fog, (0, 0), special_flags=pygame.BLEND_MULT)

    def draw_ui(self, screen):
        if self.player.is_alive:
            pygame.draw.rect(screen, (0, 0, 0), (20, 20, 200, 20))
            hp_w = int(200 * (self.player.current_health / self.player.max_health))
            pygame.draw.rect(screen, (0, 255, 0), (20, 20, hp_w, 20))

    def handle_shoot(self, dt, events):
        self.shoot_timer += dt
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.shoot_timer >= 0.3:
                    self.shoot_timer = 0
                    self.player.shoot_sfx.play()

                    raw_m = pygame.mouse.get_pos()
                    m_pos = pygame.math.Vector2(raw_m[0] / ZOOM, raw_m[1] / ZOOM)
                    bullet = BulletObject(self.player.position.x, self.player.position.y, m_pos)

                    self.bullets.add(bullet)
                    self.all_sprites.add(bullet)