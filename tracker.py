# This example requires the 'message_content' privileged intents

import os
import discord
from discord.ext import commands, tasks
import json
from dotenv import load_dotenv
import time
import requests
import asyncio

# Loading .env variables
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

API_CALL = os.getenv('API_CALL')
ROLE_NAME = 'Wrath'
ATTACKS = 'current'
CHAIN = 'chain'
TIMEOUT = 'timeout'
check_task = None
timeout = 0

channel_id = 0
message_id = 0

countdown_embed = discord.Embed(title='Chain Watcher', description=f'Time left: ')


def getTime(api_url):
    chain_data = requests.get(api_url).json()
    return chain_data[CHAIN][TIMEOUT]


async def updateTimer():
    global timeout
    counter = 0
    countdown_seconds = getTime(API_CALL)
    while True:
        # Converting seconds to minutes and seconds remaining
        countdown_minutes = countdown_seconds // 60
        countdown_seconds_remaining = countdown_seconds % 60
        # Updating the embed description with new time
        countdown_embed.description = f'Time left: {countdown_minutes}:{countdown_seconds_remaining}'

        message = await bot.get_channel(1065701444486967297).fetch_message(message_id)
        await message.edit(embed=countdown_embed)

        # Wait one second and updating the seconds timer
        await asyncio.sleep(1)
        countdown_seconds -= 1
        countdown_seconds_remaining -= 1
        counter += 1

        if countdown_seconds == 0 and countdown_minutes > 0:
            countdown_minutes -= 1
            countdown_seconds = 59

        # After 30 seconds update the timeout making an API Call
        if counter >= 30:
            countdown_seconds = getTime(API_CALL)
            # Updating global variable
            timeout = countdown_seconds
            # Resetting the counter
            counter = 0

        if countdown_seconds == 0 and countdown_minutes == 0:
            break


"""
# Task running every 30 seconds to check if the timeout is less than 2 minutes
@tasks.loop(seconds=20)
async def check_timer(ctx):
    global role
    global callTime
    chain_data = requests.get(API_CALL)
    timeout = chain_data['chain']['timeout']
    converted = str(time.strftime('%M:%S', time.gmtime(timeout)))

    try:
        role = discord.utils.get(ctx.guild.roles, name=ROLE_NAME)
    except ValueError:
        print(f'No {ROLE_NAME} found')

    if timeout == 0:
        await ctx.send(f'{role.mention} - Chain ended!')
        check_timer.stop()
        await stop_watching(ctx)

    elif timeout <= 150:
        role = discord.utils.get(ctx.guild.roles, name=ROLE_NAME)

        await ctx.send(f'{role.mention} - Chain ending in {converted}')

    else:
        print(f'Time remaining: {converted}')

"""


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.command()
async def watch(ctx):
    global timeout
    global message_id
    print("Watch started")
    try:
        role = discord.utils.get(ctx.guild.roles, name=ROLE_NAME)

        message = await ctx.send(embed=countdown_embed)
        message_id = message.id
        await updateTimer()

        if timeout < 0:
            await ctx.send(f'{role.mention} - Chain ended')

        elif timeout < 180:
            converted = str(time.strftime('%M:%S', time.gmtime(timeout)))
            await ctx.send(f'{role.mention} - Chain ending in {converted}')


    except ValueError:
        print(f'No {ROLE_NAME} found')


@bot.command()
async def stop(ctx):
    print("Watch stopped")


"""
@bot.command()
async def start_watching(ctx):
    global check_task
    if check_task is None:
        check_task = check_timer.start(ctx)
        await ctx.send("Chain watch started!")
    else:
        await ctx.send("Chain watch already running!")
"""

"""
@bot.command()
async def stop_watching(ctx):
    global check_task
    if check_task:
        check_timer.stop()
        check_task = None
        await ctx.send("Watching stopped.")
    else:
        await ctx.send("Watching not running.")
        
"""
