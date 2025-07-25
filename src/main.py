
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


def main():

    # Reads the .env file in the root of project. Loads the variables into the environment. #
    load_dotenv()

    # Retrieves the value of GEMINI_API_KEY from the environment. Values in .env are loaded and retreived using os.environ.get() #
    api_key = os.environ.get("GEMINI_API_KEY")

    # Creates a new Gemini client instance using your API key. Will use this to generate responses. #
    client = genai.Client(api_key=api_key)

    game_state = "You are an AI Dungeon Master for a text-based adventure game. The adventurer's name is Thorn, he has an iron sword."

    response = client.models.generate_content(model="gemini-2.0-flash-001", contents="Welcome the adventurer to our world.", config=types.GenerateContentConfig(max_output_tokens=100, system_instruction=game_state))

    print(response.text)




if __name__ == "__main__":
    main()