
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

    game_state = GameState(zones=[init.LAKE_OF_THOUGHTS], pois=[init.LAKEFRONT, init.MISTY_TANKARD], characters=[init.HARKEN_BRISTLE], items=[init.IRON_DAGGER], player=player)

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


schema_grab_item = types.FunctionDeclaration(
    name="grab_item",
    description="Grab/pickup an item from the player/character's current POI and place it into character's inventory, if item can_pickup is true. Deletes the item from POI's list of Items.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "grab": types.Schema(
                type=types.Type.STRING,
                description="String representing the Item.name of the item player attempts to grab.",
            ),
        },
        required=["grab"]
    ),
)

schema_list_items = types.FunctionDeclaration(
    name="list_items",
    description="List/display/show character's inventory. Function will return a formatted string displaying the character's inventory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={},
        required=[]
    ),
)

schema_move = types.FunctionDeclaration(
    name="move",
    description="Move character from current POI to target_location POI. Takes target POI as argument, returns True if character can move to target_location, else returns False.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "target_location": types.Schema(
                type=types.Type.OBJECT,
                description="Target location / POI / Point of Interest that character is attempting to move to."
            )
        },
        required=["target_location"]
    )
)

schema_equip_item = types.FunctionDeclaration(
    name="equip_item",
    description="Equip an item from the player's inventory into either player's armor var or player's weapon var. Item must be in inventory and of ItemType.WEAPON or ItemType.ARMOR." \
    "If an item is already equipped, it will move the current equip into player's inventory. Returns True if item is successfully equipped to player.armor or player.weapon. False if equip is unsuccessful.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "item_name": types.Schema(
                type=types.Type.STRING,
                description="String representing the name of the item (Item.name) that player is attempting to equip.",
            ),
        },
        required=["item_name"]
    ),
)

# Must wrap function declaration schemes as a types.Tool to pass in as list[Tool] to client config. #
available_functions = types.Tool(
    function_declarations=[
        schema_grab_item,
        schema_list_items,
        schema_move,
        schema_equip_item
    ]
)

def call_function(function: types.FunctionCall, player: Player, game_state: GameState):
    function_args = function.args
    function_name = function.name

    #print("Inside CALL_FUNCTION")

    if (function_name == "grab_item"):
        result = player.grab_item(grab=function_args["grab"])

        if (result is True):
            game_state.update_gamestate()
            return f"{player.name} grabs {function_args["grab"]}."
        else:
            return f"{player.name} cannot pickup {function_args["grab"]}."
        

    if (function_name == "list_items"):
        game_state.update_gamestate()
        return player.list_items()
    
    
    if (function_name == "move"):
        target_poi = function_args["target_location"]
        target_poi_name = target_poi["Name"]

        result = player.move(target_location=game_state.pois[target_poi_name])

        if result is True:
            game_state.update_gamestate()
            return f"{player.name} moves to {player.current_POI.name}"
        else:
            return f"{player.name} is unable to go there at this time."
        
    
    if (function_name == "equip_item"):
        result = player.equip_item(item_name=function_args["item_name"])

        if (result is True):
            game_state.update_gamestate()
            return f"{player.name} equips {function_args["item_name"]}."
        else:
            return f"{player.name} is unable to equip that."


if __name__ == "__main__":
    main()
