from mcfetch import Player
from discord import Interaction

from .linking import Linking
from vixlib.api import MOJANG_CACHE


async def fetch_player(
    player: str,
    interaction: Interaction
) -> str | None:
    if player is None:
        uuid = Linking(interaction.user.id).get_linked_player_uuid()
        if not uuid:
            if interaction.response.is_done():
                await interaction.edit_original_response(
                    content="You are not linked! Either specify a player or link your account using **/link**!"
                )
                return None
        
    else:
        uuid = Player(
            player=player, requests_obj=MOJANG_CACHE).uuid
        
        if uuid is None:
            await interaction.edit_original_response(
                content=f"**{player}** does not exist! Please provide a valid username."
            ) 
            return None
        
    return uuid