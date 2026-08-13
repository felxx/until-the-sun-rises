import math
import random
import pygame
from src.core.animation import Animation
from src.core.animation_cache import AnimationCache
from src.core.animation_set import AnimationSet
from src.entities.character_object import CharacterObject
from src.core.resource_manager import ResourceManager

class EnemyObject(CharacterObject):
    _walk_anim_cache = {}
    _death_anim_cache = {}
    _zombie_sounds = []
    
    ENEMY_PROPERTIES = {
        1: {"speed": 100, "max_health": 5, "damage": 20, "xp_value": 10},
        2: {"speed": 80, "max_health": 10, "damage": 40, "xp_value": 25},
        3: {"speed": 65, "max_health": 15, "damage": 60, "xp_value": 50},
    }

    def __init__(self, position, target, level=1):
        properties = self.ENEMY_PROPERTIES.get(level, self.ENEMY_PROPERTIES[1])
        super().__init__(
            position=position,
            speed=properties["speed"],
            max_health=properties["max_health"],
            damage=properties["damage"],
            hitbox_size=(14, 14),
            combat_radius=15
        )
        self.xp_value = properties["xp_value"]
        self.target = target
        self.level = level
        self.angle = 0
        self.death_finished = False
        self.death_timer = 0
        self.should_remove = False
        
        self._setup_sounds()
        self.sound_timer = random.uniform(1.0, 4.0)
        self._setup_sprites()
        
        self.anim_set = AnimationSet()
        self.anim_set.add_animation("walk", Animation(self._walk_anim_cache[self.level], fps=10))
        self.anim_set.add_animation("death", Animation(self._death_anim_cache[self.level], fps=10, loop=False))
        
        self.frame_index = 0
        self.animation_speed = 10
        self._layer = 2

    def _setup_sounds(self):
        if not EnemyObject._zombie_sounds:
            sound_files = [
                "assets/sounds/katjasavia-female-monster-zombie-218088.mp3",
                "assets/sounds/freesound_community-zombie-growl-3-6863.mp3",
                "assets/sounds/dragon-studio-zombie-sfx-450450.mp3"
            ]
            for file_path in sound_files:
                sound = ResourceManager.get_sound(file_path)
                if sound:
                    sound.set_volume(0.5)
                    EnemyObject._zombie_sounds.append(sound)

    def _setup_sprites(self):
        if self.level not in self._walk_anim_cache:
            if self.level == 3:
                w_paths = [f"assets/images/enemy/lv_3/walk_00{i}.png" for i in range(9)]
                d_paths = [f"assets/images/enemy/lv_3/death_00{i}.png" for i in range(6)]
                w_size, d_size = int(self.radius * 1.5), int(self.radius * 3.2)
            elif self.level == 2:
                w_paths = [f"assets/images/enemy/lv_2/walk_00{i}.png" for i in range(9)]
                d_paths = [f"assets/images/enemy/lv_2/death_00{i}.png" for i in range(6)]
                w_size, d_size = int(self.radius * 2.4), int(self.radius * 2.4)
            else:
                w_paths = [f"assets/images/enemy/lv_1/walk_00{i}.png" for i in range(9)]
                d_paths = [f"assets/images/enemy/lv_1/death_00{i}.png" for i in range(6)]
                w_size, d_size = int(self.radius * 2.2), int(self.radius * 2.2)
            
            w_frames = [ResourceManager.get_image(p, w_size) for p in w_paths]
            d_frames = [ResourceManager.get_image(p, d_size) for p in d_paths]
            EnemyObject._walk_anim_cache[self.level] = AnimationCache(w_frames)
            EnemyObject._death_anim_cache[self.level] = AnimationCache(d_frames)

    def die(self):
        self.velocity = pygame.math.Vector2(0, 0)

    def resolve_behavior(self, dt):
        if not self.is_alive:
            self.velocity = pygame.math.Vector2(0, 0)
            return
        direction = self.target.position - self.position
        dist = direction.length()
        if dist > 1.0:
            self.velocity = direction
            self.angle = math.degrees(math.atan2(-direction.y, direction.x)) - 270
        else:
            self.velocity = pygame.math.Vector2(0, 0)

    def update(self, dt, world_mouse=None):
        super().update(dt)
        if not self.is_alive:
            self.anim_set.set_state("death")
            self.death_timer += dt
            if self.death_timer >= 5.0:
                self.should_remove = True
                self.active = False
        else:
            self.anim_set.set_state("walk")
            self.sound_timer -= dt
            if self.sound_timer <= 0:
                self.sound_timer = random.uniform(4.0, 8.0)
                if random.random() < 0.20 and EnemyObject._zombie_sounds:
                    random.choice(EnemyObject._zombie_sounds).play()

    def render(self, dt):
        return self.anim_set.update_and_get_image(dt, self.angle)