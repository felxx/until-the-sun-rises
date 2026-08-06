import math
import pygame
from src.entities.dynamic_object import DynamicObject
from src.core.resource_manager import ResourceManager
from src.core.animation import Animation, AnimationCache


class BulletObject(DynamicObject):
    _bullet_anim_cache = None

    def __init__(self, position, target_pos):
        super().__init__(position, speed=800, hitbox_size=(4, 4), combat_radius=5)
        self.start_pos = position
        self.max_range = 1000

        if BulletObject._bullet_anim_cache is None:
            bullet_paths = [f"assets/images/bullet/shot{i}.png" for i in range(1, 5)]
            frames = [ResourceManager.get_image(p, 32) for p in bullet_paths]
            BulletObject._bullet_anim_cache = AnimationCache(frames)

        self.animation = Animation(BulletObject._bullet_anim_cache, fps=15)

        direction = pygame.math.Vector2(target_pos) - self.position
        if direction.length() > 0:
            self.velocity = direction.normalize() * self.speed
            self.angle = math.degrees(math.atan2(-self.velocity.y, self.velocity.x)) - 90
        else:
            self.velocity = pygame.math.Vector2(0, 0)
            self.angle = 0

        self.image = self.animation.get_image(self.angle)
        self.rect = self.image.get_rect(center=self.position)
        self._layer = 3

    def resolve_behavior(self, dt):
        pass

    def update(self, dt, world_mouse=None):
        super().update(dt)

        distance = self.position.distance_to(self.start_pos)
        if distance > self.max_range:
            self.active = False

    def render(self, dt):
        self.animation.update(dt)
        self.image = self.animation.get_image(self.angle)
        super().render(dt)