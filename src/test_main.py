import unittest

from character import Character
from item import Item, ItemType
from zone import Zone
from poi import POI
from enemy import Enemy
from player import Player

from gamestate import GameState


class Test(unittest.TestCase):
    
    def setUp(self):
        # Initialize Items #
        self.iron_sword = Item("Iron Sword", ItemType.WEAPON, 5, "A rusty iron sword.", True)
        self.iron_armor = Item("Iron Armor", ItemType.ARMOR, 10, "Iron armor, seems better than leather.", True)
        self.leather_armor = Item("Leather Armor", ItemType.ARMOR, 5, "Basic leather armor, smells like shit.", True)
        
        self.health_potion = Item("HP Potion", ItemType.CONSUMABLE, 20, "A health potion to restore health.", True)

        self.fish = Item("Small Fish", ItemType.MISC, 0, "A small fish.", True)
        self.torch = Item("Torch", ItemType.MISC, 0, "A bright torch.", True)
        self.rat_tooth = Item("Rat Tooth", ItemType.MISC, 5, "A crusty and bloody rat tooth.", True)

        self.location_1 = POI("Lakefront", "Our adventurer awakens on the lake.", (0, 0), [self.fish, self.torch, self.iron_armor], True)
        self.location_2 = POI("Shepard's Inn", "A small inn located near the edge of the lake.", (0, 2), [self.health_potion, self.health_potion], True)

        self.start_zone = Zone("Lake of Thoughts", [self.location_1, self.location_2], "A large still lake. The water sparkles clear and blue.")
        
        self.npc_1 = Character("Sam Wise", 100, [self.fish], None, 1, self.location_2, self.start_zone)
        self.npc_2 = Character("Harken Bristle", 100, [self.health_potion], None, 1, self.location_2, self.start_zone)

        self.enemy_1 = Enemy("Giant Rat", 20, 1, [self.rat_tooth], 1, self.location_1)

        self.player = Player("Jack", 100, [self.torch], self.leather_armor, self.iron_sword, None, 5, self.location_1, self.start_zone)

        self.game_state = GameState([self.start_zone], [self.location_1, self.location_2], [self.npc_1, self.npc_2], [self.enemy_1], [self.iron_sword, self.iron_armor, self.torch, self.fish, self.health_potion, self.rat_tooth], self.player)


    def test_grab_item(self):
        self.player.grab_item("small fish")
        self.assertIn(self.fish, self.player.items)


    def test_move(self):
        self.assertEqual(self.player.current_POI, self.location_1)
        self.player.move(self.location_2)
        self.assertEqual(self.player.current_POI, self.location_2)


    def test_equip(self):
        self.assertEqual(self.player.armor, self.leather_armor)
        self.player.grab_item("Iron Armor")
        self.player.equip_item("Iron Armor")
        self.assertEqual(self.player.armor, self.iron_armor)
        

    def test_gamestate(self):
        print(self.game_state.get_gamestate())
        print("\n")

        # print(self.game_state.get_nearby_characters(self.player))
        # print("\n")
        self.assertListEqual(self.game_state.get_nearby_characters(self.player), [])

        # print(self.game_state.get_nearby_enemies(self.player))
        self.assertListEqual(self.game_state.get_nearby_enemies(self.player), [self.game_state.enemies["Giant Rat"]])

    def test_attack_enemy(self):
        print(self.player.to_string() + "\n")
        print(self.enemy_1.to_string() + "\n")

        self.game_state.attack_enemy(self.player, self.enemy_1)

        print(self.player.to_string() + "\n")
        print(self.enemy_1.to_string() + "\n")


    
        

    