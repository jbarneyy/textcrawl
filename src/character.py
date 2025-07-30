from item import Item

class Character():

    def __init__(self, name: str, health: int, mana: int | None, equipment: list[Item] | None, items: list[Item] | None, quests: list | None, level: int):
        self.name = name
        self.health = health
        self.mana = mana
        self.equipment = equipment
        self.items = items
        self.quests = quests
        self.level = level


    def to_string(self):
        return f"{self.name} has Health: {self.health}, Mana: {self.mana}, Items: {", ".join(map(Item.to_string, self.items))}, Level: {self.level}"