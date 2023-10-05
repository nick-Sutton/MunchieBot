# MunchieBot
from settings import *
import discord, aiofiles
from discord.ext import commands

class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents().all()
        intents.message_content = True
        super().__init__(command_prefix=commands.when_mentioned_or('!'), intents=intents)
        self.cogs_List = ["cogs.freegamesCog", "cogs.globalCog", "cogs.helpCog", "epicSC"]

    async def setup_hook(self) -> None:
        for ext in self.cogs_List:
            await self.load_extension(ext)

    async def on_ready(self):
        try:
            print(f"\033[1m{self.user}\033[0m has connected to Discord!")
            synced = await self.tree.sync()
            print(f"synced {len(synced)} command(s)")
            await aiofiles.open("freeNow.txt", "a")
            async with aiofiles.open("freeNow.txt", "r") as file:
                  freeNowList = [line.strip() for line in await file.readlines()]
            
            freeNowStatus = " | ".join(freeNowList)
            await self.change_presence(status=discord.Status.online, activity=discord.Game(freeNowStatus))
        except Exception as e:
              print(e)

if __name__ == '__main__':
    bot = Bot()
    bot.run(TOKEN)