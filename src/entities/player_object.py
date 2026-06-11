import math
import pygame

from src.entities.character_object import CharacterObject
from src.core.constants import *
from src.core.resource_manager import ResourceManager
from src.core.sprite_sheet import SpriteSheet


class PlayerObject(CharacterObject):
    def __init__(self, position, speed, max_health=100, damage=5):
        super().__init__(position, speed, max_health=max_health, damage=damage, hitbox_size=(10, 10), combat_radius=8)

        self.shoot_sfx = ResourceManager.get_sound("assets/sounds/shoot.wav")
        self.shoot_sfx.set_volume(0.9)

        rifle_paths = [f"assets/images/player/rifle{i}.png" for i in range(1, 9)]
        self.sprite_sheet = SpriteSheet(rifle_paths, 32)

        self.frame_index = 0
        self.angle = 0
        self.image = self.sprite_sheet.get_frame(0, 0)
        self.rect = self.image.get_rect(center=self.position)
        self._layer = 2

        self.current_xp = 0
        self.level = 1
        self.xp_to_next_level = 100

    def die(self):
        self.kill()
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

    def update(self, dt, world_mouse):
        if not self.is_alive: return
        super().update(dt, world_mouse)

        if self.velocity.length() > 0:
            self.frame_index = (self.frame_index + 12 * dt) % 9
        else:
            self.frame_index = 0

        rel_x = world_mouse.x - self.position.x
        rel_y = world_mouse.y - self.position.y
        self.angle = math.degrees(math.atan2(-rel_y, rel_x)) + 90

        self.image = self.sprite_sheet.get_frame(self.frame_index, self.angle)

        if self.damage_flash_timer > 0:
            self.image = self.image.copy()
            self.image.fill((255, 100, 100), special_flags=pygame.BLEND_RGB_MULT)

        self.rect = self.image.get_rect(center=(int(self.position.x), int(self.position.y)))

    def gain_xp(self, amount):
        if not self.is_alive: return
        
        self.current_xp += amount
        if self.current_xp >= self.xp_to_next_level:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.current_xp -= self.xp_to_next_level
        self.xp_to_next_level = int(self.xp_to_next_level * 1.5)
