from discord.ext import commands
from discord import app_commands, Interaction, File
import vixlib as lib 

from vixlib.render.rendering import render_bedwars_stats
from vixlib.helpers import fetch_player_info
from vixlib.logging import handle_slash_errors
from vixlib.views import ModesView


class Bedwars(commands.Cog):
    def __init__(self, client):
        self.client: commands.Bot = client

    @app_commands.command(name="bedwars", description="View a player's Bedwars stats.")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.choices(mode=lib.MODES)
    @app_commands.describe(player="The player you want to view.", mode="The mode you want to view")
    async def bedwars(
        self,
        interaction: Interaction,
        player: str = None,
        mode: str = 'Overall'
    ):
        await interaction.response.defer()
        try:
            uuid = await fetch_player_info(player, interaction)
            if uuid is None:
                return None
  
            await render_bedwars_stats(uuid, mode)
            await interaction.edit_original_response(
                attachments=[File(f"{lib.DIR}assets/imgs/bedwars.png")],
                view=ModesView(
                    interaction, interaction.user.id, uuid, mode, type='bedwars'
                )
            )

        except Exception as error:
            await handle_slash_errors(interaction, error)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(Bedwars(client))