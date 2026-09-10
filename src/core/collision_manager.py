import pygame
from src.entities.xp_object import XPObject

class CollisionManager:
    def __init__(self, game_world):
        self.world = game_world

    def update(self, dt):
        self._handle_bullet_enemy_collisions()
        self._handle_player_enemy_collisions(dt)
        self.check_wall_collisions(self.world.player)
        
        for enemy in self.world.enemies:
            if getattr(enemy, 'is_alive', True) and getattr(enemy, 'active', True):
                self.check_wall_collisions(enemy)

    def _handle_bullet_enemy_collisions(self):
        import random
        for bullet in self.world.bullets:
            if not getattr(bullet, 'active', True):
                continue
                
            if bullet.hitbox.collidelist(self.world.collisions) != -1:
                bullet.kill()
                continue
                
            for enemy in self.world.enemies:
                if getattr(enemy, 'is_alive', True) and getattr(enemy, 'active', True):
                    if bullet.hitbox.colliderect(enemy.hitbox):

                        if enemy in getattr(bullet, 'hit_enemies', []):
                            continue
                            
                        bullet.hit_enemies.append(enemy)

                        base_damage = getattr(self.world.player, 'damage', 1)
                        crit_chance = getattr(self.world.player, 'crit_chance', 0.0)
                        
                        is_crit = random.random() < crit_chance
                        final_damage = base_damage * 2.0 if is_crit else base_damage
                        
                        enemy.take_damage(final_damage)

                        slow_factor = getattr(self.world.player, 'cryo_slow', 0.0)
                        if slow_factor > 0:
                            if not hasattr(enemy, 'base_speed'):
                                enemy.base_speed = enemy.speed
                            enemy.speed = max(20.0, enemy.base_speed * (1.0 - slow_factor))
                                                
                        if not enemy.is_alive:
                            xp_amount = getattr(enemy, 'xp_value', 10)
                            xp = XPObject(enemy.position, self.world.player, xp_value=xp_amount)
                            self.world.add_xp(xp)
                            self.world.player.score += xp_amount * 10
                        
                        max_pierce = getattr(self.world.player, 'pierce_count', 1)
                        if len(bullet.hit_enemies) >= max_pierce:
                            bullet.kill()
                            break
                        
    def _handle_player_enemy_collisions(self, dt):
        if not getattr(self.world.player, 'is_alive', True):
            return

        for enemy in self.world.enemies:
            if getattr(enemy, 'is_alive', True) and getattr(enemy, 'active', True):
                if self.world.player.hitbox.colliderect(enemy.hitbox):
                    self.world.player.take_damage(enemy.damage * dt)

                overlap_vec = enemy.position - self.world.player.position
                dist = overlap_vec.length()
                
                min_dist = 12

                if 0 < dist < min_dist:
                    push_factor = min_dist - dist
                    enemy.position += overlap_vec.normalize() * push_factor
                    
                    enemy.hitbox.center = (int(enemy.position.x), int(enemy.position.y))
                    if hasattr(enemy, 'rect'):
                        enemy.rect.center = enemy.hitbox.center

    def check_wall_collisions(self, obj):
        if not hasattr(obj, 'hitbox'):
            return
            
        for wall in self.world.collisions:
            if obj.hitbox.colliderect(wall):
                overlap_left = obj.hitbox.right - wall.left
                overlap_right = wall.right - obj.hitbox.left
                overlap_top = obj.hitbox.bottom - wall.top
                overlap_bottom = wall.bottom - obj.hitbox.top
                
                min_overlap = min(overlap_left, overlap_right, overlap_top, overlap_bottom)
                
                correction = pygame.math.Vector2(0, 0)
                
                if min_overlap == overlap_left:
                    correction.x = -overlap_left
                elif min_overlap == overlap_right:
                    correction.x = overlap_right
                elif min_overlap == overlap_top:
                    correction.y = -overlap_top
                elif min_overlap == overlap_bottom:
                    correction.y = overlap_bottom
                    
                obj.position += correction
                
                obj.hitbox.center = (int(obj.position.x), int(obj.position.y))
                if hasattr(obj, 'rect'):
                    obj.rect.center = obj.hitbox.center