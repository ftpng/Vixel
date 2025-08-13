import discord
from discord.ext import commands

from vixlib import LIGHT_RED


class ErrorHandler(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.NotOwner) and ctx.command and ctx.command.name == "sync":
            await ctx.reply(
                embed=discord.Embed(
                    description=f"Hi **{ctx.author.name}**, you are not authorized to sync commands.",
                    color=LIGHT_RED
                )
            )
            return
        raise error
    
async def setup(client: commands.Bot) -> None:
    await client.add_cog(ErrorHandler(client))