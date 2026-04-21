import os
import math
import pygame
from src.entities.dynamic_object import DynamicObject

class EnemyObject(DynamicObject):
    def __init__(self, x, y, speed, radius, target, max_health=1, z_level=1):
        super().__init__(x, y, speed, radius)
        self.target = target
        self.angle = 0
        self.max_health = max_health
        self.current_health = self.max_health
        self.z_level = z_level
        self.is_dead = False
        self.death_finished = False
        self.death_timer = 0
        self.should_remove = False

        self.volume_multi = 0.8 if self.z_level == 2 else 0.4
        self.zombie_sfx = pygame.mixer.Sound("assets/zombie.mp3")
        self.zombie_sfx.set_volume(0.0)
        self._setup_animation_frames(radius)
        self.frame_index = 0
        self.animation_speed = 10
        self.image = self.walk_frames[0]
        self.rect = self.image.get_rect(center=self.position)

    def _setup_animation_frames(self, radius):
        walk_prefix = "walk_lv2_00" if self.z_level == 2 else "walk_00"
        death_prefix = "death_lv2_00" if self.z_level == 2 else "death_00"
        display_radius = (radius * 3) * (1.3 if self.z_level == 2 else 1.0)

        self.walk_frames = [self._load_and_scale(f"{walk_prefix}{i}.png", display_radius) for i in range(9)]
        self.death_frames = [self._load_and_scale(f"{death_prefix}{i}.png", display_radius) for i in range(6)]

    def _load_and_scale(self, filename, size):
        path = os.path.join("assets", filename)
        try:
            img = pygame.image.load(path).convert_alpha()
            return pygame.transform.scale(img, (int(size), int(size)))
        except:
            surf = pygame.Surface((32, 32))
            surf.fill((255, 0, 0))
            return surf

    def take_damage(self, amount):
        if not self.is_dead:
            self.current_health -= amount
            if self.current_health <= 0:
                self.die()

    def die(self):
        if not self.is_dead:
            self.is_dead = True
            self.frame_index = 0
            self.velocity = pygame.math.Vector2(0, 0)
            self.zombie_sfx.stop()

    def resolve_behavior(self, dt):
        if self.is_dead:
            return

        direction = self.target.position - self.position
        distance = direction.length()

        if distance > (self.radius + self.target.radius):
            self.velocity = direction.normalize() * self.speed
            self.angle = math.degrees(math.atan2(-direction.y, direction.x)) - 250
        else:
            self.velocity = pygame.math.Vector2(0, 0)

    def update(self, dt):
        super().update(dt)

        if self.is_dead:
            self._update_death_state(dt)
        else:
            self._update_alive_state(dt)

        self.rect = self.image.get_rect(center=self.rect.center)

    def _update_alive_state(self, dt):
        dist = self.position.distance_to(self.target.position)
        volume = max(0.0, min(1.0, 1.0 - (dist / 500)))
        self.zombie_sfx.set_volume(volume * self.volume_multi)

        self.frame_index = (self.frame_index + self.animation_speed * dt) % len(self.walk_frames)
        current_frame = self.walk_frames[int(self.frame_index)]
        self.image = pygame.transform.rotate(current_frame, self.angle)

    def _update_death_state(self, dt):
        self.death_timer += dt
        if self.death_timer >= 5.0:
            self.should_remove = True
            self.kill()

        if not self.death_finished:
            self.frame_index += self.animation_speed * dt
            if self.frame_index >= len(self.death_frames):
                self.frame_index = len(self.death_frames) - 1
                self.death_finished = True

        current_frame = self.death_frames[int(self.frame_index)]
        self.image = pygame.transform.rotate(current_frame, self.angle)

        if self.death_timer > 3.0:
            alpha = max(0, 255 - int((self.death_timer - 3.0) * 127.5))
            self.image = self.image.copy()
            self.image.set_alpha(alpha)