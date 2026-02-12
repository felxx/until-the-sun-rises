import pygame
import random
from settings import *
from entities.player import Player
from entities.enemy import Enemy

class GameWorld:
    def __init__(self):
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.enemies = []
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
        for enemy in self.enemies:
            enemy.update(dt)

    def draw(self, screen):
        screen.fill(DARK_FILTER)
        self.player.draw(screen)
        for enemy in self.enemies:
            enemy.draw(screen)