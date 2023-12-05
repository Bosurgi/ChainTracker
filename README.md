---
Title: Chain Watcher for Torn City
Description: A Discord bot written in Python for supporting players of Torn City - Browser game
Tags:
  - python
  - discord.py
---
![image](https://github.com/Bosurgi/ChainTracker/assets/87176210/0aecd28d-5c6d-42eb-8283-a4b11ca5bac4)


# Project description
This bot is designed to help users to keep track of the Chain timers.
It will show a timer on the selected channel which uses Torn API to fetch the timeout of the chain.
Just before the chain dies it will notify the users of a specific group in order to keep the chain alive.

# Bot Template

This example starts a Discord bot using [discord.py](https://discordpy.readthedocs.io/en/stable/).

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template/PxM3nl)

The Watcher is currently deployed using Railway.
Manually configure to go live each time changes are applied on main repository.

## ✨ Features
1. Uses Discord.py
2. Uses Torn API calls (limited to 30 seconds)
3. Creates a timer
4. Notifies users
5. Cooldown function between messages

## 💁‍♀️ How to use

- Install packages using `pip install -r requirements.txt`
- Create a ```.env``` file containing Discord Token, Channel Key and User Roles ID.
- Start the bot using `python main.py`

## 📝 Notes

This is a basic bot with the prefix `!`, more information can be founded at their [offical documentation](https://discordpy.readthedocs.io/en/stable/api.html).
