from abc import ABC, abstractmethod
import pygame

from src.entities.dynamic_object import DynamicObject


class CharacterObject(DynamicObject, ABC):
    def __init__(self, position, speed, max_health, damage, hitbox_size=(12, 12), combat_radius=15):
        super().__init__(position, speed, hitbox_size, combat_radius)

        self.max_health = max_health
        self.current_health = max_health
        self.damage = damage
        self.is_alive = True
        self.damage_flash_timer = 0

    def take_damage(self, amount):
        if self.is_alive:
            self.current_health = max(0, self.current_health - amount)
            self.damage_flash_timer = 0.1
            if self.current_health <= 0:
                self.is_alive = False
                self.die()

    def heal(self, amount):
        """Método utilitário para restaurar vida sem ultrapassar max_health"""
        if self.is_alive:
            self.current_health = min(self.max_health, self.current_health + amount)

    @abstractmethod
    def die(self):
        pass

    def update(self, dt, world_mouse=None):
        super().update(dt, world_mouse)

        if self.damage_flash_timer > 0:
            self.damage_flash_timer -= dt