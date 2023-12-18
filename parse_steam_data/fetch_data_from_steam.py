import json
import math
import aiohttp
import asyncio
import pandas as pd


def in_steam(x):
    return not math.isnan(x)


async def get_app_info(session, appid: int) -> tuple:
    async with session.get(base_url, params={"appids": appid}) as resp:
        data = json.loads(await resp.content.read())
        if not (data is None):
            data = data[str(appid)]
            if "data" in data:
                data = data["data"]
                has_dlc = ("dlc" in data)
                
                if has_dlc:
                    dlc = data["dlc"]
                else:
                    dlc = "null"

                return (
                    appid,
                    data["type"],
                    data["name"],
                    has_dlc,
                    dlc,
                    data["release_date"]["coming_soon"],
                    data["release_date"]["date"]
                )
    

# games_data = pd.DataFrame(columns=["appid", "type", "steam_name", "has_dlc", "dlc", "is_coming_soon", "release_date"])
games_data = pd.read_csv("games_info.csv")

async def main(appids: list[float]):
    global games_data

    async with aiohttp.ClientSession() as session:
        
        counter = 1
        for appid in appids:
            if not math.isnan(appid):
                data = await get_app_info(session, int(appid))

                if not (data is None):
                    games_data.loc[len(games_data.index)] = data

                print(counter, data)
                counter += 1
    

base_url = "https://store.steampowered.com/api/appdetails"

df = pd.read_csv("T_games_steam_appids.csv")
df["in_steam"] = df.appid.apply(in_steam)

try:
    asyncio.run(main(list(list(set(df.appid).difference(games_data.appid)))))
finally:
    games_data.to_csv("games_info.csv", index=False)