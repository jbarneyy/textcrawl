from item import Item
from poi import POI
from zone import Zone
from quest import Quest


class Character():

    def __init__(self, name: str, health: int, items: list[Item] | None, quests: list[Quest] | None, level: int, current_POI: POI, current_zone: Zone, coins: int, description: str):
        self.name = name

        self.health = health

        self.items = items
        self.quests = quests

        self.level = level
        
        self.current_POI = current_POI
        self.current_zone = current_zone

        self.coins = coins
        self.description = description


    def to_string(self):
        return f"Character: {self.name}, Health: {self.health}, Level: {self.level}, Items: {", ".join(map(Item.to_string, self.items))}, Current Location: {self.current_POI.name}, Coins/Gold: {self.coins}, Quests: {self.quests[0].name if self.quests else "None"}, Description: {self.description}"
    

    def grab_item(self, item: Item):
        """Grab an item from the player/character's current POI and place it into character's inventory, if item can_pickup is true. Deletes the item from POI's list of Items.

        Args:
            grab: String representing the Item.name of the item player attempts to grab.

        Returns:
            True if item is picked up, False if item is not picked up. Item is appended to Character.items and removed from POI.items if True.
        """

        if item in self.current_POI.items and item.can_pickup is True:
            self.items.append(item)
            self.current_POI.items.remove(item)
            return True
        
        return False
    

    def list_items(self):
        """List character's current items / inventory.

        Args:
            None: No arguments needed, return the character's inventory with some formatting.

        Returns:
            String: A string representation of the character's inventory.
        """

        if self.items is None:
            return f"{self.name} does not have any items."
        
        items_string = f"{self.name}'s Inventory:\n"

        for item in self.items:
            items_string += f"- {item.to_string()}\n"

        return items_string.rstrip("\n")
    

    def move(self, target_location: POI):
        """Move character from current POI to target_location POI.

        Args:
            target_location: POI object representing the target POI character is attempting to move to.

        Returns:
            Bool: True if character is able to move from current POI to target_location POI (target_location.is_open and distance is less than arbitrary value).
        """

        if (target_location.is_open is True):
            self.current_POI = target_location
            return True
        else:
            return False
        

    def get_item(self, item_name: str | None) -> Item:
        item_names = list(map(lambda x: x.name, self.items))
        item = None
        
        if item_name in item_names:
            for items in self.items:
                if item_name.lower() == items.name.lower():
                    item = items

        return item
