import os
import logging
import discord
from discord.ext import commands

logger = logging.getLogger(__name__)

intents = discord.Intents.all()
intents.message_content = True


class Client(commands.AutoShardedBot):
    def __init__(self, *, intents: discord.Intents = intents):           

        super().__init__(
            intents=intents,
            command_prefix=commands.when_mentioned_or('vox$')
        )


    async def setup_hook(self):
        for folder in os.listdir("app/bot/cogs"):
            for cog in os.listdir(f"app/bot/cogs/{folder}"):
                if cog.endswith(".py"):
                    try:
                        await self.load_extension(name=f"app.bot.cogs.{folder}.{cog[:-3]}")
                        logger.info(f"Loaded: {cog[:-3]} cog")

                    except commands.errors.ExtensionNotFound:
                        logger.warning(f"Failed to load {cog[:-3]}")      


    async def on_ready(self):
        logger.info(f'Logged in as {self.user} (ID: {self.user.id})\n{50 * "-"}')