# This example requires the 'message_content' privileged intents

import os
import discord
from discord.ext import commands
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
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))
ROLE_NAME = 'Wrath'
ATTACKS = 'current'
CHAIN = 'chain'
TIMEOUT = 'timeout'

timeout = 180
message_id = 0

countdown_embed = discord.Embed(title='Chain Watcher', description=f'Time left: ')


async def getTime(api_url):
    """It gets the timeout of the current chain using an API key provided"""
    chain_data = requests.get(api_url).json()
    return chain_data[CHAIN][TIMEOUT]


async def checkTimer(ctx, remaining_time):
    while remaining_time > 0:
        try:
            role = discord.utils.get(ctx.guild.roles, name=ROLE_NAME)

            if remaining_time < 180:
                converted = time.strftime('%M:%S', time.gmtime(remaining_time))
                await ctx.send(f'{role.mention} - Chain ending in {converted}')

            await asyncio.sleep(1)
            remaining_time -= 1

        except ValueError:
            print(f'No {ROLE_NAME} found')

    await ctx.send(f'{role.mention} - Chain ended')


async def updateTimer(ctx, id_message):
    global timeout
    counter = 0
    # TODO: Reactivate this after testing
    # timeout = getTime(API_CALL)

    while timeout > 0:
        # Converting seconds to minutes and seconds remaining
        countdown_minutes = timeout // 60
        countdown_seconds_remaining = timeout % 60
        countdown_embed.description = f'Time left: {countdown_minutes:02}:{countdown_seconds_remaining:02}'

        message = await bot.get_channel(CHANNEL_ID).fetch_message(id_message)
        await message.edit(embed=countdown_embed)

        # Wait one second and updating the seconds timer
        await asyncio.sleep(1)
        # countdown_seconds -= 1
        timeout -= 1
        # countdown_seconds_remaining -= 1
        counter += 1

    # After 30 seconds update the timeout making an API Call
        if counter >= 30:
            # TODO: Reactivate this after testing offline
            # countdown_seconds = getTime(API_CALL)

            # Resetting the counter
            counter = 0

    # Notify when timer reaches 0
    await ctx.send("Chain ended!")


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.command()
async def watch(ctx):
    global timeout
    global message_id
    print("Watch started")

    message = await ctx.send(embed=countdown_embed)
    message_id = message.id

    await asyncio.gather(updateTimer(ctx, message_id), checkTimer(ctx, timeout))


@bot.command()
async def stop(ctx):
    # TODO: Implement a way to stop the Bot
    print("Watch stopped")
