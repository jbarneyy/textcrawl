from item import Item
from poi import POI

import random

class Enemy():

    def __init__(self, name: str, health: int, defence: int, items: list[Item] | None, level: int, current_POI: POI):
        self.name = name
        self.health = health
        self.defence = defence
        self.items = items
        self.level = level
        self.current_POI = current_POI

        self.xp_reward = health

    def to_string(self):
        return f"Name: {self.name}, Health: {self.health}, Defence: {self.defence}, Level: {self.level}, Current POI: {self.current_POI.name}"
    
    def roll_attack(self):
        base_damage = (self.level * 5)
        return random.randint(base_damage, base_damage + 5)