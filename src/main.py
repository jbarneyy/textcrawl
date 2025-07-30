
# Gives access to system environment variables, file paths, etc. #
import os

# Useful for system-level functions (not used here yet, but often added for sys.exit() or path manipulation). #
import sys

# Imports the Gemini (Generative AI) Python client from the google package namespace. #
# Genai is the module you use to interact with the Gemini API. #
from google import genai
from google.genai import types

# Load_dotenv() is used to load env variables from .env file instead of hardcoding them in. #
from dotenv import load_dotenv

from item import Item, ItemType
from character import Character


def main():

    iron_sword = Item("Iron Sword", ItemType.WEAPON, 5, "A simple iron sword.")
    player = Character("Jacko", 100, 100, None, [iron_sword], None, 5)

    # Reads the .env file in the root of project. Loads the variables into the environment. #
    load_dotenv()

    # Retrieves the value of GEMINI_API_KEY from the environment. Values in .env are loaded and retreived using os.environ.get() #
    api_key = os.environ.get("GEMINI_API_KEY")

    # Creates a new Gemini client instance using your API key. Will use this to generate responses. #
    client = genai.Client(api_key=api_key)

    game_state = f"You are an AI Dungeon Master for a text-based adventure game. The adventurer's is {player.to_string()}. Keep response less than 100 words."

    response = client.models.generate_content(model="gemini-2.0-flash-001", contents="Welcome the adventurer to our world.", config=types.GenerateContentConfig(max_output_tokens=100, system_instruction=game_state))

    print(response.text)


    while True:

        player_response = input("> ")

        if player_response.strip().lower() in ("quit", "exit"):
            break
        
        

        try:
            response = client.models.generate_content(model="gemini-2.0-flash-001", contents=player_response, config=types.GenerateContentConfig(max_output_tokens=100, system_instruction=game_state))
            print(response.text)
        except Exception as e:
            print(f"Error generating response: {e}")




if __name__ == "__main__":
    main()