
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
from zone import Zone
from poi import POI

import init


def main():

    player = Character("Jacko", 100, 100, None, [init.IRON_SWORD], None, 5, init.LAKEFRONT)

    game_state = f"""
        You are an AI Dungeon Master for a text-based adventure game. The adventurer is {player.to_string()}.
        Our zone is {init.LAKE_OF_THOUGHTS.to_string()}.

        Keep responses between 20 and 120 words.

        Try to only use information that is provided. Do not invent new zones or locations. Do not list items near player unless they search for them. Feel free to invent smaller details.
    """

    # Reads the .env file in the root of project. Loads the variables into the environment. #
    load_dotenv()

    # Retrieves the value of GEMINI_API_KEY from the environment. Values in .env are loaded and retreived using os.environ.get() #
    api_key = os.environ.get("GEMINI_API_KEY")

    # Creates a new Gemini client instance using your API key. Will use this to generate responses. #
    # Configure client and tools. #
    client = genai.Client(api_key=api_key)
    tools = [available_functions]
    config = types.GenerateContentConfig(max_output_tokens=100, system_instruction=game_state, tools=tools)


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
                character_action = f"{call_function(part.function_call, player)}"

                game_state = f"""
                    You are an AI Dungeon Master for a text-based adventure game. The adventurer is {player.to_string()}.
                    Our zone is {init.LAKE_OF_THOUGHTS.to_string()}.

                    Keep responses between 20 and 120 words.

                    Try to only use information that is provided. Do not invent new zones or locations. Do not list items near player unless they search for them. Feel free to invent smaller details.
                """
                config = types.GenerateContentConfig(max_output_tokens=100, system_instruction=game_state, tools=tools)

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

# Must wrap function declaration schemes as a types.Tool to pass in as list[Tool] to client config. #
available_functions = types.Tool(
    function_declarations=[
        schema_grab_item,
        schema_list_items,
        schema_move
    ]
)

def call_function(function: types.FunctionCall, character: Character):
    args = function.args
    name = function.name

    #print("Inside CALL_FUNCTION")

    if (name == "grab_item"):
        result = character.grab_item(grab=args["grab"])

        if (result is True):
            return f"{character.name} grabs {args["grab"]}."
        else:
            return f"{character.name} cannot pickup {args["grab"]}."
        
    if (name == "list_items"):
        return character.list_items()
    
    if (name == "move"):
        result = character.move(target_location=args["target_location"])

        if result is True:
            return f"{character.name} moves to {character.current_POI.name}"
        else:
            return f"{character.name} is unable to go there at this time."


if __name__ == "__main__":
    main()
