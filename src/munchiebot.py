# MunchieBot
import discord, os
from dotenv import load_dotenv
from consoleheader import logo_format, info_layout
from views import PersistentViewBot
from messageformater import retrieve_current_games
load_dotenv()
logo_format()
info_layout()

TOKEN = os.getenv("TOKEN") #Add your own token here
CHANNEL_ID = os.getenv("CHANNEL_ID")  #Add your own channel ID here
bot = PersistentViewBot()

def run_bot():
    @bot.event
    async def on_ready():
        print(f"{bot.user} has connected to Discord!")
        try:
                synced = await bot.tree.sync()
                print(f"synced {len(synced)} command(s)")
        except Exception as e:
                print(e)
        print(retrieve_current_games())

    bot.run(TOKEN)