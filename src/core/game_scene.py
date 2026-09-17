import pygame
from abc import ABC, abstractmethod
from src.core.constants import *
from src.core.resource_manager import ResourceManager

class GameScene(ABC):
    def __init__(self, manager):
        self.manager = manager
        self.font_death = ResourceManager.get_font(MENU_FONT_PATH, 64)
        self.font_title = ResourceManager.get_font(MENU_FONT_PATH, 50)
        self.font_medium = ResourceManager.get_font(MENU_FONT_PATH, 28)
        self.font_small = ResourceManager.get_font(MENU_FONT_PATH, 20)

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