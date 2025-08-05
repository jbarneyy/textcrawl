"""
Used to initialize all game variables. (Items / POIs / Characters / Enemies / Zone)
"""
import random

from item import Item, ItemType
from poi import POI
from character import Character
from zone import Zone


def populate_random_items(*lists: list[Item]):
    random_items = []

    for item_list in lists:
        random_items.append(random.choice(item_list))

    return random_items


# Initialize Weapons #
IRON_SWORD = Item("Iron Sword", ItemType.WEAPON, 5, "A simple iron sword, seems rusty.", True)
IRON_DAGGER = Item("Iron Dagger", ItemType.WEAPON, 4, "A simple iron dagger, small and sharp.", True)
IRON_HATCHET = Item("Iron Hatchet", ItemType.WEAPON, 4, "A simple iron hatchet.", True)

# Initalize Armor #

# Initalize Consumables #
SMALL_HP = Item("Small Health Potion", ItemType.CONSUMABLE, 10, "A small health potion, used to restore HP.", True)
SMALL_MP = Item("Small Mana Potion", ItemType.CONSUMABLE, 10, "A small mana potion, used to restore mana.", True)

# Initialize Quests #

# Initialize Misc #
SMALL_FISH = Item("Small Fish", ItemType.MISC, None, "A small fish.", True)
SMALL_STONE = Item("Small Stone", ItemType.MISC, None, "A little stone.", False)


# Group types of items together to be used in POI generation for randomness. #
IRON_WEAPONS = [IRON_SWORD, IRON_DAGGER, IRON_HATCHET]
SMALL_CONSUMABLES = [SMALL_HP, SMALL_MP]
MISC = [SMALL_FISH, SMALL_STONE]



# Initialize POIs #
LAKEFRONT = POI("Lakefront",
                "You are under the swaying branches of a gnarled willow tree, its long silver leaves dancing in the breeze like whispers of ancient secrets. " \
                "You can see the Lake of Thoughts before you.",
                (0, 0),
                populate_random_items(IRON_WEAPONS, SMALL_CONSUMABLES, MISC))



# Initialize Zones #
LAKE_OF_THOUGHTS = Zone("Lake of Thoughts",
            [LAKEFRONT],
            "The Lake of Thoughts stretches before you, its surface unnaturally still — a mirror reflecting a sky streaked with lavender clouds and twin suns low on the horizon." \
            "There is a firm breeze in the air, yet the water remains undisturbed. The scent of wet earth and touch of cool air envelops our adventurer." \
            "This is where our adventure begins.")