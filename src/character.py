from item import Item
from poi import POI

class Character():

    def __init__(self, name: str, health: int, mana: int | None, equipment: list[Item] | None, items: list[Item] | None, quests: list | None, level: int, current_POI: POI):
        self.name = name

        self.health = health
        self.mana = mana

        self.equipment = equipment
        self.items = items
        self.quests = quests

        self.level = level
        self.current_POI = current_POI


    def to_string(self):
        return f"{self.name} has Health: {self.health}, Mana: {self.mana}, Level: {self.level}, Items: {", ".join(map(Item.to_string, self.items))}"