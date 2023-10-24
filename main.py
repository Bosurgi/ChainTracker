import tracker
import os

# Running the bot
if __name__ == '__main__':
    tracker.bot.run(os.environ["DISCORD_TOKEN"])
