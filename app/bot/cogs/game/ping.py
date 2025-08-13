from discord.ext import commands
from discord import app_commands, Interaction, Embed

from vixlib.logging import handle_slash_errors
from vixlib.helpers import fetch_player_info
from mcfetch import Player

import vixlib as lib 


class Ping(commands.Cog):
    def __init__(self, client):
        self.client: commands.Bot = client

    @app_commands.command(name="ping", description="View a players ping history")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.describe(player="The player you want to view.")
    async def ping(
        self,
        interaction: Interaction,
        player: str = None,
    ):
        await interaction.response.defer()
        try:
            uuid = await fetch_player_info(player, interaction)
            if uuid is None:
                return None

            response = await lib.fetch_polsu_player_ping(uuid)

            if not response.get("success") or "data" not in response:
                return await interaction.edit_original_response(
                    content=f"No ping history found for **{player}**."
                )

            data: dict = response["data"]
            stats = data.get("stats")
            history = data.get("history", [])

            player_name = Player(player=uuid, requests_obj=lib.CACHE).name

            if not stats:
                return await interaction.edit_original_response(
                    content=f"No ping stats found for **{player_name}**."
                )

            embed = Embed(
                title=f"Ping History For {player_name}",
                color=lib.EMBED_COLOR,
            )

            embed.add_field(name="Min", value=f"`{round(stats['min'])}ms`", inline=True)
            embed.add_field(name="Avg", value=f"`{round(stats['avg'])}ms`", inline=True)
            embed.add_field(name="Max", value=f"`{round(stats['max'])}ms`", inline=True)

            if history:
                history_sorted = sorted(history, key=lambda x: x["timestamp"], reverse=True)
                last_10 = history_sorted[:10]
                history_lines = [
                    f"- <t:{entry['timestamp']}:D> - `{round(entry['avg'])}ms`"
                    for entry in last_10
                ]
                embed.add_field(
                    name="Ping History",
                    value="\n".join(history_lines),
                    inline=False
                )
                embed.set_thumbnail(url=lib.HEAD_IMAGE + uuid + "/64")
            else:
                embed.add_field(name="Ping History", value="No history found.", inline=False)

            
            await interaction.edit_original_response(embed=embed)

        except Exception as error:
            await handle_slash_errors(interaction, error)


async def setup(client: commands.Bot) -> None:
    await client.add_cog(Ping(client))