
# Gives access to system environment variables, file paths, etc. #
import os

# Useful for system-level functions (not used here yet, but often added for sys.exit() or path manipulation). #
import sys
import time

# Imports the Gemini (Generative AI) Python client from the google package namespace. #
# Genai is the module you use to interact with the Gemini API. #
from google import genai
from google.genai import types

from collections import deque

# Load_dotenv() is used to load env variables from .env file instead of hardcoding them in. #
from dotenv import load_dotenv

from function_schemas import available_functions
from function_call import call_function

from item import Item, ItemType
from character import Character
from player import Player
from zone import Zone
from poi import POI

import init
from gamestate import GameState

def main():

    player = Player(name="Jacko", health=100, items=[init.SMALL_HP], armor=init.LEATHER_ARMOR, weapon=init.IRON_SWORD, quests=None, level=1, current_POI=init.LAKEFRONT, current_zone=init.LAKE_OF_THOUGHTS, coins=100)

    #player = Character("Jacko", 100, [init.IRON_SWORD], None, 5, init.LAKEFRONT, init.LAKE_OF_THOUGHTS)

    game_state = GameState(zones=[init.LAKE_OF_THOUGHTS], pois=[init.LAKEFRONT, init.MISTY_TANKARD], characters=[init.HARKEN_BRISTLE], enemies=[init.GIANT_RAT], items=[init.IRON_DAGGER, init.SMALL_HP, init.SMALL_MP], player=player)

    # Reads the .env file in the root of project. Loads the variables into the environment. #
    load_dotenv()

    # Retrieves the value of GEMINI_API_KEY from the environment. Values in .env are loaded and retreived using os.environ.get() #
    api_key = os.environ.get("GEMINI_API_KEY")

    # Creates a new Gemini client instance using your API key. Will use this to generate responses. #
    # Configure client and tools. #
    client = genai.Client(api_key=api_key)
    tools = [available_functions]
    config = types.GenerateContentConfig(max_output_tokens=150, system_instruction=game_state.get_gamestate(), tools=tools)

    # Using chat_history deque to make Gemini stateful. Will hold 20 interactions between user / model before automatically popping head of queue. #
    chat_history = deque(maxlen=20)

    response = client.models.generate_content(model="gemini-2.0-flash-001", contents="Welcome the adventurer to our world.", config=config)

    chat_history.append(types.Content(role="model", parts=[types.Part(text=f"{response.text}")]))

    #slow_print_text(response.text, 0.02)
    print(response.text)

    while True:

        player_response = input("> ")

        if player_response.strip().lower() in ("quit", "exit"):
            break

        chat_history.append(types.Content(role="user", parts=[types.Part(text=f"{player_response}")]))

        try:
            # response is the full Gemini model response. #
            response = client.models.generate_content(model="gemini-2.0-flash-001", contents=chat_history, config=config)

            # candidate is the first (and often only) candidate. There can be multiple candidates, we are only going to have one. #
            candidate = response.candidates[0]

            print(f"Candidate Content Parts: {candidate.content.parts}\n")

            # A part of a response is object containing different types of information. We are only interested in function_call and text. #
            part = candidate.content.parts[0]

            # Logic for handling a function_call by Gemini. #
            if part.function_call is not None:

                character_action = f"{call_function(part.function_call, player, game_state)}"

                chat_history.append(types.Content(role="model", parts=[types.Part(text=f"{character_action}")]))

                config = types.GenerateContentConfig(max_output_tokens=100, system_instruction=game_state.get_gamestate(), tools=tools)

                print(character_action + "\n")

                # except Exception as e:
                #     print("ENCOUNTERED FUNC_CALL ISSUE!!!!")
                    
                #     system_error_message = f"You had an issue trying to complete Player's previous response and called a function in error: {e}. We are going to ask for an additonal player response and ask them to try again. " \
                #     f"In your next generated response explain you had an issue in a fantasy-type way. Make sure your next response defaults to a text response and does not call an additional function."

                #     chat_history.append(types.Content(role="model", parts=[types.Part(text=system_error_message)]))

                #     response = client.models.generate_content(model="gemini-2.0-flash-001", contents=chat_history, config=config)

                #     print(response.text)




            # Logic for responding if there is not a function_call. #
            elif part.text is not None:
                chat_history.append(types.Content(role="model", parts=[types.Part(text=f"{response.text}")]))

                print(response.text)
                #slow_print_text(response.text, 0.02)
            
        except Exception as e:
            print(f"Error generating response: {e}")



def slow_print_text(text: str, delay: float = 0.03):
    for char in text:
        # Writes single character to stdout. #
        sys.stdout.write(char)

        # Flushes stdout's buffer to the CLI, without this it would build text and return at end. #
        sys.stdout.flush()

        # Delays next action by float (delay) seconds. #
        time.sleep(delay)
    
    sys.stdout.write("\n")
                    


if __name__ == "__main__":
    main()
