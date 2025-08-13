import json
import asyncio

from vixlib.api import fetch_polsu_bedwars_leaderboard


async def save_polsu_leaderboards_to_file(filename="bedwars_leaderboards.json"):
    data = await fetch_polsu_bedwars_leaderboard(
        mode="Overall",
        type_="final_kills",
        top="100"
    )
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


asyncio.run(save_polsu_leaderboards_to_file())