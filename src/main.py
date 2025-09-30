
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
import random

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

    intro_text()

    player_name = input("> ")

    player = Player(name=player_name, health=100, items=[init.SMALL_HP], armor=init.LEATHER_ARMOR, weapon=init.IRON_SWORD,
                     quests=[init.QUEST_DAYSHARD, init.QUEST_MISTY_TANKARD], level=1, current_POI=init.LAKEFRONT, current_zone=init.EVERDUSK_VALE, coins=10,
                     description="Our fearless adventurer.")


    game_state = GameState(zones=init.ZONES, pois=init.POIS, characters=init.CHARACTERS, enemies=init.ENEMIES, items=init.ITEMS, quests=init.QUESTS, player=player)

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

    print(response.text)

    print(("During your adventure you may find it helpful to 'search' for people / items / areas / enemies in your current location. You never know what you may discover.\n"
            "There are also actions that you can perform as you travel through Everdusk: 'Grab/Pickup', 'List Inventory', 'Move Locations', 'Equip Weapon/Armor', 'Attack Enemy', 'Trade Character', 'Accept Quest', 'Use Item'.\n"))

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

            #print(f"Candidate Content Parts: {candidate.content.parts}\n")

            # A part of a response is object containing different types of information. We are only interested in function_call and text. #
            #part = candidate.content.parts[0]
            parts = candidate.content.parts
            
            for part in parts:
                # Logic for handling a function_call by Gemini. #
                if part.function_call is not None:

                    character_action = f"{call_function(part.function_call, player, game_state)}"

                    chat_history.append(types.Content(role="model", parts=[types.Part(text=f"{character_action}")]))

                    config = types.GenerateContentConfig(max_output_tokens=100, system_instruction=game_state.get_gamestate(), tools=tools)

                    print(character_action + "\n", flush=True)
                    #slow_print_text(character_action)

                # Logic for responding if there is not a function_call. #
                elif part.text is not None:

                    refusal_matches = ["i am unable", "i'm unable", "i cannot", "i can't", "i am sorry", "i'm sorry", "i am programmed", "i'm programmed"]
                    lower_response = part.text.lower()

                    if (any(text in lower_response for text in refusal_matches)):
                        player_actions = "Here are some actions you can try performing: 'Grab an Item', 'List your Inventory', 'Move Locations', 'Equip Armor/Weapon', 'Attack Enemy', 'Trade', 'Start Quest', 'Use an Item'."
                        refusal_responses = [
                            "What an odd request traveler.",
                            "No spell in this realm can weave that outcome.",
                            "Your words fall on deaf ears; none here can grant that.",
                            "The world resists your command, as if the gods themselves shake their heads.",
                            "Your plea drifts into the void, unanswered.",
                            "The veil between worlds remains closed to such a request.",
                            "Your command clangs against the iron laws of this realm.",
                            "No merchant, monster, nor mortal will heed those words.",
                            "A cold wind erases the very sound of your request."
                        ]
                        updated_response = f"{random.choice(refusal_responses)}\n{player_actions}"

                        chat_history.append(types.Content(role="model", parts=[types.Part(text=updated_response)]))
                        print(updated_response, flush=True)
                        #slow_print_text(character_action)
                        
                    else:
                        chat_history.append(types.Content(role="model", parts=[types.Part(text=f"{part.text}")]))
                        print(part.text, flush=True)
                        #slow_print_text(part.text)
            
        except Exception as e:
            print(f"Error generating response: {e}")


        if (check_player_alive(player) is False):
            print("All adventures must come to an end. It's a shame you died without completing your quest. See you in the next iteration.")
            break


def slow_print_text(text: str, delay: float = 0.015):
    for char in text:
        # Writes single character to stdout. #
        sys.stdout.write(char)

        # Flushes stdout's buffer to the CLI, without this it would build text and return at end. #
        sys.stdout.flush()

        # Delays next action by float (delay) seconds. #
        time.sleep(delay)
    
    sys.stdout.write("\n")


def intro_text():
    print("You find yourself waking up at the Singing Lake. The last thing you remember was the sensation of falling - faster and faster - and then the feeling of cool dew and wet earth. Your head aches something fierce.\n")

    print("A voice echos in your head, it has a soothing presence. 'Welcome back'.\n")

    print("Who are you and where am I? You ask the voice.\n")

    print("'You are in Everdusk Vale - a land bathed in perpetual twilight.'\n")

    print("You look around and see an indigo sky streaked with slow-moving auroras. Vast crystal spires float like lazy comets above the landscape, " \
    "shedding shimmering aether dust that fuels both wonder and danger. Gravity feels slightly lighter; magic hums beneath every stone.\n")

    print("'Seek out the Dayheart - reassamble the components.' The voice commands. 'What will you call yourself on this iteration?'\n")


def check_player_alive(player: Player) -> bool:
    if (player.health <= 0):
        return False
    else:
        return True
    

if __name__ == "__main__":
    main()
