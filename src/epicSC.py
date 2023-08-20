from playwright.async_api import async_playwright
import json, aiohttp, aiofiles, time, os, calendar, discord
from discord.ext import commands, tasks
from discordviews import PaginationView

class BackgroundTasks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.Epic_Scraper.start()
        self.Epic_Json.start()
    
    def cog_unload(self) -> None:
        self.Epic_Scraper.stop()
        self.Epic_Json.stop()

    @tasks.loop(hours=12)
    async def Epic_Scraper(self):
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=False, slow_mo=50)
                page = await browser.new_page()
                await page.goto("https://store.epicgames.com/en-US/free-games", timeout=0)
                time.sleep(5)
                await page.wait_for_selector("data-testid=group-swiper-slider-titlebar")
                
                freeGameSection = page.locator("xpath=//*[contains(@class, 'css-2u323')]")
                titlesList =  []
                statusList =  []
                gameDict =  {}

                freeGameTitles = await freeGameSection.locator("data-testid=direction-auto").count()
                for i in range(freeGameTitles):
                    titles = await freeGameSection.locator("data-testid=direction-auto").nth(i).text_content()
                    titlesList.append(titles)

                freeGameStatus = await freeGameSection.locator("div[class=css-1avc5a3]").count()
                for i in range(freeGameStatus):
                    status = await freeGameSection.locator("div[class=css-1avc5a3]").nth(i).text_content()
                    statusList.append(status)

                await browser.close()

                for titlesList, statusList in zip(titlesList, statusList):
                    gameDict[titlesList] = statusList

                freeNowList =  []
                comingSoonList=  []

                for freegameTitles, freeGameStatus in gameDict.items():
                    if freeGameStatus == 'Free Now':
                        freeNowList.append(freegameTitles)
                    elif freeGameStatus == 'Coming Soon':
                        comingSoonList.append(freegameTitles)

            current_time = time.strftime("%H:%M:%S", time.localtime())
            print(f"\033[1m{current_time}\033[0m freeNowList and comingSoonList lists were successfully created.")

            freeNowFile = "freeNow.txt"
            async with aiofiles.open("freeNow.txt", "r") as file:
                freeNowtxt = [line.strip() for line in await file.readlines()]
                if freeNowtxt != freeNowList:
                    async with aiofiles.open(freeNowFile, "w") as file:
                            for line in freeNowList:
                                await file.write(f"{line}\n")
                    print(f"\033[1m{current_time}\033[0m Site data has changed.")
                    print(f"\033[1m{current_time}\033[0m Site data was successfully dumped.")

                    async with aiofiles.open("freeNow.txt", "r") as file:
                        freeNowAuto = [line.strip() for line in await file.readlines()]
                        print(freeNowList)

                    async with aiofiles.open("free_games.json", "r") as file:
                        getData = await file.read()
                        jsonAuto = json.loads(getData)

                    #Compares the Json dict and freeGamesList inorder to find the games located in the freeGameList
                    messages_List = []
                    for games in jsonAuto["data"]["Catalog"]["searchStore"]["elements"]:
                        if games["title"] in freeNowAuto:
                            #Creates an individual embed discord message for each game in the freeGamesList
                            messageFormat = discord.Embed( 
                                colour = discord.Colour.pink(),
                                title = games["title"],
                                description = games["description"],
                            )

                            messageFormat.set_author(name="Free On EpicGames[x]",url="https://store.epicgames.com/en-US/")
                            messageFormat.add_field(name="",value="", inline=False)
                            messageFormat.add_field(name="Original Price:", value=games["price"]["totalPrice"]["fmtPrice"]["originalPrice"], inline=True)
                            messageFormat.add_field(name="Sale Ends:", value=time)
                            messageFormat.set_thumbnail(url=games["keyImages"][2]["url"])

                            messages_List.append(messageFormat)

                    embeds = messages_List
                    view = PaginationView(embeds)

                    CHANNEL_ID = os.getenv("CHANNEL_ID")
                    message_channel = await self.bot.fetch_channel(CHANNEL_ID)
                    await message_channel.send("@everyone", embed=view._initial, view=view)

                else:
                    async with aiofiles.open(freeNowFile, "w") as file:
                        for line in freeNowList:
                            await file.write(f"{line}\n")
                    print(f"\033[1m{current_time}\033[0m Site data was successfully dumped.")

        except Exception as e:
            print(e)

    @tasks.loop(hours=12)
    async def Epic_Json(self):
        try:
            async with aiohttp.ClientSession() as session:
                response = await session.get("https://store-site-backend-static-ipv4.ak.epicgames.com/freeGamesPromotions?locale=en-US&country=US&allowCountries=US")
                responseText = await response.text()
                freeGameJson = json.loads(responseText)

                epicJson = "free_games.json"
                async with aiofiles.open(epicJson, "w") as file:
                    await file.write(json.dumps(freeGameJson, indent=4))
                    
                current_time = time.strftime("%H:%M:%S", time.localtime())
                print(f"\033[1m{current_time}\033[0m JSON data was successfully dumped.")

        except Exception as e:
            print(e)
        
async def setup(bot:commands.Bot) -> None:
    await bot.add_cog(BackgroundTasks(bot))
