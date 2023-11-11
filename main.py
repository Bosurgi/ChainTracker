import tracker
import os
from dotenv import load_dotenv

load_dotenv()
API_CALL = os.getenv('API_CALL')

# Running the bot
if __name__ == '__main__':
    tracker.bot.run(os.environ["DISCORD_TOKEN"])
