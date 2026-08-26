import pygame
from src.core.constants import *
from src.core.game_world import GameWorld

class GameManager:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_world = GameWorld()
        self.font_large = pygame.font.Font(None, 64)
        self.font_small = pygame.font.Font(None, 24)

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            events = pygame.event.get()
            
            self.handle_events(events)
            self.game_world.update(dt, events)
            self.game_world.draw(self.screen)
            
            if not self.game_world.player.is_alive:
                self.draw_game_over()
            elif self.game_world.is_victorious:
                self.draw_victory()
                
            scaled = pygame.transform.scale(self.screen, (WINDOW_WIDTH, WINDOW_HEIGHT))
            self.window.blit(scaled, (0, 0))
            pygame.display.flip()
            
        pygame.quit()

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    if not self.game_world.player.is_alive or self.game_world.is_victorious:
                        self.game_world = GameWorld()

    def draw_game_over(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        game_over_text = self.font_large.render("GAME OVER", True, (255, 50, 50))
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
        self.screen.blit(game_over_text, text_rect)

        score_text = self.font_small.render(f"Pontuação Final: {self.game_world.player.score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        self.screen.blit(score_text, score_rect)
        
        restart_text = self.font_small.render("Pressione 'R' para reiniciar", True, (255, 255, 255))
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
        self.screen.blit(restart_text, restart_rect)

    def draw_victory(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((255, 255, 200, 100))
        self.screen.blit(overlay, (0, 0))
        
        victory_text = self.font_large.render("VOCÊ SOBREVIVEU!", True, (50, 200, 50))
        text_rect = victory_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
        self.screen.blit(victory_text, text_rect)

        final_score = self.game_world.player.score + 5000
        score_text = self.font_small.render(f"Pontuação Final: {final_score}", True, (0, 0, 0))
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        self.screen.blit(score_text, score_rect)
        
        restart_text = self.font_small.render("Pressione 'R' para jogar novamente", True, (0, 0, 0))
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
        self.screen.blit(restart_text, restart_rect)