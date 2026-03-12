import pygame
from src.entities.dynamic_object import DynamicObject
from src.core.sprite_sheet_manager import SpriteSheetManager


class PlayerObject(DynamicObject):
    def __init__(self, x, y, speed, color, radius=15):
        super().__init__(x, y, speed, color, radius)

        self.animations = {
            "north": SpriteSheetManager.get_frames("assets/SMS_Soldier_WALK_NORTH_strip4.png"),
            "south": SpriteSheetManager.get_frames("assets/SMS_Soldier_WALK_SOUTH_strip4.png"),
            "east":  SpriteSheetManager.get_frames("assets/SMS_Soldier_WALK_EAST_strip4.png"),
            "west":  SpriteSheetManager.get_frames("assets/SMS_Soldier_WALK_WEST_strip4.png"),
        }

        self.direction = "south"
        self.frame_index = 0
        self.image = self.animations[self.direction][0]
        self.rect = self.image.get_rect(center=(x, y))

    def resolve_behavior(self, dt):
        keys = pygame.key.get_pressed()
        self.velocity.x = keys[pygame.K_d] - keys[pygame.K_a]
        self.velocity.y = keys[pygame.K_s] - keys[pygame.K_w]

    def update(self, dt):
        super().update(dt)
        self.rect.center = self.position
        self.animate(dt)

    def animate(self, dt):
        if self.velocity.length() > 0:
            self.frame_index = (self.frame_index + 10 * dt) % 4
            self.image = self.animations[self.direction][int(self.frame_index)]