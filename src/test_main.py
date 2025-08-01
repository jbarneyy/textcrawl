import unittest

from character import Character
from item import Item, ItemType
from zone import Zone
from poi import POI


class Test(unittest.TestCase):
    
    def setUp(self):

        self.iron_sword = Item("Iron Sword", ItemType.WEAPON, 5, "A rusty iron sword.")
        self.torch = Item("Torch", ItemType.MISC, 0, "A bright torch.")
        self.health_potion = Item("HP Potion", ItemType.CONSUMABLE, 20, "A health potion to restore health.")
        self.fish = Item("Small Fish", ItemType.MISC, 0, "A small fish.", True)
        self.mead = Item("Mead", ItemType.CONSUMABLE, 0, "A nice cool glass of mead.", True)

        self.location_1 = POI("Lakefront", "Our adventurer awakens on the lake.", (0, 0), [self.fish, self.health_potion])
        self.location_2 = POI("Shepard's Inn", "A small inn located near the edge of the lake.", (0, 2), [self.mead])

        start_zone = Zone("Lake of Thoughts", [self.location_1, self.location_2], "A large still lake. The water sparkles clear and blue.")
        
        self.player = Character("Testy", 100, 100, None, [self.iron_sword], None, 5, self.location_1)

    
    def test_simple(self):
        print("-- TEST SIMPLE --")
        
        print(self.player.to_string())

    def test_grab_item(self):
        print("-- TEST GRAB ITEM --")
        print(f"Player before grab: {self.player.to_string()}")
        print(f"POI before grab: {self.location_1.to_string()}")

        self.player.grab_item("small fish")

        print(f"Player after grab: {self.player.to_string()}")
        print(f"POI after grab: {self.location_1.to_string()}")