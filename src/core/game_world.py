import math
import random
import pytmx
import pyscroll

from src.core.constants import *
from src.core.game_scene import GameScene
from src.core.collision_manager import CollisionManager
from src.core.upgrade_manager import UpgradeManager
from src.entities.player_object import PlayerObject
from src.entities.enemy_object import EnemyObject
from src.entities.bullet_object import BulletObject

class GameWorld(GameScene):
    def __init__(self, manager):
        super().__init__(manager)
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
        self.xp_gems = []
        self.zombie_spawn = []
        self.collisions = []
        
        self._setup_from_tmx()
        
        self.spawn_timer = 0
        self.shoot_timer = 0
        self.game_time = 0
        self.score = 0
        
        self.upgrade_manager = UpgradeManager(self.player)
        self.collision_manager = CollisionManager(self)
        
        pygame.mixer.music.load("assets/sounds/ambient_wind.mp3")
        pygame.mixer.music.play(-1)
        
        self.fog = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.DAWN_DURATION = DAWN_DURATION 
        self.NIGHT_COLOR = DARK_FILTER
        self.DAY_COLOR = DAY_FILTER
        
        self.flashlight_range = 280
        self.flashlight_angle = 50 
        self.aura_radius = 300 
        
        self.base_light = self._create_light_texture()
        self.light_cache = {}
        self.ui_font = pygame.font.Font(None, 28)
        self.ui_font_small = pygame.font.Font(None, 20)
        self.last_player_level = 1
        
        self.is_victorious = False

    def _create_light_texture(self):
        size = self.flashlight_range * 2 + 100
        center = (size // 2, size // 2)
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        
        aura_steps = 50
        for i in range(aura_steps, 0, -1):
            r = int(self.aura_radius * (i / aura_steps))
            factor = 1.0 - (i / aura_steps)
            intensity = int(200 * (factor ** 2.5)) 
            pygame.draw.circle(surface, (intensity, intensity, intensity, 255), center, r)
            
        cone_steps = 35
        half_angle = self.flashlight_angle / 2.0
        
        center_vec = pygame.math.Vector2(center)
        
        for i in range(cone_steps, 0, -1):
            curr_dist = self.flashlight_range * (i / cone_steps)
            factor = 1.0 - (i / cone_steps)
            intensity = int(240 * (factor ** 0.85)) 
            arc_points = [center]
            num_segments = 16
            
            for seg in range(num_segments + 1):
                angle_deg = -half_angle + (self.flashlight_angle * seg / num_segments)
                
                offset = pygame.math.Vector2()
                offset.from_polar((curr_dist, angle_deg))
                
                point = center_vec + offset
                arc_points.append((point.x, point.y))
                
            pygame.draw.polygon(surface, (intensity, intensity, intensity, 255), arc_points)
            
        return surface

    def add_entity(self, entity, logic_list):
        logic_list.append(entity)
        self.all_sprites.add(entity.sprite)

    def cleanup_dead_entities(self):
        for i in range(len(self.enemies) - 1, -1, -1):
            if not self.enemies[i].active:
                self.enemies[i].sprite.kill()
                self.enemies.pop(i)

        for i in range(len(self.bullets) - 1, -1, -1):
            if not self.bullets[i].active:
                self.bullets[i].sprite.kill()
                self.bullets.pop(i)

        for i in range(len(self.xp_gems) - 1, -1, -1):
            if not self.xp_gems[i].active:
                self.xp_gems[i].sprite.kill()
                self.xp_gems.pop(i)

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

    def _setup_from_tmx(self):
        for obj in self.tmx_data.get_layer_by_name("entities_layer"):
            if obj.type == "spawn":
                if obj.name == "player":
                    self.player = PlayerObject(pygame.math.Vector2(obj.x, obj.y), 125)
                    self.all_sprites.add(self.player.sprite)
                elif obj.name == "zombie":
                    self.zombie_spawn.append(pygame.math.Vector2(obj.x, obj.y))
        for obj in self.tmx_data.get_layer_by_name("collision_layer"):
            self.collisions.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

    def spawn_enemy(self, dt):
        if self.is_victorious:
            return
            
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

    def handle_events(self, events):
        if getattr(self, 'upgrade_manager', None) and self.upgrade_manager.is_paused_for_levelup:
            self.upgrade_manager.handle_events(events, self.get_screen_mouse_pos)
            return

        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                from src.core.menus import MainMenuScreen
                self.manager.change_scene(MainMenuScreen(self.manager, paused_world=self))
                return
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.shoot_timer >= 0.3:
                    self.shoot_timer = 0
                    if hasattr(self.player, 'shoot_sfx'):
                        self.player.shoot_sfx.play()
                    world_mouse = self.get_world_mouse_pos()
                    bullet = BulletObject(self.player.position, world_mouse)
                    self.add_entity(bullet, self.bullets)

    def update(self, dt):
        if not self.player.is_alive:
            pygame.mixer.music.stop()
            from src.core.menus import DeathAnimationScene
            self.manager.change_scene(DeathAnimationScene(self.manager, self))
            return
            
        if getattr(self, 'is_victorious', False):
            pygame.mixer.music.stop()
            from src.core.menus import InputScoreScene
            self.manager.change_scene(InputScoreScene(self.manager, self.player.score + 5000, is_victory=True))
            return
            
        self.game_time += dt
        if self.game_time >= self.DAWN_DURATION:
            self.is_victorious = True
            for enemy in self.enemies:
                enemy.take_damage(9999)
            return
            
        if self.player.level > self.last_player_level:
            self.last_player_level = self.player.level
            self.upgrade_manager.trigger_level_up()
            
        if self.upgrade_manager.is_paused_for_levelup:
            return

        world_mouse = self.get_world_mouse_pos()
        self.player.update(dt, world_mouse)
        for bullet in self.bullets: bullet.update(dt, world_mouse)
        for enemy in self.enemies: enemy.update(dt, world_mouse)
        for gem in self.xp_gems: gem.update(dt, world_mouse)
        
        self.spawn_enemy(dt)
        self.shoot_timer += dt
        self.collision_manager.update(dt)
        
        for gem in self.xp_gems:
            if gem.active and self.player.position.distance_to(gem.position) < 15:
                self.player.gain_xp(gem.xp_value)
                gem.active = False
                
        self.cleanup_dead_entities()
        self.all_sprites.center(self.player.position)
        self.all_sprites.update(dt)

    def render(self, screen):
        self.all_sprites.draw(screen)
        self._draw_fog(screen)
        self.draw_health_bar(screen)
        self.draw_xp_bar(screen)
        self.draw_score(screen)
        self.upgrade_manager.draw(screen, self.get_screen_mouse_pos)

    def _draw_fog(self, screen):
        progress = min(1.0, self.game_time / self.DAWN_DURATION)
        
        r = int(self.NIGHT_COLOR[0] + (self.DAY_COLOR[0] - self.NIGHT_COLOR[0]) * progress)
        g = int(self.NIGHT_COLOR[1] + (self.DAY_COLOR[1] - self.NIGHT_COLOR[1]) * progress)
        b = int(self.NIGHT_COLOR[2] + (self.DAY_COLOR[2] - self.NIGHT_COLOR[2]) * progress)
        ambient_color = (r, g, b)
        
        self.fog.fill(ambient_color)
        
        if progress >= 1.0:
            return
            
        world_mouse = self.get_world_mouse_pos()
        
        direction = world_mouse - self.player.position
        
        angle = math.degrees(math.atan2(-direction.y, direction.x))
        approx_angle = int(angle // 5) * 5
        
        if approx_angle not in self.light_cache:
            self.light_cache[approx_angle] = pygame.transform.rotate(self.base_light, approx_angle)
            
        rotated_light = self.light_cache[approx_angle]
        
        cam_pos = pygame.math.Vector2(self.map_layer.view_rect.topleft)
        
        screen_player_pos = (self.player.position - cam_pos) * self.map_layer.zoom
        
        light_rect = rotated_light.get_rect(center=(int(screen_player_pos.x), int(screen_player_pos.y)))
        
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
            xp_ratio = min(1.0, self.player.current_xp / max(1, self.player.xp_to_next_level))
            xp_w = int(SCREEN_WIDTH * xp_ratio)
            pygame.draw.rect(screen, (0, 150, 255), (0, 0, xp_w, 15))
            pygame.draw.line(screen, (0, 0, 0), (0, 15), (SCREEN_WIDTH, 15), 2)
            
            lvl_str = f"LVL {self.player.level}"
            shadow_text = self.ui_font.render(lvl_str, True, (0, 0, 0))
            shadow_rect = shadow_text.get_rect(topright=(SCREEN_WIDTH - 18, 27))
            screen.blit(shadow_text, shadow_rect)
            
            lvl_text = self.ui_font.render(lvl_str, True, (255, 255, 255))
            lvl_rect = lvl_text.get_rect(topright=(SCREEN_WIDTH - 20, 25))
            screen.blit(lvl_text, lvl_rect)

    def draw_score(self, screen):
        score_str = f"SCORE: {self.player.score}"
        
        margin_x = 20
        margin_y_from_bottom = 35
        
        pos_x = margin_x
        pos_y = SCREEN_HEIGHT - margin_y_from_bottom

        shadow_text = self.ui_font.render(score_str, True, (0, 0, 0))
        shadow_rect = shadow_text.get_rect(topleft=(pos_x + 2, pos_y + 2))
        screen.blit(shadow_text, shadow_rect)
        
        score_text = self.ui_font.render(score_str, True, (255, 255, 255))
        score_rect = score_text.get_rect(topleft=(pos_x, pos_y))
        screen.blit(score_text, score_rect)

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