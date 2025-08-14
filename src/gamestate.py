from zone import Zone
from poi import POI
from item import Item
from character import Character
from player import Player
from enemy import Enemy

import init


class GameState():

    def __init__(self, zones: list[Zone] | None, pois: list[POI] | None, characters: list[Character] | None, enemies: list[Enemy] | None, items: list[Item] | None, player: Player):

        self.zones: dict[str, Zone] = {}
        self.pois: dict[str, POI] = {}
        self.characters: dict[str, Character] = {}
        self.items: dict[str, Item] = {}
        self.enemies: dict[str, Enemy] = {}
        
        for zone in zones:
            self.zones[zone.name] = zone

        for poi in pois:
            self.pois[poi.name] = poi

        for character in characters:
            self.characters[character.name] = character

        for item in items:
            self.items[item.name] = item

        for enemy in enemies:
            self.enemies[enemy.name] = enemy

        self.player = player

        self.game_state = f"""
            You are an AI Dungeon Master for a text-based adventure game.
            
            The adventurer is {self.player.to_string()}.

            Our current Zone is: {self.player.current_zone.to_string()}.

            Our current POI is: {self.player.current_POI.to_string()}.

            Nearby NPCs / Characters: {", ".join(map(Character.to_string, self.get_nearby_characters(self.player)))}

            Nearby Enemies: {", ".join(map(Enemy.to_string, self.get_nearby_enemies(self.player)))}

            Keep responses between 20 and 120 words.

            Feel free to give general responses to player/character actions. Do not invent new zones or locations. Do not list items near player unless they search for them. Feel free to invent smaller details.

            Always attempt to call function_call over returning text.
        """

    
    def get_gamestate(self) -> str:
        return self.game_state
    
    def update_gamestate(self) -> str:
        self.game_state = f"""
            You are an AI Dungeon Master for a text-based adventure game.
            
            The adventurer is {self.player.to_string()}.

            Our current Zone is {self.player.current_zone.to_string()}.

            Our current POI is: {self.player.current_POI.to_string()}.

            Nearby NPCs / Characters: {", ".join(map(Character.to_string, self.get_nearby_characters(self.player)))}

            Nearby Enemies: {", ".join(map(Enemy.to_string, self.get_nearby_enemies(self.player)))}

            Keep responses between 20 and 120 words.

            Feel free to give general responses to player/character actions. Do not invent new zones or locations. Do not list items near player unless they search for them. Feel free to invent smaller details.

            Always attempt to call function_call over returning text.
        """
        return self.game_state
    
    def get_nearby_characters(self, player: Player) -> list[Character]:
        nearby_characters = []

        for character in self.characters.values():
            if character.current_POI is player.current_POI:
                nearby_characters.append(character)

        return nearby_characters
    
    def get_nearby_enemies(self, player: Player) -> list[Enemy]:
        nearby_enemies = []

        for enemy in self.enemies.values():
            if enemy.current_POI is player.current_POI:
                nearby_enemies.append(enemy)

        return nearby_enemies

    def attack_enemy(self, player: Player, enemy: Enemy) -> str:
        """Attack an enemy if player and enemy are in the same POI. Rolls one attack round of player attacking enemy and enemy attacking player.

        Args:
            player: Player object representing our player.
            enemy: Enemy object representing the enemy our player is attacking.

        Returns:
            String representing outcome of battle.
        """
        if (player.current_POI is not enemy.current_POI):
            return f"{player.name} cannot attack {enemy.name}."

        player_damage = player.roll_attack()
        enemy_damage = enemy.roll_attack()

        enemy.health -= player_damage
        player.health -= enemy_damage

        if (enemy.health <= 0):
            return f"{player.name} has defeated {enemy.name}."
        
        return f"{player.name} has dealt {player_damage} to {enemy.name}.\n{enemy.name} has dealt {enemy_damage} to {player.name}."