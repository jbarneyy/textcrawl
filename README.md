# textcrawl
Text based adventure game using Gemini to curate custom adventure.

## SetUp
1. Clone repo into local folder.
2. Create virtual environment using `python3 -m venv venv`
3. Activate virtual environment `source venv/bin/activate`
4. Install requirements with pip `pip install -r requirements.txt`
5. Create .env file in root of project, and create a [Gemini API Key](https://aistudio.google.com/app/api-keys).
6. In .env add the following line: `GEMINI_API_KEY=YourAPIKey`
7. Save all above files, make sure you are in venv, run `./main.sh` to start game.