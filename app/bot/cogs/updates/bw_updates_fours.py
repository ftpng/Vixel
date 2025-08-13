import json
import os
from discord import HTTPException
from discord.ext import commands, tasks
from vixlib.render import Prestige
from vixlib.hypixel import Leveling
from mcfetch import Player
import vixlib as lib


BEDWARS_LEADERBOARDS_FOURS = {
    "winstreak": {
        "path": f"{lib.DIR}data/fours/bedwars_winstreak.json",
        "channel_id": lib.FOURS_WINSTREAK_CHANNEL,
        "display_name": "Winstreak"
    },
    "games_played": {
        "path": f"{lib.DIR}data/fours/bedwars_games.json",
        "channel_id": lib.FOURS_STATS_CHANNEL,
        "display_name": "Games Played"
    },
    "wins": {
        "path": f"{lib.DIR}data/fours/bedwars_wins.json",
        "channel_id": lib.FOURS_STATS_CHANNEL,
        "display_name": "Wins"
    },
    "losses": {
        "path": f"{lib.DIR}data/fours/bedwars_losses.json",
        "channel_id": lib.FOURS_STATS_CHANNEL,
        "display_name": "Losses"
    },
    "wlr": {
        "path": f"{lib.DIR}data/fours/bedwars_wlr.json",
        "channel_id": lib.FOURS_WLR_CHANNEL,
        "display_name": "WLR"
    },
    "kills": {
        "path": f"{lib.DIR}data/fours/bedwars_kills.json",
        "channel_id": lib.FOURS_STATS_CHANNEL,
        "display_name": "Kills"
    },
    "deaths": {
        "path": f"{lib.DIR}data/fours/bedwars_deaths.json",
        "channel_id": lib.FOURS_STATS_CHANNEL,
        "display_name": "Deaths"
    },
    "kdr": {
        "path": f"{lib.DIR}data/fours/bedwars_kdr.json",
        "channel_id": lib.FOURS_KDR_CHANNEL,
        "display_name": "KDR"
    },
    "final_kills": {
        "path": f"{lib.DIR}data/fours/bedwars_final_kills.json",
        "channel_id": lib.FOURS_STATS_CHANNEL,
        "display_name": "Final Kills"
    },
    "final_deaths": {
        "path": f"{lib.DIR}data/fours/bedwars_final_deaths.json",
        "channel_id": lib.FOURS_STATS_CHANNEL,
        "display_name": "Final Deaths"
    },
    "fkdr": {
        "path": f"{lib.DIR}data/fours/bedwars_fkdr.json",
        "channel_id": lib.FOURS_FKDR_CHANNEL,
        "display_name": "FKDR"
    },
    "beds_broken": {
        "path": f"{lib.DIR}data/fours/bedwars_beds_broken.json",
        "channel_id": lib.FOURS_STATS_CHANNEL,
        "display_name": "Beds Broken"
    },
    "beds_lost": {
        "path": f"{lib.DIR}data/fours/bedwars_beds_lost.json",
        "channel_id": lib.FOURS_STATS_CHANNEL,
        "display_name": "Beds Lost"
    },
    "bblr": {
        "path": f"{lib.DIR}data/fours/bedwars_bblr.json",
        "channel_id": lib.FOURS_BBLR_CHANNEL,
        "display_name": "BBLR"
    },
}

class BedwarsUpdatesFours(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.update_message.start()

    @tasks.loop(minutes=5)
    async def update_message(self):
        try:
            for lb_key, lb_info in BEDWARS_LEADERBOARDS_FOURS.items():
                data = await lib.fetch_polsu_bedwars_leaderboard(
                    mode="Fours",
                    type_=lb_key,
                    top="100"
                )
                if not data.get("success") or "data" not in data:
                    continue

                new_players = data["data"].get("leaderboard", [])
                if not new_players:
                    continue

                if os.path.exists(lb_info["path"]):
                    with open(lb_info["path"], "r", encoding="utf-8") as f:
                        old_data = json.load(f)
                    if isinstance(old_data, dict):
                        old_leaderboard = old_data.get("data", {}).get("leaderboard", [])
                    elif isinstance(old_data, list):
                        old_leaderboard = old_data
                    else:
                        old_leaderboard = []
                    old_players = {p['uuid']: p['position'] for p in old_leaderboard}
                else:
                    old_players = {}

                changes_list = []

                current_uuids = set()

                for player in new_players:
                    uuid = player["uuid"]
                    current_uuids.add(uuid)
                    new_pos = player["position"]
                    old_pos = old_players.get(uuid)

                    player_name = lib.format_lb_name(player["formatted"])
                    value = player["value"]

                    if old_pos is None:
                        emoji = lib.GREEN_DOT
                        changes_list.append(
                            f"> {emoji} `{player_name}` entered leaderboard at `{new_pos}` "
                            f"*({lib.format_value(lb_key, value)} {lb_info['display_name']})*"
                        )
                    elif old_pos != new_pos:
                        if new_pos < old_pos:
                            emoji = lib.GREEN_DOT
                        else:
                            emoji = lib.RED_DOT
                        changes_list.append(
                            f"> {emoji} `{player_name}` position updated: `{old_pos}` ➡ `{new_pos}` "
                            f"*({lib.format_value(lb_key, value)} {lb_info['display_name']})*"
                        )

                for old_player in old_leaderboard:
                    uuid = old_player["uuid"]

                    if uuid not in current_uuids:
                        player_name = lib.format_lb_name(old_player["formatted"])

                        value = old_player["value"]
                        old_pos = old_player["position"]
                        
                        emoji = lib.RED_DOT
                        changes_list.append(
                            f"> {emoji} `{player_name}` left the top 100 (Old position: `{old_pos}`) "
                            f"*({lib.format_value(lb_key, value)} {lb_info['display_name']})*"
                        )
                        
                if changes_list:
                    channel = self.client.get_channel(lb_info["channel_id"])
                    if channel:
                        header = f"**Fours {lb_info['display_name']} Updates**\n"
                        max_length = 2000
                        chunk = header
                        for line in changes_list:
                            if len(chunk) + len(line) + 1 > max_length:
                                try:
                                    await channel.send(content=chunk)
                                except HTTPException as e:
                                    print(f"Failed to send message chunk: {e}")
                                chunk = header + line + "\n"
                            else:
                                chunk += line + "\n"
                        if chunk.strip():
                            try:
                                await channel.send(content=chunk)
                            except HTTPException as e:
                                print(f"Failed to send message chunk: {e}")

                with open(lb_info["path"], "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)

        except Exception as e:
            import traceback
            print(f"An error occurred in leaderboard Fours updates: {e}")
            traceback.print_exc()

    def cog_unload(self):
        self.update_message.cancel()

async def setup(client: commands.Bot):
    await client.add_cog(BedwarsUpdatesFours(client))
