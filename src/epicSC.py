from playwright.sync_api import sync_playwright
import json, requests

def Epic_Scraper():
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False, slow_mo=50)
            page = browser.new_page()
            page.goto("https://store.epicgames.com/en-US/free-games")
            page.wait_for_selector("data-testid=group-swiper-slider-titlebar")
            
            freeGameSection = page.locator("xpath=//*[contains(@class, 'css-2u323')]")
            titlesList =  []
            statusList =  []
            gameDict =  {}

            freeGameTitles = freeGameSection.locator("data-testid=direction-auto").count()
            for i in range(freeGameTitles):
                titles = freeGameSection.locator("data-testid=direction-auto").nth(i).text_content()
                titlesList.append(titles)

            freeGameStatus = freeGameSection.locator("div[class=css-1avc5a3]").count()
            for i in range(freeGameStatus):
                status = freeGameSection.locator("div[class=css-1avc5a3]").nth(i).text_content()
                statusList.append(status)

            print(statusList)
            print(titlesList)
            browser.close()

            for titlesList, statusList in zip(titlesList, statusList):
                gameDict[titlesList] = statusList

            print(gameDict)

            freeNowList =  []
            comingSoonList=  []

            for freegameTitles, freeGameStatus in gameDict.items():
                if freeGameStatus == 'Free Now':
                    freeNowList.append(freegameTitles)
                elif freeGameStatus == 'Coming Soon':
                    comingSoonList.append(freegameTitles)

            print(freeNowList)
            print(comingSoonList)
        return freeNowList, comingSoonList
    except Exception as e:
        print(e)
        return [], []

def Epic_Json():
    try:
        response = requests.get("https://store-site-backend-static-ipv4.ak.epicgames.com/freeGamesPromotions?locale=en-US&country=US&allowCountries=US")
        freeGameData = json.loads(response.text)
        
        #pretty_json = json.dumps(freeGameData, indent=2)
        #print(pretty_json)
        return freeGameData
    except Exception as e:
        print(e)
