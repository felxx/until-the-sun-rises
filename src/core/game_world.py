import pygame
import random
import math

from src.core.constants import *
from src.core.collision_manager import CollisionManager
from src.entities.player_object import PlayerObject
from src.entities.enemy_object import EnemyObject
from src.entities.bullet_object import BulletObject

class GameWorld:
    def __init__(self):
        self.player = PlayerObject(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 250, color=(0, 255, 0))
        self.enemies = []
        self.bullets = []
        self.spawn_timer = 0
        self.shoot_timer = 0
        self.game_time = 0
        
        pygame.mixer.music.load("assets/ambient_wind.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
        
        self.fog = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.light_radius = 350 
        
        self.base_light = pygame.Surface((self.light_radius * 2, self.light_radius * 2), pygame.SRCALPHA)
        
        pygame.draw.circle(self.base_light, (100, 100, 100), (self.light_radius, self.light_radius), 60)
        
        cone_points = [
            (self.light_radius, self.light_radius),
            (self.light_radius * 2, self.light_radius - 140),
            (self.light_radius * 2, self.light_radius + 140)          
        ]
        pygame.draw.polygon(self.base_light, (255, 255, 255), cone_points)
        self.collision_manager = CollisionManager(
            self.player, self.enemies, self.bullets)

    def spawn_enemy(self, dt):
        self.game_time += dt
        self.spawn_timer += dt
        
        # O intervalo de spawn diminui conforme o tempo passa
        spawn_interval = max(0.5, 1.5 - (self.game_time / 60))
        
        if self.spawn_timer > spawn_interval:
            self.spawn_timer = 0
            
            # Spawn em qualquer borda da tela
            side = random.choice(['top', 'bottom', 'left', 'right'])
            if side == 'top':
                spawn_x, spawn_y = random.randint(0, SCREEN_WIDTH), -50
            elif side == 'bottom':
                spawn_x, spawn_y = random.randint(0, SCREEN_WIDTH), SCREEN_HEIGHT + 50
            elif side == 'left':
                spawn_x, spawn_y = -50, random.randint(0, SCREEN_HEIGHT)
            else:
                spawn_x, spawn_y = SCREEN_WIDTH + 50, random.randint(0, SCREEN_HEIGHT)
            
            # Chance de spawnar LV 2 (começa em 10% e sobe com o tempo)
            lv2_chance = min(0.4, 0.1 + (self.game_time / 120))
            
            if random.random() < lv2_chance:
                # Zumbi LV 2: Mais vida, som próprio e tamanho maior
                self.enemies.append(EnemyObject(
                    spawn_x, spawn_y, 130, (255, 0, 0), 15, 
                    self.player, max_health=2, z_level=2))
            else:
                # Zumbi básico
                self.enemies.append(EnemyObject(
                    spawn_x, spawn_y, 150, (255, 0, 0), 15, self.player))

    def update(self, dt):
        if not self.player.is_alive:
            pygame.mixer.music.stop()
            return

        self.player.update(dt)
        self.spawn_enemy(dt)
        self.handle_shoot(dt)

        for enemy in self.enemies:
            enemy.update(dt)
            if not enemy.is_dead and self.player.rect.colliderect(enemy.rect):
                self.player.take_damage(30 * dt)

        # Lógica de colisão de projéteis atualizada para suportar vida
        for bullet in self.bullets[:]:
            bullet.update(dt)
            for enemy in self.enemies:
                if not enemy.is_dead and bullet.rect.colliderect(enemy.rect):
                    # Tira 1 de vida do inimigo
                    enemy.take_damage(1)
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                    break # Projétil some após atingir um alvo
            
            if bullet.is_off_screen() and bullet in self.bullets:
                self.bullets.remove(bullet)

        self.enemies = [e for e in self.enemies if not e.should_remove]
        self.collision_manager.update()

    def draw(self, screen):
        screen.fill(DARK_FILTER)
        
        for enemy in self.enemies:
            enemy.draw(screen)
        for bullet in self.bullets:
            bullet.draw(screen)
            
        self.player.draw(screen)
        
        self.fog.fill((15, 15, 15))
        
        mouse_pos = pygame.mouse.get_pos()
        dx = mouse_pos[0] - self.player.position.x
        dy = mouse_pos[1] - self.player.position.y
        
        angle = math.degrees(math.atan2(-dy, dx))
        rotated_light = pygame.transform.rotate(self.base_light, angle)
        light_rect = rotated_light.get_rect(center=(int(self.player.position.x), int(self.player.position.y)))
        
        self.fog.blit(rotated_light, light_rect, special_flags=pygame.BLEND_RGBA_ADD)
        screen.blit(self.fog, (0, 0), special_flags=pygame.BLEND_MULT)

        if self.player.is_alive:
            pygame.draw.rect(screen, (0, 0, 0), (20, 20, 200, 20))
            hp_width = int(200 * (self.player.current_health / self.player.max_health))
            pygame.draw.rect(screen, (0, 255, 0), (20, 20, hp_width, 20))
            pygame.draw.rect(screen, (255, 255, 255), (20, 20, 200, 20), 2)

    def handle_shoot(self, dt):
        self.shoot_timer += dt
        mouse_pressed = pygame.mouse.get_pressed()
        if mouse_pressed[0] and self.shoot_timer >= 0.3:
            self.shoot_timer = 0
            self.player.shoot_sfx.play()
            mouse_pos = pygame.math.Vector2(pygame.mouse.get_pos())
            self.bullets.append(BulletObject(
                self.player.position.x, self.player.position.y, mouse_pos))