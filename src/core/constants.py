import pygame

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
ZOOM = 2

SCREEN_WIDTH = WINDOW_WIDTH // ZOOM  
SCREEN_HEIGHT = WINDOW_HEIGHT // ZOOM  
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# --- SISTEMA DE ILUMINAÇÃO ---
DARK_FILTER = (10, 10, 20)      # escuridão 
DAY_FILTER = (255, 255, 255)    # luz ambiente
DAWN_DURATION = (180.0 * 3)           # transição noite -> dia 