from character import Character
from item import Item, ItemType
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
    

    def list_items(self):
        """List Player's current items / inventory and equipment.

        Args:
            None: No arguments needed, return the Player's inventory with some formatting.

        Returns:
            String: A string representation of the character's inventory and equipment.
        """

        if self.items is None:
            return f"{self.name} does not have any items."
        
        items_string = f"{self.name}'s Inventory:\n"

        for item in self.items:
            items_string += f"- {item.to_string()}\n"

        return f"{self.name}: Level - {self.level} / Health - {self.health} / Location - {self.current_POI.name}\n\n{self.name}'s Equipment:\n- {self.armor.to_string()}\n- {self.weapon.to_string()}\n\n" + items_string.rstrip("\n")
    
    
    def equip_item(self, item_name: str) -> bool:
        """Equip an item from the player's inventory into either player's armor var or player's weapon var. Item must be in inventory and of ItemType.WEAPON or ItemType.ARMOR.
        If an item is already equipped, it will move the current equip into player's inventory.

        Args:
            item_name: String representing the name of the item that player is attempting to equip.

        Returns:
            True if item is successfully equipped to player.armor or player.weapon. False if equip is unsuccessful.
        """

        potential_equip = None

        for item in self.items:
            if (item_name.lower() == item.name.lower() and (item.type is ItemType.WEAPON or ItemType.ARMOR)):
                potential_equip = item
        
        if (potential_equip is None):
            return False
        
        if (potential_equip.type is ItemType.WEAPON):
            if (self.weapon is None):
                self.weapon = potential_equip
                self.items.remove(potential_equip)
            else:
                self.items.append(self.weapon)
                self.weapon = potential_equip
                self.items.remove(potential_equip)
            return True
        
        elif (potential_equip.type is ItemType.ARMOR):
            if (self.armor is None):
                self.armor = potential_equip
                self.items.remove(potential_equip)
            else:
                self.items.append(self.armor)
                self.armor = potential_equip
                self.items.remove(potential_equip)
            return True

    def roll_attack(self):
        return (self.level * 2) + self.weapon.power