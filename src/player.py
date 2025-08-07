from character import Character
from item import Item
from poi import POI
from zone import Zone

class Player(Character):

    def __init__(self, name: str, health: int, items: list[Item] | None, armor: Item | None, weapon: Item | None, quests: list | None, level: int, current_POI: POI, current_zone: Zone):
        super().__init__(name, health, items, quests, level, current_POI, current_zone)

        self.armor = armor
        self.weapon = weapon

    def to_string(self):
        return f"Player: {self.name}, Health: {self.health}, Level: {self.level}, Equipped Armor: {self.armor.to_string()}, Equipped Weapon: {self.weapon.to_string()}, \
                Items: {", ".join(map(Item.to_string, self.items))}, Current Location: {self.current_POI.name}"
    