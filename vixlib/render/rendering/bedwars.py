from vixlib.render import BackgroundImageLoader, ImageRender, DisplayName
from vixlib.hypixel import BedwarsStats, get_player_guild_dict
from vixlib.polsu import PlayerPing

from vixlib import DIR


bg = BackgroundImageLoader(dir="bedwars")

async def render_bedwars_stats(
    uuid: str, 
    mode: str,
    hypixel_data: dict,
    polsu_data: dict
) -> None:
    
    stats = BedwarsStats(hypixel_data, mode)
    ping = PlayerPing(polsu_data, uuid)
    im = ImageRender(bg.load_default_background())

    im.text.draw_many([
        (f"&a{stats.wins:,}", {"position": (413, 252)}),
        (f"&c{stats.losses:,}", {"position": (640, 252)}),
        (f"&6{stats.wlr}", {"position": (867, 252)}),

        (f"&a{stats.final_kills:,}", {"position": (413, 322)}),
        (f"&c{stats.final_deaths:,}", {"position": (640, 322)}),
        (f"&6{stats.fkdr}", {"position": (867, 322)}),

        (f"&a{stats.kills:,}", {"position": (413, 392)}),
        (f"&c{stats.deaths:,}", {"position": (640, 392)}),
        (f"&6{stats.kdr}", {"position": (867, 392)}),

        (f"&a{stats.beds_broken:,}", {"position": (413, 462)}),
        (f"&c{stats.beds_lost:,}", {"position": (640, 462)}),
        (f"&6{stats.bblr}", {"position": (867, 462)}),
    ], default_text_options={
        "shadow_offset": (2, 2), "align": "center", "font_size": 20}
    )   

    im.text.draw_many([
        (f"({mode})", {"position": (170, 91)})
    ], default_text_options={
        "shadow_offset": (2, 2), "align": "center", "font_size": 18},
    ) 

    im.text.draw_many([
        (f"&9{stats.games_played:,}", {"position": (955, 116)}),
        (f"&9{stats.most_played}", {"position": (955, 147)}),
        (f"&9{stats.winstreak:,}", {"position": (955, 178)}),
    ], default_text_options={
        "shadow_offset": (2, 2), "align": "right", "font_size": 16}
    )

    im.text.draw_many([
        (f"&d{ping.average_ping} &fms", {"position": (60, 465)}),
    ], default_text_options={
        "shadow_offset": (2, 2), "align": "left", "font_size": 16},
    )    

    hypixel_player_data = get_player_guild_dict(hypixel_data)
    display_name = DisplayName(hypixel_player_data).get_displayname_guild()
    im.text.draw_many([
        (display_name, {"position": (640, 60)})
    ], default_text_options={
        "shadow_offset": (2, 2), "align": "center", "font_size": 20},
    )

    lvl_progress, lvl_target, lvl_progress_percent = stats.leveling.progression

    await im.progress.draw_progress_bar(
        level=stats.level,
        progress_percentage=lvl_progress_percent,
        current_xp=lvl_progress,
        positions={
            'left': (430, 173),
            'center': (520, 172),
            'right': (611, 173)
        },
        font_size=18
    )    

    await im.progress.draw_progression(
        progress=lvl_progress, target=lvl_target,
        position=(520, 144),
        font_size=18
    )

    await im.progress.draw_prestige(
        level=stats.level,
        position=(520, 117),
        font_size=18
    )

    await im.skin.paste_skin(
        uuid, position=(70, 115), size=(204, 374)
    )

    im.overlay_image(bg.load_image(image_path=f"bg/bedwars/overlay.png"))
    im.save(f"{DIR}assets/imgs/bedwars.png")