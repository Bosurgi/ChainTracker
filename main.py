import tracker
import os
import requests
from dotenv import load_dotenv
load_dotenv()
API_CALL = os.getenv('API_CALL')

# Running the bot
if __name__ == '__main__':
    tracker.bot.run(os.environ["DISCORD_TOKEN"])
    #data = requests.get(API_CALL).json()
