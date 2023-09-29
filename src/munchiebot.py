# MunchieBot
import discord, os, aiofiles
from dotenv import load_dotenv
from consoleheader import logo_format, info_layout
from view import ViewBot
load_dotenv()
logo_format()
info_layout()

TOKEN = os.getenv("TOKEN") #Add your own token here
CHANNEL_ID = os.getenv("CHANNEL_ID")  #Add your own channel ID here
bot = ViewBot()

@bot.event
async def on_ready():
        try:
                print(f"\033[1m{bot.user}\033[0m has connected to Discord!")
                synced = await bot.tree.sync()
                print(f"synced {len(synced)} command(s)")
                async with aiofiles.open("freeNow.txt", "r") as file:
                        freeNowList = [line.strip() for line in await file.readlines()]

                freeNowStatus = " | ".join(freeNowList)   
                await bot.change_presence(status=discord.Status.online, activity=discord.Game(freeNowStatus))
        except Exception as e:
                print(e)

bot.run(TOKEN)