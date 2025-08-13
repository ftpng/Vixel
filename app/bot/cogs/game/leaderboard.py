from discord.ext import commands
from discord import app_commands, Interaction, File

import vixlib as lib
from vixlib.render.rendering import render_leaderboard
from vixlib.logging import handle_slash_errors
from vixlib.views import LeaderboardView


class Leaderboard(commands.Cog):
    def __init__(self, client):
        self.client: commands.Bot = client

    leaderboard = app_commands.Group(
        name="leaderboard", 
        description="Leaderboard related commands",
        allowed_contexts=app_commands.AppCommandContext(guild=True, dm_channel=True, private_channel=True),
        allowed_installs=app_commands.AppInstallationType(guild=True, user=True)
    )

    @leaderboard.command(name="bedwars", description="Shows the BedWars leaderboard")
    @app_commands.describe(mode="The mode you want to view.", type="The stats you want to view.")
    @app_commands.choices(
        mode=lib.MODES,
        type=lib.TYPES_LEADERBOARD
    )
    async def bedwars(self, interaction: Interaction, mode: str = 'Overall', type: str = 'Stars'):
        await interaction.response.defer()
        try:
            if type.lower() == 'stars' and mode.lower() != 'overall':
                mode = 'Overall'

            modes = next(c for c in lib.MODES if c.value.lower() == mode.lower())
            choice = next(c for c in lib.TYPES_LEADERBOARD if c.value.lower() == type.lower())

            data = await lib.fetch_polsu_bedwars_leaderboard(
                mode=modes.value,
                type_=choice.value,
                top=100
            )
            if data is None:
                return interaction.edit_original_response(
                    content=(
                        "An error has occurred while running your command, please try again!\n"
                        "If the issue persists, please report this to **Vixel's Dev Team**!"
                    )
                )
            
            await render_leaderboard(data, modes.name, choice.name)
            await interaction.edit_original_response(
                attachments=[File(f"{lib.DIR}assets/imgs/leaderboard.png")],
                view=LeaderboardView(
                    interaction, interaction.user.id, modes.value, choice.value, modes.name, choice.name
                )
            )
        
        except Exception as error:
            await handle_slash_errors(interaction, error) 

async def setup(client: commands.Bot) -> None:
    await client.add_cog(Leaderboard(client))
