"""
Used to initialize all game variables. (Items / POIs / Characters / Enemies / Zone)
"""
import random

from item import Item, ItemType
from poi import POI
from character import Character
from zone import Zone
from enemy import Enemy
from quest import Quest
from gamestate import GameState
from player import Player


def populate_random_items(*lists: list[Item]):
    random_items = []

    for item_list in lists:
        random_items.append(random.choice(item_list))

    return random_items

# Initialize Quest Completion Callables #
def visited_misty_tankard(player: Player, gamestate: GameState) -> bool:
    return player.current_POI is gamestate.pois.get("The Misty Tankard")

def return_harkens_pole(player: Player, gamestate: GameState) -> bool:
    return player.current_POI is gamestate.pois.get("The Misty Tankard") and gamestate.items.get("Harken's Pole") in gamestate.characters.get("Harken Bristle").items

def return_rat_tooth(player: Player, gamestate: GameState) -> bool:
    return player.current_POI is gamestate.pois.get("The Misty Tankard") and gamestate.items.get("Rat Tooth") in gamestate.characters.get("Sylvara Reedwhistle").items

# Initialize Item Weapons #
IRON_SWORD = Item("Iron Sword", ItemType.WEAPON, 5, "A simple iron sword, seems rusty.", True)
IRON_DAGGER = Item("Iron Dagger", ItemType.WEAPON, 4, "A simple iron dagger, small and sharp.", True)
IRON_HATCHET = Item("Iron Hatchet", ItemType.WEAPON, 4, "A simple iron hatchet.", True)

# Initalize Item Armors #
LEATHER_ARMOR = Item("Leather Armor", ItemType.ARMOR, 5, "Basic leather armor, smells like shit.", True)
IRON_ARMOR = Item("Iron Armor", ItemType.ARMOR, 10, "Iron armor, seems better than leather.", True)

# Initalize Item Consumables #
SMALL_HP = Item("Small Health Potion", ItemType.CONSUMABLE, 10, "A small health potion, used to restore HP.", True)
SMALL_MP = Item("Small Mana Potion", ItemType.CONSUMABLE, 10, "A small mana potion, used to restore mana.", True)

# Initialize Item Misc #
SMALL_FISH = Item("Small Fish", ItemType.MISC, None, "A small fish.", True)
SMALL_STONE = Item("Small Stone", ItemType.MISC, None, "A little stone.", False)

# Initialize Item Quest #
HARKENS_POLE = Item("Harken's Pole", ItemType.QUEST, None, "Harken's old fishing pole.", True, 0)
RAT_TOOTH = Item("Rat Tooth", ItemType.QUEST, None, "A crusty and bloody rat tooth.", True)

# Initialize Quests #
QUEST_MISTY_TANKARD = Quest("Visit Misty Tankard", "Travel to The Misty Tankard.", "Seek out The Misty Tankard.", visited_misty_tankard, False, 10)
QUEST_HARKENS_POLE = Quest("Harken's Fishing Pole", "Return Harken's fishing pole to him.", "Harken looks to you with his eyes of stubborn resolve. " \
"He asks that you help him return his prized fishing rod, last seen down at the Lakefront. He was chased away by a Giant Rat while fishing there last.", return_harkens_pole, False, 50)
QUEST_RAT_TOOTH = Quest("Return Rat Tooth", "Return the Giant Rat's tooth to Sylvara.", "Sylvara's emerald eyes look at you with hope. Please kill that foul rat seen in the Lakefront and bring me confirmation that the deed is done.",
                        return_rat_tooth, False, 50)


# Group types of items together to be used in POI generation for randomness. #
IRON_WEAPONS = [IRON_SWORD, IRON_DAGGER, IRON_HATCHET]
SMALL_CONSUMABLES = [SMALL_HP, SMALL_MP]
MISC = [SMALL_FISH, SMALL_STONE]



# Initialize POIs #
LAKEFRONT = POI("Singing Lake",
                ("A vast, glassy lake that hums like a choir when moonlight touches its surface. Crystalline fish leap from the water trailing stardust. "
                "The Singing Lake lies in a secluded hollow of Everdusk Vale, cradled by crystal-studded cliffs and veiled in soft silver mist. "
                "Its waters are perfectly still except during the moon's zenith, when ripples form delicate concentric rings without wind. "
                "At night, moonlight refracts through the floating Dayheart shards suspended above, causing the lake to hum in layered harmonies—tones so pure they vibrate through bone and memory. "
                "Ancient moonwillow trees grow along the shore, their leaves chiming like soft bells when brushed by the lake's vibrations."),
                (0, 0),
                populate_random_items(IRON_WEAPONS, MISC, MISC, MISC) + [HARKENS_POLE],
                True)

MISTY_TANKARD = POI("The Misty Tankard",
                    ("Nestled at the edge of the shimmering Lake of Thoughts, The Misty Tankard is a small, weathered tavern with moss-covered shingles and warm amber light spilling from its foggy windows. "
                    "The wooden sign creaks gently in the breeze, etched with the image of a frothy mug and a drifting wisp of mist. "
                    "As adventurers step inside, they're greeted by the scent of oak smoke, salted fish, and a faint trace of lavender that seems to linger in the beams. "
                    "A low murmur of conversation, the clink of mugs, and the occasional distant loon call mix in the background. "
                    "Shelves behind the bar are stocked with strange colored bottles, local brews, and curious herbal infusions. "
                    "The tavern is warm and welcoming, its walls lined with faded maps, old fishing rods, and a massive mounted trout with one missing eye."),
                    (2, 2),
                    populate_random_items(SMALL_CONSUMABLES, SMALL_CONSUMABLES, SMALL_CONSUMABLES) + [IRON_ARMOR],
                    True)

BLEAKTHORN = POI("Bleakthorn Woods",
                 ("An endless forest of silver-barked trees that bleed glowing blue sap. The canopy is so thick it feels like walking through a dream."),
                 (5, 2),
                 [SMALL_STONE],
                 True)


# Initialize Zones #
EVERDUSK_VALE = Zone("Everdusk Vale",
            [LAKEFRONT, MISTY_TANKARD, BLEAKTHORN],
            description=("Everdusk Vale is a land bathed in perpetual twilight, an indigo sky streaked with slow-moving auroras. "
            "Vast crystal spires float like lazy comets above the landscape, shedding shimmering aether dust that fuels both wonder and danger. "
            "Gravity feels slightly lighter; magic hums beneath every stone. 10,000 years ago it was a sunlit kingdom ruled by the Celestine Dynasty, a council of archmages who mastered Solar Magic. "
            "Legends tell of the Dayheart, a colossal crystal at the world's core that regulated sunlight and moonlight in perfect balance. Then 3,000 years ago The Moonfall took place - "
            "a catastrophic ritual meant to draw more lunar energy for magical research went awry. The Dayheart shattered, plunging Everdusk into permanent twilight. "
            "Fragments of the Dayheart scattered across the land, becoming the floating crystals that still orbit the vale. The Celestine vanished—some say ascended to the moon, others claim they fused with the crystals themselves. "
            "Now in current day we enter the Age of Aether. Magic is abundant but unstable; reality itself bends in places. Factions vie to control the largest Dayheart shards, believing they can either restore the sun or unleash godlike power."))


# Initialize Characters #
HARKEN_BRISTLE = Character("Harken Bristle", 100, [SMALL_HP, SMALL_MP], [QUEST_HARKENS_POLE], 1, MISTY_TANKARD, EVERDUSK_VALE, 10,
                           description="""A grizzled, broad-shouldered dwarf with a beard like twisted iron and eyes that gleam with stubborn resolve. 
                           Once a master blacksmith of the Emberdeep Forges, he now runs the Misty Tankard tavern as both a barkeep 
                           and quiet keeper of local secrets. Harken speaks in a gravelly baritone, every word weighed like 
                           a hammer strike, and carries the scent of smoke and oiled steel wherever he goes. 
                           Though age has silvered the edges of his hair, his arms still bear the strength of 
                           decades at the anvil, and his sharp wit makes him as quick with a clever retort as he once was 
                           with a forge hammer. Rumor has it Harken keeps a hidden cache of rare ores beneath the tavern 
                           floor—and a past filled with debts, alliances, and old grudges.
                            """)

SYLVARA = Character("Sylvara Reedwhistle", 100, [SMALL_HP], [QUEST_RAT_TOOTH], 1, MISTY_TANKARD, EVERDUSK_VALE, 10,
                    description="""A quick-witted half-elf bard with emerald eyes and a voice that can hush a rowdy tavern mid-brawl.
                    Sylvara wears a patchwork cloak of deep forest greens and dusky blues, each swatch telling a story of a place she has wandered.
                    She strums a weathered lute strung with silver-thread strings and always keeps a dagger hidden in her boot—“just in case the song does not work.”
                    Patrons say she trades tales for drinks, and her songs often contain veiled warnings or riddles about dangers lurking beyond the lake.
                    Rumor has it she is searching for a long-lost lover… or perhaps a priceless artifact she won in a wager and foolishly lost.
                    """)

# Initialize Enemies #
GIANT_RAT = Enemy("Giant Rat", 20, 1, [RAT_TOOTH], 1, LAKEFRONT)
