import math
import pygame
from src.core.animation import Animation
from src.core.animation_cache import AnimationCache
from src.core.animation_set import AnimationSet
from src.entities.character_object import CharacterObject
from src.core.constants import *
from src.core.resource_manager import ResourceManager

class PlayerObject(CharacterObject):
    _player_anim_data = None

    def __init__(self, position, speed, max_health=100, damage=5):
        super().__init__(position, speed, max_health=max_health, damage=damage, hitbox_size=(10, 10), combat_radius=8)
        self.shoot_sfx = ResourceManager.get_sound("assets/sounds/shoot.wav")
        self.shoot_sfx.set_volume(0.9)
        self.original_speed = speed
        self.active_buffs = {}
        
        if PlayerObject._player_anim_data is None:
            rifle_paths = [f"assets/images/player/rifle{i}.png" for i in range(1, 9)]
            frames = [ResourceManager.get_image(p, 32) for p in rifle_paths]
            PlayerObject._player_anim_data = AnimationCache(frames)
            
        self.anim_set = AnimationSet()
        self.anim_set.add_animation("rifle", Animation(PlayerObject._player_anim_data, fps=12))
        
        self.angle = 0
        self._layer = 2
        self.current_xp = 0
        self.level = 1
        self.xp_to_next_level = 100
        self.score = 0

    def die(self):
        self.active = False
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

    def add_buff(self, buff_name, duration, apply_callback=None, remove_callback=None):
        self.active_buffs[buff_name] = duration
        if apply_callback and buff_name not in self.active_buffs:
            apply_callback()

    def update(self, dt, world_mouse):
        if not self.is_alive: return

        expired_buffs = []
        for buff_name, duration in self.active_buffs.items():
            self.active_buffs[buff_name] -= dt
            if self.active_buffs[buff_name] <= 0:
                expired_buffs.append(buff_name)

        for buff_name in expired_buffs:
            del self.active_buffs[buff_name]
            if buff_name == "speed_boost":
                self.speed = self.original_speed

        super().update(dt, world_mouse)
        direction = world_mouse - self.position
        self.angle = math.degrees(math.atan2(-direction.y, direction.x)) + 90

    def render(self, dt):
        is_moving = self.velocity.length() > 0
        is_playing = is_moving if self.is_alive else False

        img = self.anim_set.update_and_get_image(dt, self.angle, is_playing=is_playing)
        if img:
            self.sprite.image = img

    def gain_xp(self, amount):
        if not self.is_alive: return
        self.current_xp += amount
        if self.current_xp >= self.xp_to_next_level:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.current_xp -= self.xp_to_next_level
        self.xp_to_next_level = int(self.xp_to_next_level * 1.5)