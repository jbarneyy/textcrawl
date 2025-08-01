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
    

    def grab_item(self, grab: str):
        """Grab an item from the player/character's current POI and place it into character's inventory, if item can_pickup is true. Deletes the item from POI's list of Items.

        Args:
            grab: String representing the Item.name of the item player attempts to grab.

        Returns:
            None. Item is appended to Character.items and removed from POI.items.
        """

        for item in self.current_POI.items:
            if (grab.lower() == item.name.lower() and item.can_pickup):
                self.items.append(item)
                self.current_POI.items.remove(item)
                return