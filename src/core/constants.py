import pygame

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
ZOOM = 2
SCREEN_WIDTH = WINDOW_WIDTH // ZOOM
SCREEN_HEIGHT = WINDOW_HEIGHT // ZOOM
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

DARK_FILTER = (10, 10, 20)
DAY_FILTER = (255, 255, 255)
DAWN_DURATION = 600.0

# --- UI palette (identidade pós-apocalíptica / zumbi) ---
BLOOD_RED = (176, 30, 30)           # título, borda de hover
DIM_TEXT = (150, 145, 140)          # botão não selecionado
BRIGHT_TEXT = (225, 220, 210)       # botão selecionado/hover
BACKGROUND_FALLBACK = (18, 16, 16)  # fundo sólido enquanto o vídeo do menu não existe

MENU_FONT_PATH = "assets/fonts/menu-font.ttf"

