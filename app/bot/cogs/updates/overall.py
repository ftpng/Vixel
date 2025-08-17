import os
import json
from discord.ext import commands, tasks

from vixlib.api.polsu import fetch_polsu_data
import vixlib as lib


class BedwarsUpdatesOverall(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.update_message.start()

    @tasks.loop(minutes=5)
    async def update_message(self):
        try:

            mode = "overall"
            leaderboards = lib.BEDWARS_LEADERBOARDS[mode]

            for lb_key, lb_info in leaderboards.items():
                data = await fetch_polsu_data(
                    "leaderboard",
                    mode=mode,
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
                    old_leaderboard = []

                changes_list = []
                current_uuids = set()

                for player in new_players:
                    uuid = player["uuid"]
                    current_uuids.add(uuid)
                    new_pos = player["position"]
                    old_pos = old_players.get(uuid)

                    player_name = lib.format_name(player["formatted"])
                    value = player["value"]

                    if old_pos is None:
                        emoji = lib.GREEN_DOT
                        changes_list.append(
                            f"> {emoji} `{player_name}` entered leaderboard at `{new_pos}` "
                            f"*({lib.format_value(lb_key, value)} {lb_info['display_name']})*"
                        )
                    elif old_pos != new_pos:
                        emoji = lib.GREEN_DOT if new_pos < old_pos else lib.RED_DOT
                        changes_list.append(
                            f"> {emoji} `{player_name}` position updated: `{old_pos}` ➡ `{new_pos}` "
                            f"*({lib.format_value(lb_key, value)} {lb_info['display_name']})*"
                        )

                for old_player in old_leaderboard:
                    uuid = old_player["uuid"]
                    if uuid not in current_uuids:
                        player_name = lib.format_name(old_player["formatted"])
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
                        header = f"**{mode.title()} {lb_info['display_name']} Updates**\n"
                        max_length = 2000
                        chunk = header
                        for line in changes_list:
                            if len(chunk) + len(line) + 1 > max_length:
                                await channel.send(content=chunk)
                                chunk = header + line + "\n"
                            else:
                                chunk += line + "\n"
                        if chunk.strip():
                            await channel.send(content=chunk)

                with open(lb_info["path"], "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)

        except Exception as e:
            import traceback
            print(f"An error occurred in leaderboard overall updates: {e}")
            traceback.print_exc()

    def cog_unload(self):
        self.update_message.cancel()


async def setup(client: commands.Bot):
    await client.add_cog(BedwarsUpdatesOverall(client))