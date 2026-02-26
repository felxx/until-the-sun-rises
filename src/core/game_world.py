from src.core.constants import *
from src.entities.player_object import PlayerObject
from src.entities.enemy_object import EnemyObject 
from src.core.constants import *
import random 

class GameWorld:
    def __init__(self):
        self.player = PlayerObject(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 250, color=(0, 255, 0))
        self.objects = [self.player]
        self.spawn_timer = 0

    def spawn_enemy(self, dt):
        self.spawn_timer += dt
        if self.spawn_timer > 1.5:
            self.spawn_timer = 0
            spawn_x = random.choice([-20, SCREEN_WIDTH + 20])
            spawn_y = random.randint(0, SCREEN_HEIGHT)
            self.objects.append(EnemyObject(spawn_x, spawn_y, 150, (255, 0, 0), 15, self.player))

    def update(self, dt):
        self.spawn_enemy(dt)
        for obj in self.objects:
            obj.update(dt)

    def draw(self, screen):
        screen.fill(DARK_FILTER)
        for obj in self.objects:
            obj.draw(screen)