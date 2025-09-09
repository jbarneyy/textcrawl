from enum import Enum

class ItemType(Enum):
    WEAPON = "Weapon"
    ARMOR = "Armor"
    CONSUMABLE = "Consumable"
    QUEST = "Quest"
    MISC = "Misc"

class Item():

    def __init__(self, name: str, type: ItemType, power: int | None, description: str, can_pickup: bool = False, value: int = 0):
        self.name = name
        self.type = type
        self.power = power
        self.description = description
        self.can_pickup = can_pickup
        self.value = value

    def to_string(self):
        return f"Name: {self.name} - Type: {self.type.value} - Power: {self.power} - Description: {self.description} - Value: {self.value} gold"
    
    def use_item(self):

        match self.type:
            case ItemType.WEAPON:
                return f"I attack with {self.name}, it deals {self.power} damage."
            
            case ItemType.ARMOR:
                return f"I am wearing {self.name}, it reduces damage by {self.power}."
            
            case ItemType.CONSUMABLE:
                return f"I consume {self.name}, it restores {self.power} health."
            
            case ItemType.QUEST:
                return f"I observe {self.name}, it tells me {self.description}."
            
            case ItemType.MISC:
                return f"I observe {self.name}, it doesn't do much."
            
            case _:
                return f"What is this thing?"

