from zone import Zone
from poi import POI
from item import Item
from character import Character

import init


class GameState():

    def __init__(self, zones: list[Zone] | None, pois: list[POI] | None, characters: list[Character] | None, items: list[Item] | None, player: Character):

        self.zones: dict[str, Zone] = {}
        self.pois: dict[str, POI] = {}
        self.characters: dict[str, Character] = {}
        self.items: dict[str, Item] = {}
        
        for zone in zones:
            self.zones[zone.name] = zone

        for poi in pois:
            self.pois[poi.name] = poi

        for character in characters:
            self.characters[character.name] = character

        for item in items:
            self.items[item.name] = item

        self.player = player

        self.game_state = f"""
            You are an AI Dungeon Master for a text-based adventure game.
            
            The adventurer is {self.player.to_string()}.

            Our current Zone is: {self.player.current_zone.to_string()}.

            Our current POI is: {self.player.current_POI.to_string()}.

            Nearby NPCs / Characters: {", ".join(map(Character.to_string, self.get_nearby_characters(self.player)))}

            Keep responses between 20 and 120 words.

            Try to only use information that is provided. Do not invent new zones or locations. Do not list items near player unless they search for them. Feel free to invent smaller details.
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

            Keep responses between 20 and 120 words.

            Try to only use information that is provided. Do not invent new zones or locations. Do not list items near player unless they search for them. Feel free to invent smaller details.
        """
        return self.game_state
    
    def get_nearby_characters(self, player: Character) -> list[Character]:
        nearby_characters = []

        for character in self.characters.values():
            if character.current_POI is player.current_POI:
                nearby_characters.append(character)

        return nearby_characters
    
    def print_pois(self):
        print(self.pois)