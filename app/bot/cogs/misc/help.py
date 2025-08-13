from discord.ext import commands
from discord import app_commands, Interaction, Embed

from vixlib.logging import handle_slash_errors

import vixlib as lib 


class Help(commands.Cog):
    def __init__(self, client):
        self.client: commands.Bot = client

    @app_commands.command(name="help", description="Displays Help")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    async def invite(self, interaction: Interaction):
        await interaction.response.defer()

        try:
            embed = Embed(
                title='Vixel Help',
                description=f"Need Support? Join our [Discord]({lib.SUPPORT_SERVER}) and create a ticket to directly contact us.",
                color=lib.EMBED_COLOR
            )
            embed.set_thumbnail(url=lib.LOGO)
            embed.add_field(
                name="Bedwars Stats",
                value=(
                    "Vixel supports detailed Bedwars stats from Hypixel. Use `/bedwars [player] [mode]` "
                    "to check a player's stats in different game modes like solos, doubles, or fours."
                ),
                inline=False
            )
            embed.add_field(
                name="Session Stats",
                value=(
                    "Track your current Bedwars session progress with `/session bedwars [player] [mode]`. "
                    "You can reset your session anytime using `/session reset`. Note: players must link "
                    "their Minecraft account with `/link` to use session commands."
                ),
                inline=False
            )
            embed.add_field(
                name="Leaderboards",
                value=(
                    "View top players in Bedwars via `/leaderboard [mode] [type]`. You can see rankings "
                    "based on stats like stars, wins, final kills, WLR, FKDR, beds broken, and more."
                ),
                inline=False
            )
            embed.add_field(
                name="Linking",
                value=(
                    "Link your Minecraft account to your Discord with `/link` to make commands easier—no "
                    "need to specify your player name each time. Linking also automatically starts your session. "
                    "Use `/unlink` to unlink your account when needed."
                ),
                inline=False
            )
            embed.add_field(
                name="Leaderboard Updates",
                value=(
                    "Stay up-to-date with top 100 Bedwars leaderboard changes every 15 minutes. "
                    "We track `overall`, `solos`, `doubles`, `threes`, `fours`, and `4v4` modes, highlighting position changes "
                    "based on `FKDR`, `KDR`, `WLR`, `BBLR`, `wins`, `losses`, `final kills` and everything else. "
                    f"These live updates are posted directly in our [Discord server]({lib.SUPPORT_SERVER}), "
                    "where you can join the community and follow the action closely."
                ),
                inline=False
            )
            await interaction.edit_original_response(embed=embed)
        
        except Exception as error:
            await handle_slash_errors(interaction, error)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(Help(client)) 