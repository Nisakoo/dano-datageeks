import json
import math
import aiohttp
import asyncio
import pandas as pd


async def get_app_info(session, appid: int) -> tuple:
    async with session.get(base_url.format(appid=appid)) as resp:
        data = json.loads(await resp.content.read())["query_summary"]
        return (
            appid,
            data["total_positive"],
            data["total_negative"],
            data["total_reviews"],
            data["review_score_desc"]
        )
    

reviews = pd.DataFrame(columns=["appid", "pos_reviews", "neg_reviews", "total_reviews", "review_score_desc"])

async def main(appids: list[float]):
    global reviews

    async with aiohttp.ClientSession() as session:
        
        counter = 1
        for appid in appids:
            if not math.isnan(appid):
                data = await get_app_info(session, int(appid))

                if not (data is None):
                    reviews.loc[len(reviews.index)] = data

                print(counter, data)
                counter += 1
    

base_url = "https://store.steampowered.com/appreviews/{appid}?json=1"

df = pd.read_csv("T_games_steam_appids.csv")

try:
    asyncio.run(main(df.appid))
finally:
    reviews.to_csv("games_info.csv", index=False)