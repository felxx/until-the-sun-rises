import math
import pygame

from src.entities.dynamic_object import DynamicObject
from src.core.resource_manager import ResourceManager
from src.core.sprite_sheet import SpriteSheet


class EnemyObject(DynamicObject):
    _walk_sheets = {}
    _death_sheets = {}

    def __init__(self, x, y, speed, target, max_health=1, z_level=1):
        super().__init__(x, y, speed, hitbox_size=(14, 14), combat_radius=15)
        self.target = target
        self.z_level = z_level
        self.max_health = max_health
        self.current_health = max_health

        self.angle = 0
        self.is_dead = False
        self.death_finished = False
        self.death_timer = 0
        self.should_remove = False

        self.zombie_sfx = ResourceManager.get_sound("assets/sounds/zombie.mp3")
        self.volume_multi = 0.8 if self.z_level == 2 else 0.4

        self._setup_sprites()

        self.frame_index = 0
        self.animation_speed = 10
        self.image = self._walk_sheets[self.z_level].get_frame(0, 0)
        self.rect = self.image.get_rect(center=self.position)
        self._layer = 2

    def _setup_sprites(self):
        if self.z_level not in self._walk_sheets:
            walk_prefix = "lv_2/walk_00" if self.z_level == 2 else "lv_1/walk_00"
            death_prefix = "lv_2/death_00" if self.z_level == 2 else "lv_1/death_00"

            walk_paths = [f"assets/images/enemy/{walk_prefix}{i}.png" for i in range(9)]
            death_paths = [f"assets/images/enemy/{death_prefix}{i}.png" for i in range(6)]
            display_size = int(self.radius * 2.4) if self.z_level == 2 else int(self.radius * 2.2)

            EnemyObject._walk_sheets[self.z_level] = SpriteSheet(walk_paths, display_size)
            EnemyObject._death_sheets[self.z_level] = SpriteSheet(death_paths, display_size)

    def die(self):
        if not self.is_dead:
            self.is_dead = True
            self.frame_index = 0
            self.velocity = pygame.math.Vector2(0, 0)

    def take_damage(self, amount):
        if not self.is_dead:
            self.current_health -= amount
            if self.current_health <= 0:
                self.die()

    def resolve_behavior(self, dt):
        if self.is_dead:
            self.velocity = pygame.math.Vector2(0, 0)
            return

        direction = self.target.position - self.position
        dist = direction.length()

        if dist > (self.radius + self.target.radius):
            self.velocity = direction
            self.angle = math.degrees(math.atan2(-direction.y, direction.x)) - 270
        else:
            self.velocity = pygame.math.Vector2(0, 0)

    def update(self, dt, world_mouse=None):
        super().update(dt)

        if self.is_dead:
            self._update_death_state(dt)
            sheet = self._death_sheets[self.z_level]
        else:
            self._update_alive_state(dt)
            sheet = self._walk_sheets[self.z_level]

        self.image = sheet.get_frame(self.frame_index, self.angle)

        if self.is_dead and self.death_timer > 3.0:
            alpha = max(0, 255 - int((self.death_timer - 3.0) * 127.5))
            self.image = self.image.copy()
            self.image.set_alpha(alpha)

    def _update_alive_state(self, dt):
        self.frame_index = (self.frame_index + self.animation_speed * dt) % 9

    def _update_death_state(self, dt):
        self.death_timer += dt
        if self.death_timer >= 5.0:
            self.should_remove = True
            self.kill()

        if not self.death_finished:
            self.frame_index += self.animation_speed * dt
            if self.frame_index >= 5:
                self.frame_index = 5
                self.death_finished = True