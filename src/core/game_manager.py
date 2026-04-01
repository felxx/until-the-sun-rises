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
        
        self.font_large = pygame.font.Font(None, 64)
        self.font_small = pygame.font.Font(None, 24)

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            
            # Captura a lista de eventos deste frame
            events = pygame.event.get()
            
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r and not self.game_world.player.is_alive:
                        self.game_world = GameWorld()

            # Passamos a lista de eventos para o update do mundo
            self.game_world.update(dt, events)
            
            self.game_world.draw(self.screen)
            
            if not self.game_world.player.is_alive:
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 180)) 
                self.screen.blit(overlay, (0, 0))
                
                game_over_text = self.font_large.render("GAME OVER", True, (255, 50, 50))
                text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
                self.screen.blit(game_over_text, text_rect)
                
                restart_text = self.font_small.render("Pressione 'R' para reiniciar", True, (255, 255, 255))
                restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
                self.screen.blit(restart_text, restart_rect)

            scaled_screen = pygame.transform.scale(self.screen, (WINDOW_WIDTH, WINDOW_HEIGHT))
            self.window.blit(scaled_screen, (0, 0))
            pygame.display.flip()
        
        pygame.quit()
        sys.exit()