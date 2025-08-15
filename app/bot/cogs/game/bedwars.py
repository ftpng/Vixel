from discord.ext import commands
from discord import app_commands, Interaction, File
import vixlib as lib 

from vixlib.render.rendering import render_bedwars_stats
from vixlib.api.polsu import fetch_polsu_data
from vixlib.api.hypixel import fetch_hypixel_player_data
from vixlib.utils import fetch_player
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

        uuid = await fetch_player(player, interaction)
        if uuid is None:
            return None
  
        hypixel_data: dict = await fetch_hypixel_player_data(uuid, include_guild=True)
        polsu_data: dict = await fetch_polsu_data("ping", uuid=uuid)

        if not hypixel_data or not polsu_data:
            await interaction.edit_original_response(
                content=lib.ERROR_MESSAGE
            )
            return None

        await render_bedwars_stats(
            uuid, mode, hypixel_data, polsu_data
        )
        await interaction.edit_original_response(
            attachments=[File(f"{lib.DIR}assets/imgs/bedwars.png")],
            view=ModesView(
                interaction, interaction.user.id, uuid, mode, hypixel_data, polsu_data, type='bedwars', 
            )
        )        

async def setup(client: commands.Bot) -> None:
    await client.add_cog(Bedwars(client))