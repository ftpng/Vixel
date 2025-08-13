from discord.ext import commands
from discord import app_commands, Interaction, Embed

from vixlib.logging import handle_slash_errors

import vixlib as lib 


class Support(commands.Cog):
    def __init__(self, client):
        self.client: commands.Bot = client


    @app_commands.command(name="support", description="Join the support server")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    async def support(self, interaction: Interaction):
        await interaction.response.defer()

        try:
            embed = Embed(
                title='Support Server',
                description=f"Need assistance or found a bug you'd like to report?\nHop into our official [support server]({lib.SUPPORT_SERVER})!",
                color=lib.EMBED_COLOR
            )
            embed.set_thumbnail(url=lib.LOGO)
            await interaction.edit_original_response(embed=embed)
        
        except Exception as error:
            await handle_slash_errors(interaction, error)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(Support(client)) 