# This example requires the 'message_content' privileged intents

import os
import discord
from discord.ext import commands
import json
from dotenv import load_dotenv
import time
import requests


# Loading .env variables
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
WATCH_MESSAGE = "Looking for chains. Start watching..."
API_CALL = os.getenv('API_CALL')
watching = False


# It parses the data from the API call and generates a dictionary containing the data
def parse_data(url_request):
    data = url_request.json()
    # Dumping the data into a string
    json_str = json.dumps(data, sort_keys=True, indent=4)
    return json.loads(json_str)


# It checks if the chain timeout is expiring
# Returns true if timer is close to expire
def is_expiring():
    chain_data = parse_data(requests.get(API_CALL))
    timeout = chain_data['chain']['timeout']
    if timeout < 120:
        return True
    else:
        return False


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.command
async def start_watching():
    # TODO: Implement command
    return
