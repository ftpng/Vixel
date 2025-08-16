from vixlib.render import BackgroundImageLoader, ImageRender, DisplayName
from vixlib.hypixel import SessionStats, BedwarsStats, get_player_guild_dict

from vixlib.utils import Session
import vixlib as lib


bg = BackgroundImageLoader(dir="session")

async def render_session_stats(
    uuid: str, 
    mode: str,
    hypixel_data: dict
) -> None:

    session = Session(uuid)

    session_data: dict = session.get_session()
    stats = SessionStats(hypixel_data, session_data, mode)
    bedwars_stats = BedwarsStats(hypixel_data, mode)

    im = ImageRender(bg.load_default_background())

    im.text.draw_many([
        (f"&a{stats.wins:,}", {"position": (413, 173)}),
        (f"&c{stats.losses:,}", {"position": (640, 173)}),
        (f"&6{stats.wlr}", {"position": (867, 173)}),

        (f"&a{stats.final_kills:,}", {"position": (413, 243)}),
        (f"&c{stats.final_deaths:,}", {"position": (640, 243)}),
        (f"&6{stats.fkdr}", {"position": (867, 243)}),

        (f"&a{stats.kills:,}", {"position": (413, 313)}),
        (f"&c{stats.deaths:,}", {"position": (640, 313)}),
        (f"&6{stats.kdr}", {"position": (867, 313)}),

        (f"&a{stats.beds_broken:,}", {"position": (413, 383)}),
        (f"&c{stats.beds_lost:,}", {"position": (640, 383)}),
        (f"&6{stats.bblr}", {"position": (867, 383)}),
    ], default_text_options={
        "shadow_offset": (2, 2), "align": "center", "font_size": 20}
    )     

    lvl_diff = round(
        bedwars_stats.leveling.level - stats.leveling.level, 2
    )
    
    im.text.draw_many([
        (f"&bLevels Gained: {lvl_diff}", {"position": (320, 434)}),
        (f"&bEXP Gained: {stats.experience_diff:,}", {"position": (320, 462)})
    ], default_text_options={
        "shadow_offset": (2, 2), "align": "left", "font_size": 14},
    )    

    started_on = session.get_session_creation_date()
    im.text.draw_many([
        (f"&fStarted {lib.format_timestamp(started_on)}", {"position": (640, 108)}),
    ], default_text_options={
        "shadow_offset": (2, 2), "align": "center", "font_size": 14},
    )
    im.text.draw_many([
        (f"({mode})", {"position": (170, 91)})
    ], default_text_options={
        "shadow_offset": (2, 2), "align": "center", "font_size": 18},
    )    

    hypixel_player_data = get_player_guild_dict(hypixel_data)
    display_name = DisplayName(hypixel_player_data).get_displayname_guild()
    im.text.draw_many([
        (display_name, {"position": (640, 60)})
    ], default_text_options={
        "shadow_offset": (2, 2), "align": "center", "font_size": 20},
    )

    lvl_progress, lvl_target, lvl_progress_percent = bedwars_stats.leveling.progression

    await im.progress.draw_progress_bar(
        level=stats.level,
        progress_percentage=lvl_progress_percent,
        current_xp=lvl_progress,
        positions={
            'left': (670, 462),
            'center': (760, 461),
            'right': (851, 462)
        },
        font_size=18
    )   

    await im.progress.draw_progression(
        progress=lvl_progress, target=lvl_target,
        position=(760, 433),
        font_size=18
    )

    await im.skin.paste_skin(
        uuid, position=(70, 115), size=(204, 374)
    )    

    im.overlay_image(bg.load_image(image_path=f"bg/session/overlay.png"))
    im.save(f"{lib.DIR}assets/imgs/session.png")