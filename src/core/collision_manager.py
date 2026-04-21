import pygame


class CollisionManager:
    def __init__(self, player, enemy_group, bullet_group, walls):
        self.player = player
        self.enemy_group = enemy_group
        self.bullet_group = bullet_group
        self.walls = walls  

    def update(self, dt):
        self._handle_bullet_enemy_collisions()
        self._handle_player_enemy_collisions(dt)

        self.check_wall_collisions(self.player)
        for enemy in self.enemy_group:
            if not enemy.is_dead:
                self.check_wall_collisions(enemy)

    def _handle_bullet_enemy_collisions(self):
        for bullet in self.bullet_group:
            if bullet.rect.collidelist(self.walls) != -1:
                bullet.kill()

        hits = pygame.sprite.groupcollide(
            self.bullet_group, self.enemy_group, True, False, pygame.sprite.collide_circle
        )
        for bullet, struck_enemies in hits.items():
            for enemy in struck_enemies:
                if not enemy.is_dead:
                    enemy.take_damage(1)

    def _handle_player_enemy_collisions(self, dt):
        collisions = pygame.sprite.spritecollide(
            self.player, self.enemy_group, False, pygame.sprite.collide_circle
        )
        for enemy in collisions:
            if not enemy.is_dead:
                self.player.take_damage(30 * dt)

    def check_wall_collisions(self, dynamic_obj):
        idx = dynamic_obj.rect.collidelist(self.walls)
        if idx != -1:
            wall_rect = self.walls[idx]

            if dynamic_obj.velocity.x > 0:
                dynamic_obj.rect.right = wall_rect.left
            elif dynamic_obj.velocity.x < 0:
                dynamic_obj.rect.left = wall_rect.right

            if dynamic_obj.velocity.y > 0:
                dynamic_obj.rect.bottom = wall_rect.top
            elif dynamic_obj.velocity.y < 0:
                dynamic_obj.rect.top = wall_rect.bottom

            dynamic_obj.position.x = float(dynamic_obj.rect.centerx)
            dynamic_obj.position.y = float(dynamic_obj.rect.centery)