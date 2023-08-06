import discord
from epicSC import Epic_Scraper
from epicSC import Epic_Json
import calendar

freeGameData = Epic_Json()
freeNowList, comingSoonList = Epic_Scraper()

def date_converter():
    date_List = []
    for time in freeGameData["data"]["Catalog"]["searchStore"]["elements"]:
        if time["title"] in freeNowList:
            gameDates = time["promotions"]["promotionalOffers"][0]["promotionalOffers"][0]["endDate"]
            gameYear = (gameDates[0:4])
            gameDay = (gameDates[8:10])

            if int(gameDates[6]) == 0:
                gameMonth = int(gameDates[7])
            else:
                gameMonth = int(gameDates[6:7])

            gameMonthName = calendar.month_name[gameMonth]
    
            formatedDate = str(f"{gameMonthName} {gameDay}, {gameYear}")
            date_List.append(formatedDate)

    return date_List

def retrieve_current_games():
    messages_List = []
    for games in freeGameData["data"]["Catalog"]["searchStore"]["elements"]:
        if games["title"] in freeNowList:
            messageFormat = discord.Embed(
                colour = discord.Colour.pink(),
                title = games["title"],
                description = games["description"],
            )

            messageFormat.set_author(name="Free On EpicGames[x]",url="https://store.epicgames.com/en-US/")
            messageFormat.add_field(name="",value="", inline=False)
            messageFormat.add_field(name="Original Price:", value=games["price"]["totalPrice"]["fmtPrice"]["originalPrice"], inline=True)
            messageFormat.add_field(name="Sale Ends:", value=date_converter()[0])
            messageFormat.set_thumbnail(url=games["keyImages"][2]["url"])

            messages_List.append(messageFormat)
    return messages_List

def current_games_ephemeral():
    messageFormat = discord.Embed(
        colour = discord.Colour.pink(),
        title = "The current free games are:",
    )
    messageFormat.set_author(name="Free On EpicGames[x]",url="https://store.epicgames.com/en-US/")
    for games in freeGameData["data"]["Catalog"]["searchStore"]["elements"]:
        if games["title"] in freeNowList:
            messageFormat.add_field(name=games["title"], value=games["description"])
            messageFormat.add_field(name="Original Price:", value=games["price"]["totalPrice"]["fmtPrice"]["originalPrice"], inline=True)
            messageFormat.add_field(name="Sale Ends:", value=date_converter()[0], inline=True)
    return messageFormat

def helper():
    commandList = discord.Embed(
    colour = discord.Colour.dark_purple(),
    title = "Commands",
    )
    commandList.set_author(name="Munchie Bot >^.^<")
    commandList.add_field(name="/help", value="See list of commands.", inline=False)
    commandList.add_field(name="/global", value="@everyone to notify the whole server.", inline=False)
    commandList.add_field(name="/freegame", value="See the latest free game on epic.", inline=False)
    commandList.add_field(name="/ilovemunchie", value="Tell Munchie how you feel about her.", inline=False)

    return commandList