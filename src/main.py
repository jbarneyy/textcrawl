
# Gives access to system environment variables, file paths, etc. #
import os

# Useful for system-level functions (not used here yet, but often added for sys.exit() or path manipulation). #
import sys
import time

# Imports the Gemini (Generative AI) Python client from the google package namespace. #
# Genai is the module you use to interact with the Gemini API. #
from google import genai
from google.genai import types

# Load_dotenv() is used to load env variables from .env file instead of hardcoding them in. #
from dotenv import load_dotenv

from function_schemas import available_functions

from item import Item, ItemType
from character import Character
from player import Player
from zone import Zone
from poi import POI

import init
from gamestate import GameState

def main():

    player = Player(name="Jacko", health=100, items=[init.SMALL_HP], armor=init.LEATHER_ARMOR, weapon=init.IRON_SWORD, quests=None, level=5, current_POI=init.LAKEFRONT, current_zone=init.LAKE_OF_THOUGHTS)

    #player = Character("Jacko", 100, [init.IRON_SWORD], None, 5, init.LAKEFRONT, init.LAKE_OF_THOUGHTS)

    game_state = GameState(zones=[init.LAKE_OF_THOUGHTS], pois=[init.LAKEFRONT, init.MISTY_TANKARD], characters=[init.HARKEN_BRISTLE], enemies=[init.GIANT_RAT], items=[init.IRON_DAGGER], player=player)

    # Reads the .env file in the root of project. Loads the variables into the environment. #
    load_dotenv()

    # Retrieves the value of GEMINI_API_KEY from the environment. Values in .env are loaded and retreived using os.environ.get() #
    api_key = os.environ.get("GEMINI_API_KEY")

    # Creates a new Gemini client instance using your API key. Will use this to generate responses. #
    # Configure client and tools. #
    client = genai.Client(api_key=api_key)
    tools = [available_functions]
    config = types.GenerateContentConfig(max_output_tokens=100, system_instruction=game_state.get_gamestate(), tools=tools)


    response = client.models.generate_content(model="gemini-2.0-flash-001", contents="Welcome the adventurer to our world.", config=config)

    #slow_print_text(response.text, 0.02)
    print(response.text)

    while True:

        player_response = input("> ")

        if player_response.strip().lower() in ("quit", "exit"):
            break

        try:
            # response is the full Gemini model response. #
            response = client.models.generate_content(model="gemini-2.0-flash-001", contents=player_response, config=config)

            # candidate is the first (and often only) candidate. There can be multiple candidates, we are only going to have one. #
            candidate = response.candidates[0]

            print(f"Candidate Content Parts: {candidate.content.parts}\n")

            # A part of a response is object containing different types of information. We are only interested in function_call and text. #
            part = candidate.content.parts[0]

            # Logic for handling a function_call by Gemini. #
            if part.function_call is not None:
                character_action = f"{call_function(part.function_call, player, game_state)}"

                config = types.GenerateContentConfig(max_output_tokens=100, system_instruction=game_state.get_gamestate(), tools=tools)

                print(character_action + "\n")
                

            # Logic for responding if there is not a function_call. #
            elif part.text is not None:
                print(response.text)
                #slow_print_text(response.text, 0.02)
            
        except Exception as e:
            print(f"Error generating response: {e}")



def slow_print_text(text: str, delay: float):
    for char in text:
        # Writes single character to stdout. #
        sys.stdout.write(char)

        # Flushes stdout's buffer to the CLI, without this it would build text and return at end. #
        sys.stdout.flush()

        # Delays next action by float (delay) seconds. #
        time.sleep(delay)
    
    sys.stdout.write("\n")


def call_function(function: types.FunctionCall, player: Player, game_state: GameState):
    function_args = function.args
    function_name = function.name

    #print("Inside CALL_FUNCTION")

    """
    Function call for Player() grab_item. If grab_item() is True will grab item and return.

    If grab_item() is False will not call grab_item().
    """
    if (function_name == "grab_item"):
        result = player.grab_item(grab=function_args["grab"])

        if (result is True):
            game_state.update_gamestate()
            return f"{player.name} grabs {function_args["grab"]}."
        else:
            return f"{player.name} cannot pickup {function_args["grab"]}."
        

    """
    Function call for Player() list_items. Will always evaluate to True and will return list of all items in Player() inventory.
    """
    if (function_name == "list_items"):
        game_state.update_gamestate()
        return player.list_items()
    
    
    """
    Function call for Player() move(). If Player() can move to listed POI will move Player().

    If Player() cannot move to requested POI will not move Player().
    """
    if (function_name == "move"):
        target_poi = function_args["target_location"]
        target_poi_name = target_poi["Name"]

        result = player.move(target_location=game_state.pois[target_poi_name])

        if result is True:
            game_state.update_gamestate()
            return f"{player.name} moves to {player.current_POI.name}"
        else:
            return f"{player.name} is unable to go there at this time."
        
    
    """
    Function call for Player() equip_item. If Item() is in Player() inventory and can_equip, will equip item and swap with inventory slot.
    """
    if (function_name == "equip_item"):
        result = player.equip_item(item_name=function_args["item_name"])

        if (result is True):
            game_state.update_gamestate()
            return f"{player.name} equips {function_args["item_name"]}."
        else:
            return f"{player.name} is unable to equip that."
        

    """
    Function call for GameState() attack_enemy(). If enemy is in same POI as Player() will start attack dialogue.

    Continue attack dialogue until Player() flees or completes battle.
    """
    if (function_name == "attack_enemy"):
        
        target_enemy_name = function_args["enemy"]["Name"]
        target_enemy = game_state.enemies[target_enemy_name]


        while True:
            print(f"{player.name} HP: {player.health} is battling {target_enemy_name} HP: {target_enemy.health}")
            print("1) Attack or 2) Flee" + "\n")
            player_response = input("> ")

            if (player_response == "2"):
                break

            print(game_state.attack_enemy(player, game_state.enemies[target_enemy_name]) + "\n")
            game_state.update_gamestate()

            if (target_enemy.health <= 0):
                # GameState() needs to remove Enemy entity #
                break
                


if __name__ == "__main__":
    main()
