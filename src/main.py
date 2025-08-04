
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

    iron_sword = Item("iron sword", ItemType.WEAPON, 5, "A simple iron sword.")
    fish = Item("small fish", ItemType.MISC, 0, "A small blue fish.", True)
    mead = Item("mead", ItemType.CONSUMABLE, 0, "A delicous glass of mead.")

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

    slow_print_text(response.text, 0.02)

    while True:

        player_response = input("> ")

        if player_response.strip().lower() in ("quit", "exit"):
            break


        try:
            response = client.models.generate_content(model="gemini-2.0-flash-001", contents=player_response, config=config)
            character_actions = ""

            if (response.function_calls):
                # Mutate game state based on each function in function calls, maybe one at a time? Update game state, generate new response based on new game state? #

                for function_call in response.function_calls:
                    print(function_call)
                    # call function and update game state based on function return
                    character_actions += f"{call_function(function_call, player)} "

                    print(f"CHARACTER_ACTIONS: {character_actions}")
                    print(f"CHARACTER STATUS: {player.to_string()}")
                    # generate new response? Or should called function return a string describing action that occurred?
                    
                    # For each function return (string), append to final return string? Feed entire string as player_response to contents of response call?

                    #
                
                game_state = f"""
                    You are an AI Dungeon Master for a text-based adventure game. The adventurer is {player.to_string()}.
                    Our starting zone is {start_zone.to_string()}.

                    Keep responses between 20 and 120 words.

                    Try to only use information that is provided. Do not invent new zones or locations. Do not list items near player unless they search for them. Feel free to invent smaller details.
                """
                config = types.GenerateContentConfig(max_output_tokens=100, system_instruction=game_state, tools=tools)
                response = client.models.generate_content(model="gemini-2.0-flash-001", contents=character_actions, config=config)


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

# Must wrap function declaration schemes as a types.Tool to pass in as list[Tool] to client config #
available_functions = types.Tool(
    function_declarations=[
        schema_grab_item
    ]
)

def call_function(function: types.FunctionCall, character: Character):
    args = function.args
    name = function.name

    if (name == "grab_item"):
        print("calling grab_item")
        print(f"Character Current POI: {character.current_POI}")
        character.grab_item(grab=args["grab"])

        print(f"Char ITEMS: {", ".join(map(Item.to_string, character.items))}")
        return f"{character.name} grabs {args["grab"]}."


if __name__ == "__main__":
    main()
