import pygame
import math
import os
from src.entities.dynamic_object import DynamicObject

class EnemyObject(DynamicObject):
    def __init__(self, x, y, speed, color, radius, target, max_health=1, z_level=1):
        super().__init__(x, y, speed, color, radius)
        self.target = target
        self.angle = 0
        
        self.max_health = max_health
        self.current_health = self.max_health
        self.z_level = z_level
        
        self.is_dead = False
        self.death_finished = False
        self.death_timer = 0
        self.should_remove = False
        
        sound_file = "assets/zombie.mp3"
        self.volume_multi = 0.4
        
        walk_prefix = "walk_00"
        death_prefix = "death_00"
        
        if self.z_level == 2:
            walk_prefix = "walk_lv2_00"
            death_prefix = "death_lv2_00"
            self.volume_multi = 0.8

        self.zombie_sfx = pygame.mixer.Sound(sound_file)
        self.zombie_sfx.set_volume(0.0)
        self.zombie_sfx.play(loops=-1)
        
        self.walk_frames = []
        self.death_frames = []
        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        assets_dir = os.path.join(base_dir, "..", "..", "assets")

        display_radius = radius * 3
        if self.z_level == 2:
            display_radius *= 1.3

        for i in range(9):
            path = os.path.join(assets_dir, f"{walk_prefix}{i}.png")
            self.walk_frames.append(self._load_and_scale(path, display_radius))

        for i in range(6):
            path = os.path.join(assets_dir, f"{death_prefix}{i}.png")
            self.death_frames.append(self._load_and_scale(path, display_radius))

        self.frame_index = 0
        self.animation_speed = 10
        self.image = self.walk_frames[0]
        self.rect = self.image.get_rect(center=(x, y))

    def _load_and_scale(self, path, size):
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
            self.current_health = 0
            self.frame_index = 0
            self.velocity = pygame.math.Vector2(0, 0)
            self.zombie_sfx.stop()

    def resolve_behavior(self, dt):
        if self.is_dead:
            return
        direction = self.target.position - self.position
        if direction.length_squared() > 0:
            direction = direction.normalize()
            self.velocity = direction * self.speed
            self.angle = math.degrees(math.atan2(-direction.y, direction.x)) - 250
        else:
            self.velocity = pygame.math.Vector2(0, 0)

    def update(self, dt):
        super().update(dt)
        
        if self.is_dead:
            self.death_timer += dt
            if self.death_timer >= 5.0:
                self.should_remove = True

            if not self.death_finished:
                self.frame_index += self.animation_speed * dt
                if self.frame_index >= len(self.death_frames):
                    self.frame_index = len(self.death_frames) - 1
                    self.death_finished = True
            
            current_frame = self.death_frames[int(self.frame_index)]
        else:
            max_audio_dist = 500
            dist = self.position.distance_to(self.target.position)
            
            volume = 1.0 - (dist / max_audio_dist)
            volume = max(0.0, min(1.0, volume))
            self.zombie_sfx.set_volume(volume * self.volume_multi)

            self.frame_index += self.animation_speed * dt
            if self.frame_index >= len(self.walk_frames):
                self.frame_index = 0
            current_frame = self.walk_frames[int(self.frame_index)]
        
        self.image = pygame.transform.rotate(current_frame, self.angle)
        self.rect = self.image.get_rect(center=self.position)

    def draw(self, screen):
        if self.is_dead and self.death_timer > 3.0:
            alpha = max(0, 255 - int((self.death_timer - 3.0) * 127.5))
            self.image.set_alpha(alpha)
            
        screen.blit(self.image, self.rect)