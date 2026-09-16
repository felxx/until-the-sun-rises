from src.entities.consumable_object import ConsumableObject
from src.core.resource_manager import ResourceManager
import pygame

class MedicalKit(ConsumableObject):
    def __init__(self, position, heal_amount=25):
        super().__init__(position, hitbox_size=(14, 14))
        self.heal_amount = heal_amount
        self.sprite.image = ResourceManager.get_image("assets/images/item/medical_kit.png", 8)
        self.sprite.rect = self.sprite.image.get_rect(center=self.position)

    def apply_effect(self, player):
        player.heal(self.heal_amount)

    def render(self, dt):
        pass