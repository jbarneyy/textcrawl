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

def collect_bark_map(player: Player, gamestate: GameState) -> bool:
    if player.current_POI is gamestate.pois.get("Bleakthorn Woods") and gamestate.items.get("Bark Map") in player.items:
        gamestate.pois.get("Moonveil Citadel").is_open = True
        return True
    else:
        return False
    
def return_runed_sword(player: Player, gamestate: GameState) -> bool:
    if (player.current_POI is gamestate.pois.get("Moonveil Citadel") and gamestate.items.get("Runed Sword Top Shard") in gamestate.characters.get("Dorian Krail").items and
        gamestate.items.get("Runed Sword Bottom Shard") in gamestate.characters.get("Dorian Krail").items):
        player.items.append(gamestate.items.get("Runed Steel Sword"))
        return True
    else:
        return False
    


# Initialize Item Weapons #
IRON_SWORD = Item("Iron Sword", ItemType.WEAPON, 5, "A simple iron sword, seems rusty.", True, 5)
IRON_DAGGER = Item("Iron Dagger", ItemType.WEAPON, 4, "A simple iron dagger, small and sharp.", True, 5)
IRON_HATCHET = Item("Iron Hatchet", ItemType.WEAPON, 4, "A simple iron hatchet.", True, 5)

STEEL_DAGGER = Item("Steel Dagger", ItemType.WEAPON, 7, "Looks more potent than iron.", True, 17)
STEEL_SWORD = Item("Steel Sword", ItemType.WEAPON, 9, "Tempered iron with carbon; sharper and more durable than iron.", True, 20)
STEEL_WARHAMMER = Item("Steel Warhammer", ItemType.WEAPON, 9, "Tempered iron with carbon; in the shape of a hammer.", True, 25)

RUNED_STEEL_SWORD = Item("Runed Steel Sword", ItemType.WEAPON, 25, "Steel blade etched with runes, they shimmer with potential.", True, 40)

# Initalize Item Armors #
LEATHER_ARMOR = Item("Leather Armor", ItemType.ARMOR, 5, "Basic leather armor, smells like shit.", True, 5)
IRON_ARMOR = Item("Iron Armor", ItemType.ARMOR, 10, "Iron armor, seems better than leather.", True, 15)
STEEL_ARMOR = Item("Steel Armor", ItemType.ARMOR, 20, "Steel-hardened battle armor, seems effective.", True, 30)

# Initalize Item Consumables #
SMALL_HP = Item("Small Health Potion", ItemType.CONSUMABLE, 10, "A small health potion, used to restore HP.", True, 5)
MEDIUM_HP = Item("Medium Health Potion", ItemType.CONSUMABLE, 25, "A medium health potion, used to restore HP.", True, 10)

# Initialize Item Misc #
SMALL_FISH = Item("Small Fish", ItemType.MISC, None, "A small fish.", True, 2)
SMALL_STONE = Item("Small Stone", ItemType.MISC, None, "A little stone.", True, 1)
OLD_MAP = Item("Old Map", ItemType.MISC, None, "An old crusty map, can't even tell where North is.", True, 10)
SATCHEL = Item("Traveler's Satchel", ItemType.MISC, None, "Well-worn leather bag with faint scorch marks from campfires.", True, 5)
WATERFLASK = Item("Tin Waterflask", ItemType.MISC, None, "Dented and cold to the touch, no matter the weather.", True, 5)
JUNIPER = Item("Bundle of Juniper", ItemType.MISC, None, "Used for fire-starting or mild seasoning in stews.", True, 8)
ROPE = Item("Rope Coil", ItemType.MISC, None, "Frayed at the ends, smells faintly of salt and pine.", True, 8)
LANTERN = Item("Iron Lantern", ItemType.MISC, None, "Simple oil lamp with cracked glass patched by wire.", True, 8)
SPADE = Item("Rusty Spade", ItemType.MISC, None, "Blade worn thin from years of digging graves or gardens.", True, 6)
FLETCHING = Item("Fletching Kit", ItemType.MISC, None, "Pouch of feathers, arrowheads, and pitch glue.", True, 10)
KNIFE = Item("Pocket Knife", ItemType.MISC, None, "Folded steel blade with a chipped bone handle.", True, 10)
DICE = Item("Wooden Dice", ItemType.MISC, None, "Corners rounded from hundreds of tavern games.", True, 10)

# Initialize Item Quest #
HARKENS_POLE = Item("Harken's Pole", ItemType.QUEST, None, "Harken's old fishing pole.", True, 0)
RAT_TOOTH = Item("Rat Tooth", ItemType.QUEST, None, "A crusty and bloody rat tooth.", True, 0)
BARK_MAP = Item("Bark Map", ItemType.QUEST, None, "A map made of the ent's bark, showing a path to Moonveil Citadel.", True, 20)
RUNED_SWORD_TOP = Item("Runed Sword Top Shard", ItemType.QUEST, None, "Top shard of Dorian's runed steel sword.", True, 20)
RUNED_SWORD_BOT = Item("Runed Sword Bottom Shard", ItemType.QUEST, None, "Bottom shard of Dorian's runed steel sword.", True, 20)

# Initialize Quests #
QUEST_MISTY_TANKARD = Quest("Visit Misty Tankard", "Travel to The Misty Tankard.", "Seek out The Misty Tankard.", visited_misty_tankard, False, 10, "You find your way to the Misty Tankard. The first step in a long adventure.")

QUEST_HARKENS_POLE = Quest("Harken's Fishing Pole", "Return Harken's fishing pole to him.", "Harken looks to you with his eyes of stubborn resolve. " \
"He asks that you help him return his prized fishing rod, last seen down at the Lakefront. He was chased away by a Giant Rat while fishing there last.", return_harkens_pole, False, 50, 
"Harken gives you a stern nod of approval. 'Thank you lad, tonight's drinks are on me.'")

QUEST_RAT_TOOTH = Quest("Return Rat Tooth", "Return the Giant Rat's tooth to Sylvara.", "Sylvara's emerald eyes look at you with hope. Please kill that foul rat seen in the Lakefront and bring me confirmation that the deed is done.",
                        return_rat_tooth, False, 50, "You rid yourself of the stinky rat tooth. Wondering what Sylvara will use it for.")

QUEST_BARK_MAP = Quest("Collect Bark Map", "To unlock the path to Moonveil Citadel, collect a bark map from the back of one of the Blue Ents that roam Bleakthorn Woods.",
                       "Neric rises from listening to the ground, 'Collect a Bark Map from an ent to unlock the path to Moonveil, I would pay to know this path as well.' What an odd man.", collect_bark_map, False, 100,
                       "You see a pattern on the back of the bark map, showing a faint outline of the route to Moonveil Citadel.")

QUEST_RUNED_SWORD = Quest(name="Reforge Steel-Runed Sword", description="Bring Dorian back both pieces of his runed sword.", 
                          accept_message="Dorian looks at you with steeled eyes. 'Someone like you will need a better weapon to deal with what's out there.' Find the two runed shards in the Catacombs and return them.",
                          check_complete=return_runed_sword, is_complete=False, xp_reward=100, 
                          complete_message="Dorian breaths icy breath over the two shards and recombines them into a runed steel sword. He hands it to you gently as mist seeps off the blade.")



# Group types of items together to be used in POI generation for randomness. #
IRON_WEAPONS = [IRON_SWORD, IRON_DAGGER, IRON_HATCHET]
SMALL_CONSUMABLES = [SMALL_HP]
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
                    "A low murmur of conversation, the clink of mugs, and the occasional distant loon call mix in the background. There are many people sampling the bar's drink. "
                    "Shelves behind the bar are stocked with strange colored bottles, local brews, and curious herbal infusions. "
                    "The tavern is warm and welcoming, its walls lined with faded maps, old fishing rods, and a massive mounted trout with one missing eye."),
                    (2, 2),
                    populate_random_items(SMALL_CONSUMABLES, SMALL_CONSUMABLES, SMALL_CONSUMABLES) + [IRON_ARMOR],
                    True)

BLEAKTHORN = POI("Bleakthorn Woods",
                 ("An endless forest of silver-barked trees that bleed glowing blue sap. The canopy is so thick it feels like walking through a dream. "
                 "The forest canopy is so dense it blocks what little starlight Everdusk provides, creating a perpetual twilight haze even darker than the rest of the vale. "
                 "The air smells faintly of iron and crushed herbs, and every sound—rustling leaves, distant howls—seems to echo as though the forest itself is listening. "
                 "Once a sacred grove tended by Celestine moon-priests. After the Moonfall, the grove's protective wards shattered, allowing the woods to grow unchecked. "
                 "Ancient texts refer to it as The Choir of Roots, suggesting the forest once sang in harmony with the Singing Lake before the Dayheart shattered."),
                 (5, 2),
                 [STEEL_DAGGER, OLD_MAP, JUNIPER, SPADE],
                 True)

MOONVEIL = POI("Moonveil Citadel",
               ("A shimmering city built atop a ring of hovering platforms connected by glowing bridges. The citadel's spires are infused with moonstone that channels raw aether. "
               "Moonstone bridges span the empty air, glowing faintly as if lit from within. Thin waterfalls of luminous aether cascade from the floating structures into the mist below, "
               "creating a perpetual silver rain that reflects the indigo sky. Moonveil is both city and arcane engine, its architecture shaped by ancient Celestine magic. "
               "Gravity-defying bridges sway gently but never break. Some move like living things, subtly shifting routes based on lunar phases. "
               "Vertical hanging gardens of luminous moss and moonwillow trees provide air purification and soft light."),
               (7, 4),
               [DICE, KNIFE, FLETCHING, ROPE, ROPE, WATERFLASK],
               False)

MOONVEIL_CATACOMB = POI("Moonveil Catacombs",
                        ("The Moonveil Catacombs are an ancient necropolis carved into the bedrock directly below Moonveil Citadel. "
                        "Long before the Citadel's marble towers rose, this labyrinth served as a sacred burial ground for the first Celestine scholars and the founding Moonpriests. "
                        "Over centuries of lunar eclipses and aether storms, the magical wards that once sealed the tunnels fractured, allowing moon-charged aether to seep through the crypts and awaken restless spirits. "
                        "Narrow marble corridors engraved with lunar runes that pulse faint silver light. Water drips from the ceiling, forming pools that glow faintly under moonlight."),
                        (7, 6),
                        [LANTERN, OLD_MAP, OLD_MAP, SMALL_STONE, SMALL_STONE, SATCHEL, KNIFE],
                        True)




# Initialize Zones #
EVERDUSK_VALE = Zone("Everdusk Vale",
            [LAKEFRONT, MISTY_TANKARD, BLEAKTHORN, MOONVEIL],
            description=("Everdusk Vale is a land bathed in perpetual twilight, an indigo sky streaked with slow-moving auroras. "
            "Vast crystal spires float like lazy comets above the landscape, shedding shimmering aether dust that fuels both wonder and danger. "
            "Gravity feels slightly lighter; magic hums beneath every stone. 10,000 years ago it was a sunlit kingdom ruled by the Celestine Dynasty, a council of archmages who mastered Solar Magic. "
            "Legends tell of the Dayheart, a colossal crystal at the world's core that regulated sunlight and moonlight in perfect balance. Then 3,000 years ago The Moonfall took place - "
            "a catastrophic ritual meant to draw more lunar energy for magical research went awry. The Dayheart shattered, plunging Everdusk into permanent twilight. "
            "Fragments of the Dayheart scattered across the land, becoming the floating crystals that still orbit the vale. The Celestine vanished—some say ascended to the moon, others claim they fused with the crystals themselves. "
            "Now in current day we enter the Age of Aether. Magic is abundant but unstable; reality itself bends in places. Factions vie to control the largest Dayheart shards, believing they can either restore the sun or unleash godlike power."))


# Initialize Characters #
HARKEN_BRISTLE = Character("Harken Bristle", 100, [SMALL_HP, SMALL_HP], [QUEST_HARKENS_POLE], 1, MISTY_TANKARD, EVERDUSK_VALE, 10,
                           description="""A grizzled, broad-shouldered dwarf with a beard like twisted iron and eyes that gleam with stubborn resolve. 
                           Once a master blacksmith of the Emberdeep Forges, he now runs the Misty Tankard tavern as both a barkeep 
                           and quiet keeper of local secrets. Harken speaks in a gravelly baritone, every word weighed like 
                           a hammer strike, and carries the scent of smoke and oiled steel wherever he goes. 
                           Though age has silvered the edges of his hair, his arms still bear the strength of 
                           decades at the anvil, and his sharp wit makes him as quick with a clever retort as he once was 
                           with a forge hammer. Rumor has it Harken keeps a hidden cache of rare ores beneath the tavern 
                           floor—and a past filled with debts, alliances, and old grudges.
                            """)

SYLVARA = Character("Sylvara Reedwhistle", 100, [SMALL_HP, SMALL_HP], [QUEST_RAT_TOOTH], 1, MISTY_TANKARD, EVERDUSK_VALE, 10,
                    description="""A quick-witted half-elf bard with emerald eyes and a voice that can hush a rowdy tavern mid-brawl.
                    Sylvara wears a patchwork cloak of deep forest greens and dusky blues, each swatch telling a story of a place she has wandered.
                    She strums a weathered lute strung with silver-thread strings and always keeps a dagger hidden in her boot—“just in case the song does not work.”
                    Patrons say she trades tales for drinks, and her songs often contain veiled warnings or riddles about dangers lurking beyond the lake.
                    Rumor has it she is searching for a long-lost lover… or perhaps a priceless artifact she won in a wager and foolishly lost.
                    """)

NERIC = Character("Neric the Wayfarer", 100, [OLD_MAP, OLD_MAP, FLETCHING], [QUEST_BARK_MAP], 1, BLEAKTHORN, EVERDUSK_VALE, 10, 
                  ("A seasoned traveler and self-proclaimed cartomancer who roams Bleakthorn Woods mapping shifting paths and magical anomalies. "
                  "Neric sells living maps that redraw themselves nightly, but their accuracy depends on both the moon's phase and the buyer's own intentions. "
                  "Wears a patched longcoat lined with pockets that emit faint glows, each pocket storing a different magical compass or ink bottle. "
                  "Claims the paths whisper to him, often pausing mid-conversation to listen to the ground."))

SERAPHINE = Character(name="Seraphine Veyra", health=100, items=[MEDIUM_HP, MEDIUM_HP, MEDIUM_HP, JUNIPER], quests=None, level=1, current_POI=MOONVEIL, current_zone=EVERDUSK_VALE, coins=10, 
                      description=("A pale, silver-eyed elf who tends the Citadel's moonlit archives. Her robes shimmer like frost on crystal, and a faint smell of lavender follows her. "
                      "Soft-spoken but relentless in pursuit of lost knowledge. Speaks in careful, poetic sentences. "
                      "Has a commanding presence about herself, she seeks out individuals who share her passions."))

DORIAN = Character(name="Dorian Krail", health=100, items=[STEEL_WARHAMMER, STEEL_SWORD, STEEL_ARMOR], quests=[QUEST_RUNED_SWORD], level=1, current_POI=MOONVEIL, current_zone=EVERDUSK_VALE, coins=10,
                   description=("Warden of Moonveil Citadel's guard. A scarred human veteran clad in half-plate etched with lunar runes. His left gauntlet bears the sigil of the Citadel's royal guard. "
                   "Gruff, impatient, but fiercely honorable. Prefers action to words. "
                   "Has some good steel to trade for the right price. Dorian talks of a runed sword he lost in the Catacombs a few months back."))

MORWEN = Character(name="Morwen Lyric", health=100, items=[KNIFE, DICE, ROPE], quests=None, level=1, current_POI=MOONVEIL, current_zone=EVERDUSK_VALE, coins=10,
                   description=("An elderly half-orc priestess with luminous white hair and a silver bell-staff. She keeps the Citadel's ceremonial bells in perfect harmony. "
                   "She is warm and grandmotherly, but cryptic when speaking of omens. She tends to ring her bell-staff when she is preoccupied or nervous. "
                   "Morwen claims to know where the location of one of the Dayheart shards, but will need some help before revealing the location."))

# Initialize Enemies #
GIANT_RAT = Enemy("Giant Rat", 20, 1, [RAT_TOOTH], 1, LAKEFRONT)
LAKE_SNAKE = Enemy("Lake Snake", 25, 1, None, 2, LAKEFRONT)
BEAR = Enemy("Grizzled Bear", 30, 1, None, 2, LAKEFRONT)

BLUE_ENT = Enemy("Blue Ent", 50, 1, [BARK_MAP], 3, BLEAKTHORN)
RED_ENT = Enemy("Red Ent", 50, 1, None, 3, BLEAKTHORN)
GREEN_ENT = Enemy("Green Ent", 50, 1, None, 3, BLEAKTHORN)



# Initialize Lists to pass to GameState() in main.py #
ZONES = [EVERDUSK_VALE]

POIS = [LAKEFRONT, MISTY_TANKARD, BLEAKTHORN, MOONVEIL, MOONVEIL_CATACOMB]

CHARACTERS = [HARKEN_BRISTLE, SYLVARA, NERIC, SERAPHINE, DORIAN, MORWEN]

ENEMIES = [GIANT_RAT, LAKE_SNAKE, BEAR, BLUE_ENT, RED_ENT, GREEN_ENT]

ITEM_WEAPONS = [IRON_SWORD, IRON_DAGGER, IRON_HATCHET, STEEL_DAGGER, STEEL_SWORD, STEEL_WARHAMMER, RUNED_STEEL_SWORD]
ITEM_ARMORS = [LEATHER_ARMOR, IRON_ARMOR, STEEL_ARMOR]
ITEM_CONSUMABLES = [SMALL_HP, MEDIUM_HP]
ITEM_MISC = [SMALL_FISH, SMALL_STONE, OLD_MAP, SATCHEL, WATERFLASK, JUNIPER, ROPE, LANTERN, SPADE, FLETCHING, KNIFE, DICE]
ITEM_QUEST = [HARKENS_POLE, RAT_TOOTH, BARK_MAP, RUNED_SWORD_TOP, RUNED_SWORD_BOT]

ITEMS = ITEM_WEAPONS + ITEM_ARMORS + ITEM_CONSUMABLES + ITEM_MISC + ITEM_QUEST

QUESTS = [QUEST_MISTY_TANKARD, QUEST_HARKENS_POLE, QUEST_RAT_TOOTH, QUEST_BARK_MAP]
