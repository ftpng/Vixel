from discord.ext import commands
from discord import app_commands, Interaction, File
import vixlib as lib 
from mcfetch import Player

from vixlib.render.rendering import render_session_stats
from vixlib.api.hypixel import fetch_hypixel_player_data
from vixlib.utils import fetch_player, Linking, Session
from vixlib.views import ModesView


class SessionBedwars(commands.Cog):
    def __init__(self, client):
        self.client: commands.Bot = client

    session = app_commands.Group(
        name="session", 
        description="Session related commands",
        allowed_contexts=app_commands.AppCommandContext(guild=True, dm_channel=True, private_channel=True),
        allowed_installs=app_commands.AppInstallationType(guild=True, user=True)
    )

    @session.command(name="bedwars", description="View your bedwars session stats.")
    @app_commands.describe(player="The username of the player", mode="The mode you want to view",)
    @app_commands.choices(mode=lib.MODES)
    async def session_bedwars(
        self, 
        interaction: Interaction, 
        player: str = None,
        mode: str = 'Overall'    
    ):
        await interaction.response.defer()

        is_linked = Linking(interaction.user.id).get_linked_player_uuid()
        if is_linked is None:
            return await interaction.edit_original_response(
                content="You don't have an account linked! In order to view sessions use **/link**!"
            )    

        uuid = await fetch_player(player, interaction)
        if uuid is None:
            return None


        hypixel_data = await fetch_hypixel_player_data(uuid, include_guild=True)

        has_session = Session(uuid).get_session()
        if not has_session:
            bedwars_data = hypixel_data.get("player", {}).get("stats", {}).get("Bedwars", {})
            Session(uuid).start_session(bedwars_data)           


        await render_session_stats(uuid, mode, hypixel_data)
        await interaction.edit_original_response(
            attachments=[File(f"{lib.DIR}assets/imgs/session.png")],
            view=ModesView(
                interaction, interaction.user.id, uuid, mode, hypixel_data, type='session'
            )
        )        


    @session.command(name="reset", description="Reset your bedwars session stats.")
    async def reset(self, interaction: Interaction):
        await interaction.response.defer()

        uuid = Linking(interaction.user.id).get_linked_player_uuid()
        if uuid is None:
            return await interaction.edit_original_response(
                content="You don't have an account linked! In order to reset sessions use **/link**!"
            )
            
        hypixel_data = await fetch_hypixel_player_data(uuid, cache=False)
        bedwars_data = hypixel_data.get("player", {}).get("stats", {}).get("Bedwars", {})

        Session(uuid).start_session(bedwars_data)

        await interaction.edit_original_response(
            content="Successfully reset your session stats."
        )
                  
async def setup(client: commands.Bot) -> None:
    await client.add_cog(SessionBedwars(client))