import pygame
from src.entities.dynamic_object import DynamicObject


class XPObject(DynamicObject):
    def __init__(self, position, player, xp_value=10):
        super().__init__(position, speed=100, hitbox_size=(4, 4))
        self.player = player
        self.xp_value = xp_value
        self.magnet_radius = 30
        self._layer = 1

        self._xp_surface = pygame.Surface((4, 4), pygame.SRCALPHA)
        pygame.draw.circle(self._xp_surface, (0, 255, 255), (2, 2), 2)
        pygame.draw.circle(self._xp_surface, (255, 255, 255), (2, 2), 1)

    def resolve_behavior(self, dt):
        if self.player and self.player.is_alive:
            direction = self.player.position - self.position
            distance = direction.length()

            if distance < self.magnet_radius and distance > 0:
                self.velocity = direction
            else:
                self.velocity = pygame.math.Vector2(0, 0)
        else:
            self.velocity = pygame.math.Vector2(0, 0)

    def update(self, dt, world_mouse=None):
        super().update(dt, world_mouse)

    def render(self, dt):
        return self._xp_surface