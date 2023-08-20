import discord, aiofiles, json, calendar, os
from discord.ext import commands
from discord import app_commands
from discordviews import PaginationView

class GlobalCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="global", description="@everyone' to notify the whole server")
    async def globalCog(self, interaction: discord.Interaction):
        #Reads the games stored in the freeNow.txt file and returns them as a list
        async with aiofiles.open("freeNow.txt", "r") as file:
            freeNowList = [line.strip() for line in await file.readlines()]
            print(freeNowList)
        #Reads the Json data stored in free_games.json and stores it as a dictionary
        async with aiofiles.open("free_games.json", "r") as file:
            getData = await file.read()
            freeGameJson = json.loads(getData)

        #Searche the json dict for a nested dict that has the same game title as the first title in the freegamesList
        for time in freeGameJson["data"]["Catalog"]["searchStore"]["elements"]:
            if time["title"] in freeNowList[0]:
                #breaks the json date foramt into Month/Day/Year format
                gameDates = time["promotions"]["promotionalOffers"][0]["promotionalOffers"][0]["endDate"]
                gameYear = (gameDates[0:4])
                gameDay = (gameDates[8:10])

                #Determines if the Month value is single digit or multiple digits
                if int(gameDates[6]) == 0:
                    gameMonth = int(gameDates[7])
                else:
                    gameMonth = int(gameDates[6:7])

                #Changes the month int to the calender month
                gameMonthName = calendar.month_name[gameMonth]
        
                #Creates a string containing Month Day, Year
                formatedDate = str(f"{gameMonthName} {gameDay}, {gameYear}")

        #Compares the Json dict and freeGamesList inorder to find the games located in the freeGameList
        messages_List = []
        for games in freeGameJson["data"]["Catalog"]["searchStore"]["elements"]:
            if games["title"] in freeNowList:
                #Creates an individual embed discord message for each game in the freeGamesList
                messageFormat = discord.Embed( 
                    colour = discord.Colour.pink(),
                    title = games["title"],
                    description = games["description"],
                )

                messageFormat.set_author(name="Free On EpicGames[x]",url="https://store.epicgames.com/en-US/")
                messageFormat.add_field(name="",value="", inline=False)
                messageFormat.add_field(name="Original Price:", value=games["price"]["totalPrice"]["fmtPrice"]["originalPrice"], inline=True)
                messageFormat.add_field(name="Sale Ends:", value=formatedDate)
                messageFormat.set_thumbnail(url=games["keyImages"][2]["url"])

                messages_List.append(messageFormat)

        embeds = messages_List
        view = PaginationView(embeds)
        #possibly add auto send statment here
        await interaction.response.send_message("@everyone", embed=view._initial, view=view, ephemeral=False)

async def setup(bot:commands.Bot) -> None:
    await bot.add_cog(GlobalCog(bot))

