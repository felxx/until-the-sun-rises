from src.entities.consumable_object import ConsumableObject
from src.core.resource_manager import ResourceManager
import pygame

class EnergyDrink(ConsumableObject):
    def __init__(self, position, speed_boost=50, duration=5.0):
        super().__init__(position, hitbox_size=(12, 12))
        self.speed_boost = speed_boost
        self.duration = duration
        self.sprite.image = ResourceManager.get_image("assets/images/item/energy_coke.png", 8)
        self.sprite.rect = self.sprite.image.get_rect(center=self.position)

    def apply_effect(self, player):
        if "speed_boost" not in player.active_buffs:
            player.speed += self.speed_boost

        player.active_buffs["speed_boost"] = self.duration

    def render(self, dt):
        pass