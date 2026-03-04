import pygame
from src.entities.dynamic_object import DynamicObject


class PlayerObject(DynamicObject):
    def __init__(self, x, y, speed, color, radius=15):
        super().__init__(x, y, speed, color, radius)

        self.animations = {
            "north": self.load_strip("assets/SMS_Soldier_WALK_NORTH_strip4.png"),
            "south": self.load_strip("assets/SMS_Soldier_WALK_SOUTH_strip4.png"),
            "east":  self.load_strip("assets/SMS_Soldier_WALK_EAST_strip4.png"),
            "west":  self.load_strip("assets/SMS_Soldier_WALK_WEST_strip4.png"),
        }

        self.direction = "south"
        self.frame_index = 0
        self.image = self.animations[self.direction][self.frame_index]
        self.rect = self.image.get_rect(center=(x, y))

    def load_strip(self, path):
        full_sheet = pygame.image.load(path).convert_alpha()
        full_sheet = pygame.transform.scale(
            full_sheet, (full_sheet.get_width() * 3, full_sheet.get_height() * 3))
        w = full_sheet.get_width() // 4
        h = full_sheet.get_height()
        return [full_sheet.subsurface(pygame.Rect(i*w, 0, w, h)) for i in range(4)]

    def resolve_behavior(self, dt):
        keys = pygame.key.get_pressed()
        self.velocity.x = keys[pygame.K_d] - keys[pygame.K_a]
        self.velocity.y = keys[pygame.K_s] - keys[pygame.K_w]

    def update(self, dt):
        super().update(dt)
        self.rect.center = self.position

        if self.velocity.length() > 0:
            if abs(self.velocity.x) > abs(self.velocity.y):
                self.direction = "east" if self.velocity.x > 0 else "west"
            else:
                self.direction = "south" if self.velocity.y > 0 else "north"

            self.frame_index += 10 * dt
            if self.frame_index >= 4:
                self.frame_index = 0
        else:
            self.frame_index = 0

        self.image = self.animations[self.direction][int(self.frame_index)]

    def draw(self, screen):
        screen.blit(self.image, self.rect)
