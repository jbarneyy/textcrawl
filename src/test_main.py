import unittest

from character import Character
from item import Item, ItemType



class Test(unittest.TestCase):
    
    def setUp(self):

        self.iron_sword = Item("Iron Sword", ItemType.WEAPON, 5, "A rusty iron sword.")
        self.torch = Item("Torch", ItemType.MISC, 0, "A bright torch.")
        self.health_potion = Item("HP Potion", ItemType.CONSUMABLE, 20, "A health potion to restore health.")

        self.items = [self.iron_sword, self.torch, self.health_potion]

        self.player = Character("Testy", 100, 100, None, self.items, None, 5)

    
    def test_simple(self):
        print(self.player.to_string())