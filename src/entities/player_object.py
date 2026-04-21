import math
import pygame
from src.entities.dynamic_object import DynamicObject
from src.core.constants import ZOOM
from src.core.resource_manager import ResourceManager
from src.core.sprite_sheet import SpriteSheet

class PlayerObject(DynamicObject):
    def __init__(self, x, y, speed, radius=15):
        super().__init__(x, y, speed, radius)

        self.max_health = 100
        self.current_health = 100
        self.is_alive = True
        self.damage_timer = 0

        self.shoot_sfx = ResourceManager.get_sound("assets/sounds/shoot.wav")
        self.shoot_sfx.set_volume(0.9)

        rifle_paths = [f"assets/images/player/rifle{i}.png" for i in range(1, 10)]
        self.sprite_sheet = SpriteSheet(rifle_paths, 64)

        self.frame_index = 0
        self.angle = 0
        self.image = self.sprite_sheet.get_frame(0, 0)
        self.rect = self.image.get_rect(center=self.position)

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
            self.frame_index = (self.frame_index + 12 * dt) % 9
        else:
            self.frame_index = 0

        raw_mouse_x, raw_mouse_y = pygame.mouse.get_pos()
        rel_x = (raw_mouse_x / ZOOM) - self.position.x
        rel_y = (raw_mouse_y / ZOOM) - self.position.y
        self.angle = math.degrees(math.atan2(-rel_y, rel_x)) - 270

        self.image = self.sprite_sheet.get_frame(self.frame_index, self.angle)

        if self.damage_timer > 0:
            self.image = self.image.copy()
            self.image.fill((255, 100, 100), special_flags=pygame.BLEND_RGB_MULT)

        self.rect = self.image.get_rect(center=(int(self.position.x), int(self.position.y)))