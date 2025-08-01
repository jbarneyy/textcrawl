
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


def main():

    iron_sword = Item("Iron Sword", ItemType.WEAPON, 5, "A simple iron sword.")
    fish = Item("Small Fish", ItemType.MISC, 0, "A small blue fish.")
    mead = Item("Mead", ItemType.CONSUMABLE, 0, "A delicous glass of mead.")

    start_zone = Zone("Lake of Thoughts", [POI("Lakefront", "Our adventurer awakens on the lake.", (0, 0), [fish]), 
                                           POI("Shepard's Inn", "A small inn located near the edge of the lake.", (0, 2), [mead])], 
                                           "A large still lake. The water sparkles clear and blue.")
    
    player = Character("Jacko", 100, 100, None, [iron_sword], None, 5, POI("Lakefront", "Our adventurer awakens on the lake.", (0, 0), [fish]))

    game_state = f"""
        You are an AI Dungeon Master for a text-based adventure game. The adventurer is {player.to_string()}.
        Our starting zone is {start_zone.to_string()}.

        Keep responses between 20 and 120 words.

        Try to only use information that is provided. Do not invent new zones or locations. Do not list items near player unless they search for them. Feel free to invent smaller details.
    """

    # Reads the .env file in the root of project. Loads the variables into the environment. #
    load_dotenv()

    # Retrieves the value of GEMINI_API_KEY from the environment. Values in .env are loaded and retreived using os.environ.get() #
    api_key = os.environ.get("GEMINI_API_KEY")

    # Creates a new Gemini client instance using your API key. Will use this to generate responses. #
    # Configure client and tools #
    client = genai.Client(api_key=api_key)
    tools = [available_functions]
    config = types.GenerateContentConfig(max_output_tokens=100, system_instruction=game_state, tools=tools)


    response = client.models.generate_content(model="gemini-2.0-flash-001", contents="Welcome the adventurer to our world.", config=config)

    #print(response.text)
    slow_print_text(response.text, 0.02)

    while True:

        player_response = input("> ")

        if player_response.strip().lower() in ("quit", "exit"):
            break
        
        

        try:
            response = client.models.generate_content(model="gemini-2.0-flash-001", contents=player_response, config=config)
            #print(response.text)
            slow_print_text(response.text, 0.02)
            
        except Exception as e:
            print(f"Error generating response: {e}")



def slow_print_text(text: str, delay: float):
    for char in text:
        # Writes single character to stdout #
        sys.stdout.write(char)

        # Flushes stdout's buffer to the CLI, without this it would build text and return at end #
        sys.stdout.flush()

        # Delays next action by float (delay) seconds #
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

available_functions = types.Tool(
    function_declarations=[
        schema_grab_item
    ]
)


if __name__ == "__main__":
    main()
