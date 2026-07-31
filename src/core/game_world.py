import math
import random
import pygame
import pytmx
import pyscroll

from src.core.constants import *
from src.core.collision_manager import CollisionManager
from src.core.upgrade_manager import UpgradeManager
from src.core.sprite_manager import SpriteManager
from src.entities.player_object import PlayerObject
from src.entities.enemy_object import EnemyObject
from src.entities.bullet_object import BulletObject
from src.entities.landmine_object import LandmineObject
from src.entities.explosion_effect import ExplosionEffect
from src.entities.xp_object import XPObject

class GameWorld:
    def __init__(self):
        self.tmx_data = pytmx.util_pygame.load_pygame("assets/maps/game-map.tmx")
        map_data = pyscroll.data.TiledMapData(self.tmx_data)
        self.map_layer = pyscroll.orthographic.BufferedRenderer(
            map_data, (SCREEN_WIDTH, SCREEN_HEIGHT), clamp_camera=True
        )
        self.map_layer.zoom = ZOOM
        
        entities_layer_index = None
        for i, layer in enumerate(self.tmx_data.layers):
            if layer.name == "entities_layer":
                entities_layer_index = i
                break
                
        if entities_layer_index is None:
            entities_layer_index = len(self.tmx_data.layers) - 1
            
        self.all_sprites = pyscroll.PyscrollGroup(
            map_layer=self.map_layer,
            default_layer=entities_layer_index
        )
        
        self.enemies = []
        self.bullets = []
        self.landmines = []
        self.xp_gems = []
        self.effects = []
        self.zombie_spawn = []
        self.collisions = []
        
        self._setup_from_tmx()
        
        self.spawn_timer = 0
        self.shoot_timer = 0
        self.game_time = 0
        self.upgrade_manager = UpgradeManager(self.player)
        self.collision_manager = CollisionManager(self)
        
        pygame.mixer.music.load("assets/sounds/ambient_wind.mp3")
        pygame.mixer.music.play(-1)
        
        self.fog = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.light_radius = 175
        self.ui_font = pygame.font.Font(None, 28)
        self.ui_font_small = pygame.font.Font(None, 20)
        self.last_player_level = 1

    def add_entity(self, entity, logic_list):
        logic_list.append(entity)
        visual = SpriteManager(entity)
        self.all_sprites.add(visual)

    def add_xp(self, xp_entity):
        self.add_entity(xp_entity, self.xp_gems)

    def get_screen_mouse_pos(self):
        raw_m = pygame.mouse.get_pos()
        win_w, win_h = pygame.display.get_surface().get_size()
        mx = raw_m[0] * (SCREEN_WIDTH / win_w)
        my = raw_m[1] * (SCREEN_HEIGHT / win_h)
        return mx, my

    def get_world_mouse_pos(self):
        raw_m = pygame.mouse.get_pos()
        win_w, win_h = pygame.display.get_surface().get_size()
        mx = raw_m[0] * (SCREEN_WIDTH / win_w)
        my = raw_m[1] * (SCREEN_HEIGHT / win_h)
        cam_x = self.map_layer.view_rect.x
        cam_y = self.map_layer.view_rect.y
        world_x = (mx / self.map_layer.zoom) + cam_x
        world_y = (my / self.map_layer.zoom) + cam_y
        return pygame.math.Vector2(world_x, world_y)

    def _setup_light_texture(self):
        self.base_light = pygame.Surface((self.light_radius * 2, self.light_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.base_light, (100, 100, 100), (self.light_radius, self.light_radius), 40)
        cone_points = [(self.light_radius, self.light_radius), (self.light_radius * 2, self.light_radius - 60),
                       (self.light_radius * 2, self.light_radius + 60)]
        pygame.draw.polygon(self.base_light, (255, 255, 255), cone_points)

    def _setup_from_tmx(self):
        for obj in self.tmx_data.get_layer_by_name("entities_layer"):
            if obj.type == "spawn":
                if obj.name == "player":
                    self.player = PlayerObject(pygame.math.Vector2(obj.x, obj.y), 125)
                    self.all_sprites.add(SpriteManager(self.player))
                elif obj.name == "zombie":
                    self.zombie_spawn.append(pygame.math.Vector2(obj.x, obj.y))
        for obj in self.tmx_data.get_layer_by_name("collision_layer"):
            self.collisions.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

    def spawn_enemy(self, dt):
        self.game_time += dt
        self.spawn_timer += dt
        if self.spawn_timer > max(0.5, 1.5 - (self.game_time / 60)):
            self.spawn_timer = 0
            if not self.zombie_spawn:
                return
            spawn_pos = random.choice(self.zombie_spawn)
            lv2_chance = min(0.4, 0.1 + (self.game_time / 120))
            if random.random() < lv2_chance:
                level = 3 if random.random() < 0.40 else 2
            else:
                level = 1
            enemy = EnemyObject(position=spawn_pos, target=self.player, level=level)
            self.add_entity(enemy, self.enemies)

    def _get_random_spawn_pos(self):
        side = random.choice(['top', 'bottom', 'left', 'right'])
        if side == 'top': return random.randint(0, SCREEN_WIDTH), -50
        if side == 'bottom': return random.randint(0, SCREEN_WIDTH), SCREEN_HEIGHT + 50
        if side == 'left': return -50, random.randint(0, SCREEN_HEIGHT)
        return SCREEN_WIDTH + 50, random.randint(0, SCREEN_HEIGHT)

    def update(self, dt, events):
        if not self.player.is_alive:
            pygame.mixer.music.stop()
            return
            
        if self.player.level > self.last_player_level:
            self.last_player_level = self.player.level
            self.upgrade_manager.trigger_level_up()
            
        if self.upgrade_manager.is_paused_for_levelup:
            self.upgrade_manager.handle_events(events, self.get_screen_mouse_pos)
            return
            
        world_mouse = self.get_world_mouse_pos()
        
        self.player.update(dt, world_mouse)
        for bullet in self.bullets: bullet.update(dt, world_mouse)
        for enemy in self.enemies: enemy.update(dt, world_mouse)
        for gem in self.xp_gems: gem.update(dt, world_mouse)
        for effect in self.effects: effect.update(dt, world_mouse)
        
        self.bullets = [b for b in self.bullets if getattr(b, 'active', True)]
        self.enemies = [e for e in self.enemies if getattr(e, 'active', True)]
        self.xp_gems = [g for g in self.xp_gems if getattr(g, 'active', True)]
        self.landmines = [m for m in self.landmines if getattr(m, 'active', True)]
        self.effects = [ef for ef in self.effects if getattr(ef, 'active', True)]
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    new_mine = LandmineObject(self.player.position)
                    self.add_entity(new_mine, self.landmines)
                    
        for mine in self.landmines:
            should_explode = mine.update(dt)
            if should_explode:
                self.explode_mine(mine)
                mine.kill()
                
        self.spawn_enemy(dt)
        self.handle_shoot(dt, events, world_mouse)
        self.collision_manager.update(dt)
        
        for gem in self.xp_gems:
            if getattr(gem, 'active', True) and self.player.position.distance_to(gem.position) < 15:
                self.player.gain_xp(gem.xp_value)
                gem.kill()
                
        self.all_sprites.center(self.player.rect.center)
        self.all_sprites.update(dt)

    def draw(self, screen):
        self.all_sprites.draw(screen)
        self.draw_health_bar(screen)
        self.draw_xp_bar(screen)
        self.upgrade_manager.draw(screen, self.get_screen_mouse_pos)

    def _draw_fog(self, screen):
        self.fog.fill((15, 15, 15))
        world_mouse = self.get_world_mouse_pos()
        dx = world_mouse.x - self.player.position.x
        dy = world_mouse.y - self.player.position.y
        angle = math.degrees(math.atan2(-dy, dx))
        rotated_light = pygame.transform.rotate(self.base_light, angle)
        cam_x, cam_y = self.map_layer.get_center_offset()
        screen_player_x = (self.player.position.x - cam_x) * self.map_layer.zoom
        screen_player_y = (self.player.position.y - cam_y) * self.map_layer.zoom
        light_rect = rotated_light.get_rect(center=(int(screen_player_x), int(screen_player_y)))
        self.fog.blit(rotated_light, light_rect, special_flags=pygame.BLEND_RGBA_ADD)
        screen.blit(self.fog, (0, 0), special_flags=pygame.BLEND_MULT)

    def draw_health_bar(self, screen):
        if self.player.is_alive:
            pygame.draw.rect(screen, (0, 0, 0), (20, 30, 200, 20))
            hp_w = int(200 * (self.player.current_health / self.player.max_health))
            pygame.draw.rect(screen, (0, 255, 0), (20, 30, hp_w, 20))

    def draw_xp_bar(self, screen):
        if self.player.is_alive:
            pygame.draw.rect(screen, (40, 40, 40), (0, 0, SCREEN_WIDTH, 15))
            xp_w = int(SCREEN_WIDTH * (self.player.current_xp / self.player.xp_to_next_level))
            pygame.draw.rect(screen, (0, 150, 255), (0, 0, xp_w, 15))
            pygame.draw.line(screen, (0, 0, 0), (0, 15), (SCREEN_WIDTH, 15), 2)
            lvl_str = f"LVL {self.player.level}"
            shadow_text = self.ui_font.render(lvl_str, True, (0, 0, 0))
            shadow_rect = shadow_text.get_rect(topright=(SCREEN_WIDTH - 18, 27))
            screen.blit(shadow_text, shadow_rect)
            lvl_text = self.ui_font.render(lvl_str, True, (255, 255, 255))
            lvl_rect = lvl_text.get_rect(topright=(SCREEN_WIDTH - 20, 25))
            screen.blit(lvl_text, lvl_rect)

    def handle_shoot(self, dt, events, world_mouse):
        self.shoot_timer += dt
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.shoot_timer >= 0.3:
                    self.shoot_timer = 0
                    if hasattr(self.player, 'shoot_sfx'):
                        self.player.shoot_sfx.play()
                    bullet = BulletObject(self.player.position, world_mouse)
                    self.add_entity(bullet, self.bullets)
                    
    def explode_mine(self, mine):
        explosion = ExplosionEffect(mine.position)
        self.add_entity(explosion, self.effects)
        for enemy in self.enemies:
            if getattr(enemy, 'is_alive', True):
                enemy_pos = pygame.math.Vector2(enemy.rect.center)
                distance = enemy_pos.distance_to(mine.position)
                
                if distance <= mine.blast_radius:
                    enemy.take_damage(mine.damage)
                    if not enemy.is_alive:
                        self.add_xp(XPObject(enemy.position, self.player, xp_value=20))