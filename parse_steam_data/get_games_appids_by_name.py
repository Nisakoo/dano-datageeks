import aiohttp
import asyncio
import requests
from bs4 import BeautifulSoup
import pandas as pd


data = pd.DataFrame(columns=["name", "appid"])

async def main(names):
    base_url = "https://store.steampowered.com/search"
    batches = list()
    batches.append(names)
    # i = 0
    # batch = list()
    # for name in names:
    #     if i == 20:
    #         i = 0
    #         batches.append(batch)
    #         batch = list()
    #         batch.append(name)
    #     else:
    #         batch.append(name)
    #         i += 1

    async with aiohttp.ClientSession() as session:

        i = 0
        for batch in batches:
            for name in batch:
                async with session.get(base_url, params={"term": name}) as resp:
                    raw_html = await resp.content.read()
                    soup = BeautifulSoup(raw_html, "html.parser")
                    a = soup.find("a", class_="search_result_row", href=True)

                    print(i + 1, name, end=" ")
                    try:
                        href = a["href"].split("/")[4]
                    except:
                        href = "null"

                    data.loc[len(data.index)] = (name, href)

                    print(href)
                    i += 1


df = pd.read_csv("T_games_dataset.csv")
already_download = pd.read_csv("steam_games_appids_1.csv")
games = list(pd.unique(df.good_name))
ad_games = list(pd.unique(already_download.name))

games = ['Age of Wonders III',
 'Age of Wonders: Planetfall - Star Kings - DLC',
 'Ethan: Meteor Hunter',
 'G.I. Joe: Operation Blackout - Retro Skins Pack - DLC',
 'GRIP: Combat Racing - DeLorean 2650 - DLC',
 'Railway Empire - Japan - DLC',
 'SkyDrift: Gladiator Multiplayer Pack - DLC',
 'Tales of Tomorrow: Experiment',
 'Unmemory',
 'Warhammer 40,000: Battlesector']

try:
    asyncio.run(main(games))
finally:
    data.to_csv("steam_games_appids.csv")