import pygame
from src.entities.xp_object import XPObject

class CollisionManager:
    def __init__(self, player, enemy_group, bullet_group, walls, all_sprites, xp_gems):
        self.player = player
        self.enemy_group = enemy_group
        self.bullet_group = bullet_group
        self.walls = walls
        self.all_sprites = all_sprites
        self.xp_gems = xp_gems

    def update(self, dt):
        self._handle_bullet_enemy_collisions()
        self._handle_player_enemy_collisions(dt)

        self.check_wall_collisions(self.player)
        for enemy in self.enemy_group:
            if not enemy.is_dead:
                self.check_wall_collisions(enemy)

    def _handle_bullet_enemy_collisions(self):
        for bullet in self.bullet_group:
            if bullet.hitbox.collidelist(self.walls) != -1:
                bullet.kill()

        hits = pygame.sprite.groupcollide(
            self.bullet_group, self.enemy_group, True, False, pygame.sprite.collide_circle
        )

        for bullet, struck_enemies in hits.items():
            for enemy in struck_enemies:
                if not enemy.is_dead:
                    enemy.take_damage(1)
                    
                    if enemy.is_dead:
                        xp_amount = 30 if enemy.z_level == 2 else 10
                        xp = XPObject(enemy.position.x, enemy.position.y, self.player, xp_value=xp_amount)
                        
                        self.xp_gems.add(xp)
                        self.all_sprites.add(xp)

    def _handle_player_enemy_collisions(self, dt):
        collisions = pygame.sprite.spritecollide(
            self.player, self.enemy_group, False, pygame.sprite.collide_circle
        )
        for enemy in collisions:
            if not enemy.is_dead:
                self.player.take_damage(30 * dt)

    def check_wall_collisions(self, obj):
        for wall in self.walls:
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
                obj.rect.center = obj.hitbox.center