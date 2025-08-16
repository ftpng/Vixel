from discord.ext import commands
from discord import app_commands, Interaction, Embed
from mcfetch import Player

from vixlib.utils import Linking, Session
from vixlib.api.hypixel import fetch_hypixel_player_data
from vixlib.api import MOJANG_CACHE
import vixlib as lib 


class Link(commands.Cog):
    def __init__(self, client):
        self.client: commands.Bot = client


    @app_commands.command(name="link", description="Link your account")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.describe(player="The player you want to link to")
    async def link(
        self, interaction: Interaction, player: str, 
    ):
        await interaction.response.defer()
        uuid = Player(player=player, requests_obj=MOJANG_CACHE).uuid
        if uuid is None:
            return await interaction.edit_original_response(
                content=f"**{player}** does not exist! Please provide a valid username."
            )            

        hypixel_data = await fetch_hypixel_player_data(uuid, cache=False)
        print(hypixel_data)
        response = Linking(interaction.user.id).link_player(
            str(interaction.user), hypixel_data, uuid
        )

        print(response)
        if response == 1:
            username = Player(player=uuid, requests_obj=MOJANG_CACHE).name
            await interaction.edit_original_response(
                content=f"Successfully linked to **{username}**"
            )

            has_active_session = Session(uuid).get_session()
            if has_active_session:
                return

            bedwars_data = hypixel_data.get("player", {}).get("stats", {}).get("Bedwars", {})
            Session(uuid).start_session(bedwars_data) 

        else:
            embed = Embed(
                title='Hypixel Discord Mismatch!', color=lib.LIGHT_RED,
                description='To link your account successfully, please make sure your Hypixel Discord connection matches your current Discord tag exactly.'
            )
            await interaction.edit_original_response(embed=embed)


    @app_commands.command(name="unlink", description="Unlink your account")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    async def unlink(self, interaction: Interaction):
        await interaction.response.defer()
        
        is_linked = Linking(interaction.user.id).unlink_player()
        if not is_linked:
            message = "You don't have an account linked! In order to link use **/link**!"
        else:
            message = "Successfully unlinked your account!"

        await interaction.edit_original_response(content=message)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(Link(client)) 