from playwright.async_api import async_playwright
import json, aiohttp, aiofiles, discord
from discord.ext import commands, tasks
from discord import app_commands

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
                await page.goto("https://store.epicgames.com/en-US/free-games")
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

                print(f"{titlesList} and {statusList} list were successfully created.")
                await browser.close()

                for titlesList, statusList in zip(titlesList, statusList):
                    gameDict[titlesList] = statusList

                print(f"gameDict{gameDict} was successfully created.")

                freeNowList =  []
                comingSoonList=  []

                for freegameTitles, freeGameStatus in gameDict.items():
                    if freeGameStatus == 'Free Now':
                        freeNowList.append(freegameTitles)
                    elif freeGameStatus == 'Coming Soon':
                        comingSoonList.append(freegameTitles)

            print(f"{freeNowList} and {comingSoonList} lists were successfully created.")

            freeNowFile = "freeNow.txt"
            async with aiofiles.open(freeNowFile, "w") as file:
                for line in freeNowList:
                    await file.write(f"{line}\n")
                    
                print("JSON data was successfully dumped.")

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
                    
                print("JSON data was successfully dumped.")

        except Exception as e:
            print(e)

    @app_commands.command(name="start", description="Starts Munchies automatic site checking")
    async def loop_start(self, interaction: discord.Integration):
        self.Epic_Scraper.start()
        self.Epic_Json.start()
    @app_commands.command(name="stop", description="Stops Munchies automatic site checking")
    async def loop_stop(self, interaction: discord.Integration):
        self.Epic_Scraper.stop()
        self.Epic_Json.stop()
        
async def setup(bot:commands.Bot) -> None:
    await bot.add_cog(BackgroundTasks(bot))
