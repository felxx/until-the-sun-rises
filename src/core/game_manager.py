import pygame

from src.core.constants import *
from src.core.score_manager import ScoreManager
from src.screens.main_menu import MainMenuScreen

class GameManager:
    def __init__(self):
        pygame.init()
        
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Until the Sun Rises")
        self.screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.score_manager = ScoreManager()
        self.current_scene = None
        
        self.change_scene(MainMenuScreen(self))

    def change_scene(self, new_scene):
        self.current_scene = new_scene

    def quit_game(self):
        self.running = False

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            events = pygame.event.get()
            
            for event in events:
                if event.type == pygame.QUIT:
                    self.quit_game()

            if self.current_scene:
                self.current_scene.handle_events(events)
                self.current_scene.update(dt)
                self.current_scene.render(self.screen)

            scaled = pygame.transform.scale(self.screen, (WINDOW_WIDTH, WINDOW_HEIGHT))
            self.window.blit(scaled, (0, 0))
            
            pygame.display.flip()
            
        pygame.quit()