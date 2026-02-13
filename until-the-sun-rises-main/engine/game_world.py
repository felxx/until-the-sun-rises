import pygame
import random
from settings import *
from entities.player import Player
from entities.enemy import Enemy
from entities.bullet import Bullet

class GameWorld:
    def __init__(self):
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.enemies = []
        self.bullets = []
        self.shoot_timer = 0
        self.spawn_timer = 0
        self.darkness_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

    def spawn_enemy(self, dt):
        self.spawn_timer += dt
        if self.spawn_timer > 1.0:
            self.spawn_timer = 0
            spawn_x = random.choice([-50, SCREEN_WIDTH + 50])
            spawn_y = random.randint(0, SCREEN_HEIGHT)
            self.enemies.append(Enemy(spawn_x, spawn_y, self.player))

    def update(self, dt):
        self.player.handle_input()
        self.player.update(dt)
        self.spawn_enemy(dt)
        self.shoot_timer += dt
        for enemy in self.enemies:
            enemy.update(dt)
        mouse_pressed = pygame.mouse.get_pressed()
        if mouse_pressed[0] and self.shoot_timer >= 0.3:
            self.shoot_timer = 0
            mouse_pos = pygame.math.Vector2(pygame.mouse.get_pos())
            self.bullets.append(Bullet(self.player.position.x, self.player.position.y, mouse_pos))

        for bullet in self.bullets[:]:
            bullet.update(dt)
            if bullet.is_off_screen():
                if bullet in self.bullets:
                    self.bullets.remove(bullet)

            for enemy in self.enemies[:]:
                for bullet in self.bullets[:]:
                    if bullet.rect.colliderect(enemy.rect):
                        if bullet in self.bullets:
                            self.bullets.remove(bullet)
                        
                        if enemy in self.enemies:
                            self.enemies.remove(enemy)
                        break

    def draw(self, screen):
        screen.fill(DARK_FILTER)
        self.player.draw(screen)
        for enemy in self.enemies:
            enemy.draw(screen)
        for bullet in self.bullets:
            bullet.draw(screen)