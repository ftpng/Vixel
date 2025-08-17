from discord.ext import commands
from discord import app_commands, Interaction, Embed

import vixlib as lib


class Invite(commands.Cog):
    def __init__(self, client):
        self.client: commands.Bot = client

    @app_commands.command(name="invite", description="Invite Vixel to your server",)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    async def invite(self, interaction: Interaction):
        await interaction.response.defer()

        embed = Embed(
            title="Invite Vixel",
            description=(
                f"To add Vixel to your server, click [here]({lib.INVITE})"
            ),
            color=lib.EMBED_COLOR,
        )
        embed.set_thumbnail(url=lib.LOGO)

        await interaction.edit_original_response(embed=embed)


async def setup(client: commands.Bot) -> None:
    await client.add_cog(Invite(client))