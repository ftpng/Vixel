from discord import Interaction, SelectOption, File
from discord.ui import Select, View

from vixlib.render.rendering import render_bedwars_stats, render_session_stats
import vixlib as lib


class ModeSelector(Select):
    def __init__(self):
        options = [
            SelectOption(label="Overall"),
            SelectOption(label="Solos"),
            SelectOption(label="Doubles"),
            SelectOption(label="Threes"),
            SelectOption(label="Fours"),
            SelectOption(label="4v4"),
        ]
        super().__init__(
            placeholder="Select A Mode",
            max_values=1,
            min_values=1,
            options=options,
            custom_id="mode_selector_bedwars"
        )

    async def callback(self, interaction: Interaction):
        if not interaction.response.is_done():
            await interaction.response.defer()

        view: ModesView = self.view
        view.mode = self.values[0]
        await view.update_mode(interaction)


class ModesView(View):
    def __init__(
        self, 
        interaction: Interaction, 
        org_user: int,
        uuid: str,
        mode: str,
        hypixel_data: dict,
        polsu_data: dict = None,
        type: str = 'bedwars',
        timeout: int = 180
    ):
        super().__init__(timeout=timeout)
        self.org_user: int = org_user
        self.mode: str = mode
        self.interaction: Interaction = interaction  
        self.uuid: str = uuid
        self.type: str = type
        self.hyp_data: dict = hypixel_data
        self.polsu_data: dict = polsu_data

        self.add_item(ModeSelector())

    async def update_mode(self, interaction: Interaction):
        if self.type == 'bedwars':
            await render_bedwars_stats(self.uuid, self.mode, self.hyp_data, self.polsu_data)
            file = File(f"{lib.DIR}assets/imgs/bedwars.png")

            if interaction.user.id == self.org_user:
                await interaction.edit_original_response(
                    attachments=[file],
                    view=self
                )   
            else:
                await interaction.followup.send(file=file, ephemeral=True)            
        
        elif self.type == 'session':
            await render_session_stats(self.uuid, self.mode, self.hyp_data)
            file = File(f"{lib.DIR}assets/imgs/session.png")

            if interaction.user.id == self.org_user:
                await interaction.edit_original_response(
                    attachments=[file],
                    view=self
                )   
            else:
                await interaction.followup.send(file=file, ephemeral=True)           
        
    async def on_timeout(self):
        self.clear_items()
        await self.interaction.edit_original_response(view=None)