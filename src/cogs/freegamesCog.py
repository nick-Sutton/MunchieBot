import discord, aiofiles, json, calendar
from discord.ext import commands
from discord import app_commands
from view import PaginationView

class FreeGamesCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="freegame", description="See the latest free game on Epic")
    async def FreeGameCog(self, interaction: discord.Interaction):
        async with aiofiles.open("freeNow.txt", "r") as file:
            freeNowList = [line.strip() for line in await file.readlines()]
            print(freeNowList)

        async with aiofiles.open("free_games.json", "r") as file:
            getData = await file.read()
            freeGameJson = json.loads(getData)

        for time in freeGameJson["data"]["Catalog"]["searchStore"]["elements"]:
            if time["title"] in freeNowList[0]:
                gameDates = time["promotions"]["promotionalOffers"][0]["promotionalOffers"][0]["endDate"]
                gameYear = (gameDates[0:4])
                gameDay = (gameDates[8:10])

                #Determines if the Month value is single digit or multiple digits
                if int(gameDates[5]) == 0:
                    gameMonth = int(gameDates[6])
                else:
                    gameMonth = (gameDates[5]) + (gameDates[6])

                #Changes the month int to the calender month
                gameMonthName = calendar.month_name[int(gameMonth)]
        
                #Creates a string containing Month Day, Year
                formatedDate = str(f"{gameMonthName} {gameDay}, {gameYear}")

        messages_List = []
        for games in freeGameJson["data"]["Catalog"]["searchStore"]["elements"]:
            if games["title"] in freeNowList:
                messageFormat = discord.Embed(
                    colour = discord.Colour.pink(),
                    title = games["title"],
                    description = games["description"],
                )

                messageFormat.set_author(name="Free On EpicGames[->]",url="https://store.epicgames.com/en-US/free-games")
                messageFormat.add_field(name="",value="", inline=False)
                messageFormat.add_field(name="Original Price:", value=games["price"]["totalPrice"]["fmtPrice"]["originalPrice"], inline=True)
                messageFormat.add_field(name="Sale Ends:", value=formatedDate)
                messageFormat.set_thumbnail(url=games["keyImages"][2]["url"])

                messages_List.append(messageFormat)

        embeds = messages_List
        view = PaginationView(embeds)
        await interaction.response.send_message(embed=view._initial, view=view, ephemeral=False)

async def setup(bot:commands.Bot) -> None:
    await bot.add_cog(FreeGamesCog(bot))
