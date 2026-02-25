import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        self.animations = {
            "north": self.load_strip("assets/SMS_Soldier_WALK_NORTH_strip4.png"),
            "south": self.load_strip("assets/SMS_Soldier_WALK_SOUTH_strip4.png"),
            "east":  self.load_strip("assets/SMS_Soldier_WALK_EAST_strip4.png"),
            "west":  self.load_strip("assets/SMS_Soldier_WALK_WEST_strip4.png"),
        }
        
        self.direction = "south"
        self.frame_index = 0
        self.image = self.animations[self.direction][self.frame_index]
        
        self.position = pygame.math.Vector2(x, y)
        self.rect = self.image.get_rect(center=(x, y))
        
        self.speed = 200
        self.velocity = pygame.math.Vector2(0, 0)

    def load_strip(self, path):
        """Corta a tira de imagem em 4 quadros"""
        full_sheet = pygame.image.load(path).convert_alpha()
        full_sheet = pygame.transform.scale(full_sheet, (full_sheet.get_width() * 3, full_sheet.get_height() * 3))
        
        w = full_sheet.get_width() // 4
        h = full_sheet.get_height()
        return [full_sheet.subsurface(pygame.Rect(i*w, 0, w, h)) for i in range(4)]

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.velocity.x = keys[pygame.K_d] - keys[pygame.K_a]
        self.velocity.y = keys[pygame.K_s] - keys[pygame.K_w]
        
        if self.velocity.length() > 0:
            self.velocity = self.velocity.normalize()

    def update(self, dt):

        self.position += self.velocity * self.speed * dt
        self.rect.center = self.position

        if self.velocity.length() > 0:
            # Define a direção 
            if abs(self.velocity.x) > abs(self.velocity.y):
                self.direction = "east" if self.velocity.x > 0 else "west"
            else:
                self.direction = "south" if self.velocity.y > 0 else "north"

            # Muda o frame da animação
            self.frame_index += 10 * dt 
            if self.frame_index >= 4: self.frame_index = 0
        else:
            self.frame_index = 0 # Para no frame neutro

        self.image = self.animations[self.direction][int(self.frame_index)]

    def draw(self, screen):
        screen.blit(self.image, self.rect)