import math
import pygame
from src.entities.dynamic_object import DynamicObject
from src.core.constants import ZOOM


class PlayerObject(DynamicObject):
    def __init__(self, x, y, speed, radius=15):
        super().__init__(x, y, speed, radius)

        self.max_health = 100
        self.current_health = 100
        self.is_alive = True
        self.damage_timer = 0

        self.shoot_sfx = pygame.mixer.Sound("assets/shoot.wav")
        self.shoot_sfx.set_volume(0.9)

        self.frames = self._load_frames()
        self.frame_index = 0
        self.angle = 0

        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=self.position)

    def _load_frames(self):
        frames = []
        for i in range(1, 10):
            path = f"assets/rifle{i}.png"
            try:
                img = pygame.image.load(path).convert_alpha()
                frames.append(pygame.transform.scale(img, (64, 64)))
            except:
                surf = pygame.Surface((64, 64), pygame.SRCALPHA)
                pygame.draw.circle(surf, (0, 255, 0), (32, 32), 15)
                frames.append(surf)
        return frames

    def take_damage(self, amount):
        if self.is_alive:
            self.current_health -= amount
            self.damage_timer = 0.1
            if self.current_health <= 0:
                self.is_alive = False
                self.kill()

    def resolve_behavior(self, dt):
        if not self.is_alive:
            self.velocity = pygame.math.Vector2(0, 0)
            return

        keys = pygame.key.get_pressed()
        move_x = keys[pygame.K_d] - keys[pygame.K_a]
        move_y = keys[pygame.K_s] - keys[pygame.K_w]
        self.velocity = pygame.math.Vector2(move_x, move_y)

    def update(self, dt):
        if not self.is_alive: return
        super().update(dt)

        if self.damage_timer > 0:
            self.damage_timer -= dt

        if self.velocity.length() > 0:
            self.frame_index = (self.frame_index + 12 * dt) % len(self.frames)
        else:
            self.frame_index = 0

        raw_mouse_x, raw_mouse_y = pygame.mouse.get_pos()
        rel_x = (raw_mouse_x / ZOOM) - self.position.x
        rel_y = (raw_mouse_y / ZOOM) - self.position.y
        self.angle = math.degrees(math.atan2(-rel_y, rel_x)) - 270

        self.original_image = self.frames[int(self.frame_index)]
        self.image = pygame.transform.rotate(self.original_image, self.angle)

        if self.damage_timer > 0:
            self.image = self.image.copy()
            self.image.fill((255, 100, 100), special_flags=pygame.BLEND_RGB_MULT)

        self.rect = self.image.get_rect(center=self.rect.center)