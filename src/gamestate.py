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

            Our current Point of Interest (POI) / Location is: {self.player.current_POI.to_string()}.

            Nearby POIs / Areas / Villages / Towns / Locations are: {", ".join(map(POI.to_string, self.get_nearby_pois()))}.

            Nearby NPCs / Characters: {", ".join(map(Character.to_string, self.get_nearby_characters(self.player)))}

            Nearby Enemies: {", ".join(map(Enemy.to_string, self.get_nearby_enemies(self.player)))}

            Keep responses between 20 and 120 words.

            Always attempt to call a function from tools over returning text, if function is available / usable.

            Feel free to give general responses to player/character actions. Do not invent new zones or locations. Feel free to invent smaller details.

            Actions our Player can perform: Grab Item, List Inventory, Move Location, Equip Item, Attack Enemy.
        """

    
    def get_gamestate(self) -> str:
        return self.game_state
    
    def update_gamestate(self) -> str:
        self.game_state = f"""
            You are an AI Dungeon Master for a text-based adventure game.
            
            The adventurer is {self.player.to_string()}.

            Our current Zone is {self.player.current_zone.to_string()}.

            Our current Point of Interest (POI) / Location is: {self.player.current_POI.to_string()}.

            Nearby POIs / Areas / Villages / Towns / Locations are: {", ".join(map(POI.to_string, self.get_nearby_pois()))}.

            Nearby NPCs / Characters: {", ".join(map(Character.to_string, self.get_nearby_characters(self.player)))}

            Nearby Enemies: {", ".join(map(Enemy.to_string, self.get_nearby_enemies(self.player)))}

            Keep responses between 20 and 120 words.

            Always attempt to call a function from tools over returning text, if function is available / usable.

            Feel free to give general responses to player/character actions. Do not invent new zones or locations. Feel free to invent smaller details.

            Actions our Player can perform: Grab Item, List Inventory, Move Location, Equip Item, Attack Enemy.
        """
        return self.game_state
    
    def get_nearby_characters(self, player: Player) -> list[Character]:
        """Returns list of nearby characters by the player.

        Args:
            player: Player object representing our player.

        Returns:
            List of characters that are in the same POI as our Player object.
        """
        nearby_characters = []

        for character in self.characters.values():
            if character.current_POI is player.current_POI:
                nearby_characters.append(character)

        return nearby_characters
    
    def get_nearby_enemies(self, player: Player) -> list[Enemy]:
        """Returns list of nearby enemies by the player.

        Args:
            player: Player object representing our player.

        Returns:
            List of enemies that are in the same POI as our Player object.
        """
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
            String representing one roll of attack between Player and Enemy in battle.
        """
        if (player.current_POI is not enemy.current_POI):
            return f"{player.name} cannot attack {enemy.name}."

        player_damage = player.roll_attack() - enemy.defence
        enemy_damage = enemy.roll_attack() - player.armor.power

        if (enemy_damage < 0): enemy_damage = 0
        if (player_damage < 0): player_damage = 0

        enemy.health -= player_damage
        player.health -= enemy_damage
        
        return f"{player.name} has dealt {player_damage} damage to {enemy.name}.\n{enemy.name} has dealt {enemy_damage} damage to {player.name}."
    

    def get_nearby_pois(self) -> list[POI]:
        """Gets the POIs that are less than or equal to 5 distance away from Player's current POI.
        Will be used when Player is looking around for nearby POIs.

        Args:
            None: Will use the only Player instance to determine current Zone / current POI.

        Returns:
            List of the POIs nearest the Player.
        """
        nearby_pois: list[POI] = []

        current_zone = self.player.current_zone
        current_poi = self.player.current_POI

        for target_poi in current_zone.points_of_interest:

            if current_poi is not target_poi and target_poi.is_open is True:
                distance_to_poi = (abs(current_poi.location[0] - target_poi.location[0]) + abs(current_poi.location[1] - target_poi.location[1])) / 2

                if distance_to_poi <= 5:
                    nearby_pois.append(target_poi)
        
        return nearby_pois


    def trade(self, character: Character):
        """
        """

        pass