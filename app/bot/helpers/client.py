import os
import discord
from discord.ext import commands
from vixlib.api.polsu import close_all_sessions, init_sessions
from vixlib.api.hypixel import close_hypixel_session, init_hypixel_session

intents = discord.Intents.all()
intents.message_content = True


class Client(commands.AutoShardedBot):
    def __init__(self, *, intents: discord.Intents = intents):           

        super().__init__(
            intents=intents,
            command_prefix=commands.when_mentioned_or('vix$')
        )


    async def setup_hook(self):
        await init_sessions()
        await init_hypixel_session()

        for folder in os.listdir("app/bot/cogs"):
            for cog in os.listdir(f"app/bot/cogs/{folder}"):
                if cog.endswith(".py"):
                    try:
                        await self.load_extension(name=f"app.bot.cogs.{folder}.{cog[:-3]}")
                        print(f"Loaded: {cog[:-3]} cog")

                    except commands.errors.ExtensionNotFound:
                        print(f"Failed to load {cog[:-3]}")      


    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})\n{50 * "-"}')


    async def close(self):
        await close_hypixel_session()
        await close_all_sessions()
        await super().close()