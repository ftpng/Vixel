from vixlib.render import BackgroundImageLoader, ImageRender, DisplayName, Prestige
from vixlib.hypixel import BedwarsStats, Leveling
from vixlib.render import DisplayName

import vixlib as lib


async def render_leaderboard(
    data: dict,
    mode: str, 
    type: str, 
    page: int = 1,
    pos: int = None
) -> None:
    
    if pos:
        bg = BackgroundImageLoader(
            dir="leaderboard/hl", 
            default_filename=f"pos_{pos}.png"
        )
    else:
        bg = BackgroundImageLoader(dir="leaderboard")

    im = ImageRender(bg.load_default_background())

    im.text.draw_many([
        (f'&f{mode} {type} Leaderboard', {'position': (413, 52)}),
        (f'&fPos', {'position': (76, 99)}),
        (f'&fPlayers', {'position': (368, 99)}),
        (f'&f{type}', {'position': (705, 99)}),
    ], default_text_options={
        "shadow_offset": (2, 2), "align": "center", "font_size": 20}
    )

    y = 146
    y_skin = 145
    entries_per_page = 10

    leaderboard = data.get("data", {}).get("leaderboard", [])

    start_index = (page - 1) * entries_per_page
    end_index = start_index + entries_per_page
    page_entries = leaderboard[start_index:end_index]

    for player in page_entries:
        player: dict 

        position = player.get("position")
        uuid = player.get("uuid")
        value = player.get("value")    

        color = {
            1: "&e",
            2: "&7",
            3: "&6"
        }.get(position, "&f")

        im.text.draw(f"{color}#{position}", text_options={
            "position": (76, y),
            "font_size": 20,
            "shadow_offset": (2, 2),
            "align": "center"
        })
        
        formatted_name = await lib.fetch_polsu_bedwars_formatted_name(uuid)
        displayname = lib.strip_minecraft_formatting(formatted_name["data"]["formatted"])

        im.text.draw(
            f"{displayname}", 
            text_options={
                "position": (160, y),
                "font_size": 18,
                "shadow_offset": (2, 2),
                "align": "left"
            }
        )

        im.text.draw(
            f"&f{lib.format_value(type, value)}", 
            text_options={
                "position": (705, y),
                "font_size": 18,
                "shadow_offset": (2, 2),
                "align": "center"
            }
        )

        await im.skin.paste_skin(
            uuid, position=(131, y_skin), size=(20, 20), style='face'
        )

        y += 46
        y_skin += 46

    im.save(f"{lib.DIR}assets/imgs/leaderboard.png")

        

