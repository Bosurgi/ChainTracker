# This example requires the 'message_content' privileged intents

import os
import discord
from discord.ext import commands, tasks
from discord.utils import get
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
ROLE_NAME = 'Wrath'
check_task = None


# It parses the data from the API call and generates a dictionary containing the data
def parse_data(url_request):
    data = url_request.json()
    # Dumping the data into a string
    json_str = json.dumps(data, sort_keys=True, indent=4)
    return json.loads(json_str)


# Task running every 30 seconds to check if the timeout is less than 2 minutes
@tasks.loop(seconds=30)
async def check_timer(ctx):
    chain_data = parse_data(requests.get(API_CALL))
    timeout = chain_data['chain']['timeout']

    try:

        if timeout <= 120:

            role = discord.utils.get(ctx.guild.roles, name=ROLE_NAME)
            await ctx.send(f'{role.mention} - Chain ending in 2 minutes!')

        elif timeout == 0:
            role = discord.utils.get(ctx.guild.roles, name=ROLE_NAME)
            await ctx.send(f'{role.mention} - Chain ended!')

    except ValueError:
        print(f'No {ROLE_NAME} found')


# It checks if the chain timeout is expiring
# Returns true if timer is close to expire


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.command
async def start_watching(ctx):
    wrath = get(ctx.guidl.roles, name='Wrath')
    global check_task
    if check_task is None:
        check_task = check_timer.start()
        await ctx.send("Chain watch started!")
    else:
        await ctx.send("Chain watch already running!")


@bot.command
async def stop_watching(ctx):
    global check_task
    if check_task:
        check_timer.stop()
        await ctx.send("Watching stopped.")
    else:
        ctx.send("Watching not running.")
