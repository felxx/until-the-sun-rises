class CollisionManager:
    def __init__(self, player, enemies, bullets):
        self.player = player
        self.enemies = enemies
        self.bullets = bullets

    def update(self):
        self._handle_bullet_enemy_collisions()
        self._handle_player_enemy_collisions()

    def _handle_bullet_enemy_collisions(self):
        for bullet in self.bullets[:]:
            for enemy in self.enemies[:]:
                distance = bullet.position.distance_to(enemy.position)

                if distance < (bullet.radius + enemy.radius):
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                    if enemy in self.enemies:
                        self.enemies.remove(enemy)
                    break

    def _handle_player_enemy_collisions(self):
        for enemy in self.enemies:
            distance = self.player.position.distance_to(enemy.position)
            if distance < (self.player.radius + enemy.radius):
                # self.player.take_damage(0.1)
                pass