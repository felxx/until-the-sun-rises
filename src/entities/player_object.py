import math
import pygame

from src.entities.dynamic_object import DynamicObject
from src.core.constants import ZOOM

class PlayerObject(DynamicObject):
    def __init__(self, x, y, speed, color, radius=15):
        super().__init__(x, y, speed, color, radius)

        self.max_health = 100
        self.current_health = 100
        self.is_alive = True
        self.damage_timer = 0 

        self.shoot_sfx = pygame.mixer.Sound("assets/shoot.wav")
        self.shoot_sfx.set_volume(0.9)

        self.frames = []
        for i in range(1, 10):
            path = f"assets/rifle{i}.png"
            try:
                img = pygame.image.load(path).convert_alpha()
                img = pygame.transform.scale(img, (64, 64))
                self.frames.append(img)
            except (pygame.error, FileNotFoundError):
                surf = pygame.Surface((64, 64), pygame.SRCALPHA)
                pygame.draw.circle(surf, (0, 255, 0), (32, 32), 15)
                self.frames.append(surf)

        self.frame_index = 0
        self.angle = 0
        self.original_image = self.frames[0]
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))

    def take_damage(self, amount):
        if self.is_alive:
            self.current_health -= amount
            self.damage_timer = 0.1 
            if self.current_health <= 0:
                self.current_health = 0
                self.is_alive = False

                pygame.mixer.music.stop()
                pygame.mixer.stop()

    def resolve_behavior(self, dt):
        if not self.is_alive:
            self.velocity = pygame.math.Vector2(0, 0)
            return

        keys = pygame.key.get_pressed()
        move_x = keys[pygame.K_d] - keys[pygame.K_a]
        move_y = keys[pygame.K_s] - keys[pygame.K_w]
        
        self.velocity = pygame.math.Vector2(move_x, move_y)
        
        if self.velocity.length() > 0:
            self.velocity = self.velocity.normalize() * self.speed
        else:
            self.velocity = pygame.math.Vector2(0, 0)

    def update(self, dt):
        if not self.is_alive:
            return

        super().update(dt)
        
        if self.damage_timer > 0:
            self.damage_timer -= dt

        if self.velocity.length() > 0:
            self.frame_index += 12 * dt
            if self.frame_index >= len(self.frames):
                self.frame_index = 0
        else:
            self.frame_index = 0

        raw_mouse_x, raw_mouse_y = pygame.mouse.get_pos()
        mouse_x = raw_mouse_x / ZOOM
        mouse_y = raw_mouse_y / ZOOM
        
        rel_x = mouse_x - self.position.x
        rel_y = mouse_y - self.position.y
        self.angle = math.degrees(math.atan2(-rel_y, rel_x)) - 270

        self.original_image = self.frames[int(self.frame_index)]
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        
        if self.damage_timer > 0:
            self.image.fill((255, 100, 100), special_flags=pygame.BLEND_RGB_MULT)

        self.rect = self.image.get_rect(center=(int(self.position.x), int(self.position.y)))

    def draw(self, screen):
        if self.is_alive:
            screen.blit(self.image, self.rect)