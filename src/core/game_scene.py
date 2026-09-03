import pygame
from abc import ABC, abstractmethod
from src.core.constants import *

class GameScene(ABC):
    def __init__(self, manager):
        self.manager = manager
        self.font_death = pygame.font.Font(None, 64)
        self.font_title = pygame.font.Font(None, 50)
        self.font_medium = pygame.font.Font(None, 28)
        self.font_small = pygame.font.Font(None, 20)

    @abstractmethod
    def handle_events(self, events):
        pass

    @abstractmethod
    def update(self, dt):
        pass

    @abstractmethod
    def render(self, screen):
        pass

    def draw_overlay(self, screen, alpha=130):
        dark_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        dark_overlay.fill((0, 0, 0, alpha))
        screen.blit(dark_overlay, (0, 0))