import pygame
import sys

from src.core.constants import *
from src.core.game_world import GameWorld

class GameManager:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Until The Sun Rises")
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_world = GameWorld()

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            self.game_world.update(dt)
            self.game_world.draw(self.screen)
            pygame.display.flip()
        
        pygame.quit()
        sys.exit()