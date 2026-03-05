import pygame
import random

from src.core.constants import *
from src.core.collision_manager import CollisionManager
from src.entities.player_object import PlayerObject
from src.entities.enemy_object import EnemyObject
from src.entities.bullet_object import BulletObject


class GameWorld:
    def __init__(self):
        self.player = PlayerObject(
            SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 250, color=(0, 255, 0))
        self.enemies = []
        self.bullets = []
        self.spawn_timer = 0
        self.shoot_timer = 0
        self.collision_manager = CollisionManager(
            self.player, self.enemies, self.bullets)

    def spawn_enemy(self, dt):
        self.spawn_timer += dt
        if self.spawn_timer > 1.5:
            self.spawn_timer = 0
            spawn_x = random.choice([-20, SCREEN_WIDTH + 20])
            spawn_y = random.randint(0, SCREEN_HEIGHT)
            self.enemies.append(EnemyObject(
                spawn_x, spawn_y, 150, (255, 0, 0), 15, self.player))

    def update(self, dt):
        self.player.update(dt)
        self.spawn_enemy(dt)
        self.handle_shoot(dt)

        for enemy in self.enemies:
            enemy.update(dt)

        for bullet in self.bullets[:]:
            bullet.update(dt)
            if bullet.is_off_screen():
                self.bullets.remove(bullet)

        self.collision_manager.update()

    def draw(self, screen):
        screen.fill(DARK_FILTER)

        for enemy in self.enemies:
            enemy.draw(screen)

        for bullet in self.bullets:
            bullet.draw(screen)

        self.player.draw(screen)

    def handle_shoot(self, dt):
        self.shoot_timer += dt
        mouse_pressed = pygame.mouse.get_pressed()
        if mouse_pressed[0] and self.shoot_timer >= 0.3:
            self.shoot_timer = 0
            mouse_pos = pygame.math.Vector2(pygame.mouse.get_pos())
            self.bullets.append(BulletObject(
                self.player.position.x, self.player.position.y, mouse_pos))