import discord
from discord import Interaction
from mcfetch import Player

import vixlib as lib
from vixlib.render.rendering import render_leaderboard

class NavButton(discord.ui.Button):
    def __init__(self, label: str, direction: str, disabled: bool):
        super().__init__(
            style=discord.ButtonStyle.gray,
            label=label,
            custom_id=f"nav_{direction}",
            disabled=disabled
        )
        self.direction = direction

    async def callback(self, interaction: Interaction):
        if not interaction.response.is_done():
            await interaction.response.defer()

        view: LeaderboardView = self.view
        if self.direction == "left":
            if view.current_page > 1:
                view.current_page -= 1

        elif self.direction == "right":
            if view.current_page < view.total_pages:
                view.current_page += 1

        await view.update_page(interaction)


class PageDisplay(discord.ui.Button):
    def __init__(self, current_page: int, total_pages: int):
        label = f"Page {current_page}/{total_pages}"
        super().__init__(
            style=discord.ButtonStyle.gray,
            label=label,
            custom_id="page_display",
            disabled=False
        )
        self.current_page = current_page
        self.total_pages = total_pages

    async def callback(self, interaction: Interaction):
        await interaction.response.send_modal(PageInputModal(self.view))


class SearchPlayer(discord.ui.Button):
    def __init__(self):
        super().__init__(
            style=discord.ButtonStyle.gray,
            label="🔍",
            custom_id="search_player",
            disabled=False
        )

    async def callback(self, interaction: Interaction):
        await interaction.response.send_modal(SearchPlayerModal(self.view))


class LeaderboardView(discord.ui.View):
    def __init__(
        self,
        interaction: Interaction,
        org_user: int,
        mode_value: str,
        type_value: str,
        mode_name: str,
        type_name: str,
        current_page: int = 1,
        total_pages: int = 10,
        timeout: int = 180
    ):
        super().__init__(timeout=timeout)
        self.current_page = current_page
        self.total_pages = total_pages
        self.org_user = org_user
        self.mode_value = mode_value
        self.type_value = type_value
        self.mode_name = mode_name
        self.type_name = type_name
        self.interaction = interaction
        self.update_buttons()

    def update_buttons(self):
        self.clear_items()
        self.add_item(NavButton("◀", "left", self.current_page == 1))
        self.add_item(PageDisplay(self.current_page, self.total_pages))
        self.add_item(NavButton("▶", "right", self.current_page == self.total_pages))
        self.add_item(SearchPlayer())

    async def update_page(self, interaction: Interaction):
        self.update_buttons()

        data = await lib.fetch_polsu_bedwars_leaderboard(
            mode=self.mode_value, 
            type_=self.type_value, 
            top=100
        )  
        
        await render_leaderboard(data, mode=self.mode_name, type=self.type_name, page=self.current_page)

        attachment = [discord.File(f"{lib.DIR}assets/imgs/leaderboard.png")]

        await interaction.edit_original_response(content='', attachments=attachment, view=self)


    async def interaction_check(self, interaction: Interaction):
        if self.org_user == 0:
            return True
        if interaction.user.id != self.org_user:
            await interaction.response.send_message(
                content=f"That message doesn't belong to you. You must run this command to interact with it.",
                ephemeral=True
            )
            return False
        return True

    async def on_timeout(self):
        self.clear_items()
        await self.interaction.edit_original_response(view=None)        


class PageInputModal(discord.ui.Modal, title="Jump to Page"):
    page_input = discord.ui.TextInput(
        label="Enter a page number",
        style=discord.TextStyle.short,
        placeholder="e.g. 3",
        required=True,
        min_length=1,
        max_length=3
    )

    def __init__(self, view: LeaderboardView):
        super().__init__()
        self._view = view

    async def on_submit(self, interaction: Interaction):
        if not interaction.response.is_done():
            await interaction.response.defer()

        if not await self._view.interaction_check(interaction):
            return

        try:
            page = int(self.page_input.value)
        except ValueError:
            await interaction.followup.send(
                f"That's not a valid number.",
                ephemeral=True
            )
            return

        if not (1 <= page <= self._view.total_pages):
            await interaction.followup.send(
                f"Page must be between 1 and {self._view.total_pages}.",
                ephemeral=True
            )
            return

        if page == self._view.current_page:
            await interaction.followup.send(
                f"You're already on page {page}.",
                ephemeral=True
            )
            return

        self._view.current_page = page
        await self._view.update_page(interaction)


class SearchPlayerModal(discord.ui.Modal, title="Find Player"):
    player_input = discord.ui.TextInput(
        label="Enter player's name",
        style=discord.TextStyle.short,
        placeholder="e.g. Ventros",
        required=True,
        min_length=1,
        max_length=16
    )

    def __init__(self, view: LeaderboardView):
        super().__init__()
        self._view = view

    async def on_submit(self, interaction: Interaction):
        if not interaction.response.is_done():
            await interaction.response.defer()

        if not await self._view.interaction_check(interaction):
            return

        player = self.player_input.value.strip()

        data = await lib.fetch_polsu_bedwars_leaderboard(
            mode=self._view.mode_value, 
            type_=self._view.type_value, 
            top=100
        )
        new_page, pos = await lib.get_leaderboard_page(data, player)
        
        if new_page is None or pos is None:
            uuid = Player(player=player, requests_obj=lib.CACHE).uuid
            if not uuid:
                return await interaction.followup.send(
                    f"**{player}** does not exist! Please provide a valid username.", ephemeral=True)

            else:
                return await interaction.followup.send(
                    f"**{player}** was not found on the leaderboard.", ephemeral=True)

        self._view.current_page = new_page
        self._view.update_buttons()

        await render_leaderboard(
            data, 
            mode=self._view.mode_name, 
            type=self._view.type_name, 
            page=new_page, 
            pos=pos
        )
        attachment = [discord.File(f"{lib.DIR}assets/imgs/leaderboard.png")]
        await interaction.edit_original_response(content='', attachments=attachment, view=self._view)