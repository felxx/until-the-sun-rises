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
        for bullet in self.world.bullets:
            if not getattr(bullet, 'active', True):
                continue

            if bullet.hitbox.collidelist(self.world.collisions) != -1:
                bullet.kill()
                continue

            for enemy in self.world.enemies:
                if getattr(enemy, 'is_alive', True) and getattr(enemy, 'active', True):
                    if bullet.hitbox.colliderect(enemy.hitbox):
                        enemy.take_damage(getattr(self.world.player, 'damage', 1))
                        bullet.kill()
                        
                        if not enemy.is_alive:
                            xp_amount = getattr(enemy, 'xp_value', 10)
                            xp = XPObject(enemy.position, self.world.player, xp_value=xp_amount)
                            self.world.add_xp(xp)
                        break

    def _handle_player_enemy_collisions(self, dt):
        if not getattr(self.world.player, 'is_alive', True):
            return

        for enemy in self.world.enemies:
            if getattr(enemy, 'is_alive', True) and getattr(enemy, 'active', True):
                if self.world.player.hitbox.colliderect(enemy.hitbox):
                    self.world.player.take_damage(enemy.damage * dt)

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

                if min_overlap == overlap_left:
                    obj.position.x -= overlap_left
                elif min_overlap == overlap_right:
                    obj.position.x += overlap_right
                elif min_overlap == overlap_top:
                    obj.position.y -= overlap_top
                elif min_overlap == overlap_bottom:
                    obj.position.y += overlap_bottom

                obj.hitbox.center = (int(obj.position.x), int(obj.position.y))
                if hasattr(obj, 'rect'):
                    obj.rect.center = obj.hitbox.center