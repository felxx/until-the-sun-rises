import pygame

class CollisionManager:
    def __init__(self, player, enemy_group, bullet_group):
        self.player = player
        self.enemy_group = enemy_group
        self.bullet_group = bullet_group

    def update(self, dt):
        self._handle_bullet_enemy_collisions()
        self._handle_player_enemy_collisions(dt)

    def _handle_bullet_enemy_collisions(self):
        hits = pygame.sprite.groupcollide(
            self.bullet_group,
            self.enemy_group,
            True,
            False,
            pygame.sprite.collide_circle
        )

        for bullet, struck_enemies in hits.items():
            for enemy in struck_enemies:
                if not enemy.is_dead:
                    enemy.take_damage(1)

    def _handle_player_enemy_collisions(self, dt):
        collisions = pygame.sprite.spritecollide(
            self.player,
            self.enemy_group,
            False,
            pygame.sprite.collide_circle
        )

        for enemy in collisions:
            if not enemy.is_dead:
                self.player.take_damage(30 * dt)