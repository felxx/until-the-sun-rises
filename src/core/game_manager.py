import pygame
import sys
from src.core.constants import *
from src.core.game_world import GameWorld

class GameManager:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Until The Sun Rises")
        
        self.screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        
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
            
            scaled_screen = pygame.transform.scale(self.screen, (WINDOW_WIDTH, WINDOW_HEIGHT))

            self.window.blit(scaled_screen, (0, 0))
            pygame.display.flip()
        
        pygame.quit()
        sys.exit()