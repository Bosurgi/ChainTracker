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

timeout = 2
message_id = 0

# Cooldown for sending messages of 30 seconds
message_cooldown = 30

last_update_time = 0

countdown_embed = discord.Embed(title='Chain Watcher', description=f'Time left: ')


async def getTime(api_url):
    """It gets the timeout of the current chain using an API key provided"""
    chain_data = requests.get(api_url).json()
    return chain_data[CHAIN][TIMEOUT]


async def cooldown_send(ctx, message, cooldown):
    global last_update_time
    current_time = time.time()
    if current_time - last_update_time >= cooldown:
        await ctx.send(message)
        last_update_time = current_time


async def checkTimer(ctx):
    counter = 30

    time_remaining = await getTime(API_CALL)
    while time_remaining > 0:

        try:
            role = discord.utils.get(ctx.guild.roles, name=ROLE_NAME)

            if counter == 0:
                time_remaining = await getTime(API_CALL)
                counter = 30

            if time_remaining < 180:
                converted = time.strftime('%M:%S', time.gmtime(time_remaining))
                await cooldown_send(ctx, f'{role.mention} - Chain ending in {converted}', 20)

            await asyncio.sleep(1.5)
            time_remaining -= 1
            counter -= 1
            print(time.strftime('%M:%S', time.gmtime(time_remaining)))

        except ValueError:
            print(f'No {ROLE_NAME} found')

    await ctx.send(f'{role.mention} - Chain ended')


async def updateTimer(ctx, id_message):
    global timeout
    counter = 0
    # TODO: Reactivate this after testing
    timeout = await getTime(API_CALL)

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
            timeout = await getTime(API_CALL)

            # Resetting the counter
            counter = 0

    # Notify when timer reaches 0
    await cooldown_send(ctx, "Chain Ended!", 10)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.command()
async def watch(ctx):
    global timeout
    global message_id
    print("Watch started")
    timeout = await getTime(API_CALL)

    message = await ctx.send(embed=countdown_embed)
    message_id = message.id

    await asyncio.gather(updateTimer(ctx, message_id), checkTimer(ctx))


@bot.command()
async def stop(ctx):
    bot.loop.stop()
    print("Watch stopped")
