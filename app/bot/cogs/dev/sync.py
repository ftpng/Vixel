import discord
from discord.ext import commands
from vixlib import LIGHT_RED, LIGHT_GREEN

import logging
logger = logging.getLogger(__name__)


class Sync(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
    
    @commands.command(name="sync")
    @commands.is_owner()
    async def sync_command(self, ctx: commands.Context):
        try:
            await self.client.tree.sync()
            await ctx.reply(
                embed=discord.Embed(
                    description=f"`✅` Done syncing!",
                    color=LIGHT_GREEN
                )
            )
        except Exception:
            await ctx.reply(
                embed=discord.Embed(
                    description=f"Failed to sync commands.",
                    color=LIGHT_RED
                )
            )

async def setup(client: commands.Bot) -> None:
    await client.add_cog(Sync(client))