from character import Character
from item import Item, ItemType
from poi import POI
from zone import Zone
from quest import Quest

import random


class Player(Character):

    def __init__(self, name: str, health: int, items: list[Item] | None, armor: Item | None, weapon: Item | None, quests: list[Quest] | None, level: int, current_POI: POI, current_zone: Zone, coins: int, description: str):
        super().__init__(name, health, items, quests, level, current_POI, current_zone, coins, description)

        self.armor = armor
        self.weapon = weapon

        self.current_xp: int = 0
        self.next_level_xp: int = self.level * 20


    def to_string(self):
        return f"Player: {self.name}, Health: {self.health}, Level: {self.level}, Experience: {self.current_xp}/{self.next_level_xp}, Equipped Armor: {self.armor.to_string()}, Equipped Weapon: {self.weapon.to_string()}, \
                Items: {", ".join(map(Item.to_string, self.items))}, Current Location: {self.current_POI.name}, Coins/Gold: {self.coins}, Quests: {", ".join(quest.to_string() for quest in self.quests if not quest.is_complete)}"
    

    def list_items(self):
        """List Player's current items / inventory / equipment / quests / stats.

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

        quests_string = f"{self.name}'s Quests:\n"

        for quest in self.quests:
            quests_string += f"- {quest.to_string()}\n"

        return (f"{self.name}: Level - {self.level} / Health - {self.health} / Location - {self.current_POI.name} / Gold - {self.coins}\n\n{self.name}'s Equipment:\n- {self.armor.to_string()}\n- {self.weapon.to_string()}\n\n"
                + items_string.rstrip("\n") + "\n\n" + quests_string.rstrip("\n"))
    
    
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
        base_damage = (self.level * 2) + self.weapon.power
        return random.randint(base_damage, base_damage + 10)
    

    def gain_xp(self, xp_amount: int) -> bool:
        """Gain experience for Player after defeating an Enemy. Player will currently gain XP based on the amount of Enemy's max/starting health.
        If Player.current_xp is greater than or equal to next_level_xp, increase Player level by 1, set current_xp to 0, add 20 to next_level_xp.

        Args:
            xp_amount: An int representing the amount of xp Player will gain.
        
        Returns:
            True if Player levels up, False if Player does not level up and only gained XP.
        """
        self.current_xp += xp_amount

        if (self.current_xp >= self.next_level_xp):
            self.level += 1
            self.current_xp = 0
            self.next_level_xp += 20

            return True
        
        return False
    

    def use_item(self, item: Item) -> str:

        if (item not in self.items):
            return f"You do not have {item.name} in your inventory."
        
        match item.type:
            case ItemType.WEAPON:
                responses = [f"You test the weight of your {item.name}, well balanced.",
                             f"The weapon feels balanced in your grip, though the hilt is slick with old sweat.",
                             f"You jab at an invisible foe.",
                             f"A sharp vibration runs up the handle, numbing your fingers.",
                             f"You heft the weapon and take a careful practice slash."]
                
                return random.choice(responses)
            
            case ItemType.ARMOR:
                return f"You examine the armor, it appears ready for combat!"
            
            case ItemType.CONSUMABLE:
                responses = [f"You examine the {item.name} and furiously consume it.",
                             f"A cool sensation flows through your veins.",
                             f"You use {item.name}, a faint glow surrounds you.",
                             f"*Glugs vigorously*",
                             f"You feel strength return to your bones."]

                self.health += item.power
                if (self.health > 100): self.health = 100

                self.items.remove(item)

                return random.choice(responses) + f"\n{item.name} restores {item.power} health."
            
            case ItemType.QUEST:
                responses = [f"You hold {item.name} aloft. Nothing happens... yet.",
                             f"{item.name} trembles slightly in your hand, as if waiting for a proper place or moment.",
                             f"You observe {item.name}. Perhaps its purpose will reveal itself in time.",
                             f"{item.name} glows faintly but remains inert."]
                
                return random.choice(responses)
            
            case ItemType.MISC:
                responses = [f"You fiddle with {item.name} for a while. It does not do much. Maybe you could sell it.",
                             f"{item.name} rests in your hand. Nothing magical happens.",
                             f"You give {item.name} a gentle shake.",
                             f"{item.name} wobbles, then stops—almost like it wanted to dance.",
                             f"For a brief moment, {item.name} warms in your hand... or was that just your imagination?",
                             f"Nothing happens. Absolutely nothing. {item.name} seems smug about it.",
                             f"{item.name} remains perfectly ordinary, despite your best efforts."]
                
                return random.choice(responses)
                

    