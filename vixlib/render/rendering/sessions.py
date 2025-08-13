from vixlib.render import BackgroundImageLoader, ImageRender, DisplayName, Prestige
from vixlib.hypixel import SessionStats, Leveling, BedwarsStats
from vixlib.helpers import Session

import vixlib as lib


async def render_session_stats(uuid: str, mode: str) -> None:

    bg = BackgroundImageLoader(dir="session")
    im = ImageRender(bg.load_default_background())

    hypixel_data = await lib.fetch_hypixel_data(uuid)

    if not hypixel_data or "player" not in hypixel_data:
        print("Failed to fetch hypixel data for this user.")
        return

    hypixel_player_data: dict = hypixel_data.get("player", {})

    if "guild" in hypixel_data and hypixel_data["guild"]:
        hypixel_player_data["guild"] = hypixel_data["guild"]

    display_name = DisplayName(hypixel_player_data).get_displayname_guild()

    im.text.draw_many(
        [(display_name, {"position": (640, 60)})],
        default_text_options={"shadow_offset": (2, 2), "align": "center", "font_size": 20},
    )

    """im.text.draw_many(
        [
            (f"&aWins", {"position": (413, 150)}),
            (f"&cLosses", {"position": (640, 150)}),
            (f"&6WLR", {"position": (867, 150)}),
            (f"&aFinal Kills", {"position": (413, 220)}),
            (f"&cFinal Deaths", {"position": (640, 220)}),
            (f"&6FKDR", {"position": (867, 220)}),
            (f"&aKills", {"position": (413, 290)}),
            (f"&cDeaths", {"position": (640, 290)}),
            (f"&6KDR", {"position": (867, 290)}),
            (f"&aBeds Broken", {"position": (413, 360)}),
            (f"&cBeds Lost", {"position": (640, 360)}),
            (f"&6BBLR", {"position": (867, 360)}),
        ],
        default_text_options={"shadow_offset": (2, 2), "align": "center", "font_size": 16},
    )
    im.text.draw_many(
        [
            (f"Session Stats", {"position": (170, 65)}),
        ],
        default_text_options={"shadow_offset": (2, 2), "align": "center", "font_size": 18},
    )"""

    bedwars_stats: dict = hypixel_player_data.get("stats", {}).get("Bedwars", {})

    session_experience = Session(uuid).get_session_experience()
    current_experience = BedwarsStats(bedwars_stats).get_experience

    xp_difference = int(current_experience - session_experience)
    
    session_level = Leveling(session_experience).level
    current_level = Leveling(current_experience).level
    
    level_difference = round(current_level - session_level, 2)

    im.text.draw_many(
        [
            (f"&bLevels Gained: {level_difference}", {"position": (320, 434)}),
            (f"&bEXP Gained: {xp_difference:,}", {"position": (320, 462)})
        ],
        default_text_options={"shadow_offset": (2, 2), "align": "left", "font_size": 14},
    )

    session_stats: dict = Session(uuid).get_session()
    
    session_data = SessionStats(session_stats).calc_stats_diff(bedwars_stats)
    stats = SessionStats(session_data).get_stats_by_mode(mode)

    im.text.draw_many(
        [
            (f"&a{stats['wins']:,}", {"position": (413, 173)}),
            (f"&c{stats['losses']:,}", {"position": (640, 173)}),
            (f"&6{stats['wlr']}", {"position": (867, 173)}),

            (f"&a{stats['final_kills']:,}", {"position": (413, 243)}),
            (f"&c{stats['final_deaths']:,}", {"position": (640, 243)}),
            (f"&6{stats['fkdr']}", {"position": (867, 243)}),

            (f"&a{stats['kills']:,}", {"position": (413, 313)}),
            (f"&c{stats['deaths']:,}", {"position": (640, 313)}),
            (f"&6{stats['kdr']}", {"position": (867, 313)}),

            (f"&a{stats['beds_broken']:,}", {"position": (413, 383)}),
            (f"&c{stats['beds_lost']:,}", {"position": (640, 383)}),
            (f"&6{stats['bblr']}", {"position": (867, 383)}),
        ],
        default_text_options={"shadow_offset": (2, 2), "align": "center", "font_size": 20},
    )

    started_on = Session(uuid).get_session_creation_date()
    im.text.draw_many(
        [
            (f"&fStarted {lib.started_on(started_on)}", {"position": (640, 108)}),
        ],
        default_text_options={"shadow_offset": (2, 2), "align": "center", "font_size": 14},
    )
    im.text.draw_many(
        [(f"({mode})", {"position": (170, 91)})],
        default_text_options={"shadow_offset": (2, 2), "align": "center", "font_size": 18},
    )

    xp = Leveling(current_experience).current_xp_towards_next_level
    xp_needed = Leveling(current_experience).xp_needed_for_next_level(current_level)
    progress_percentage = Leveling(current_experience).progress_percentage

    await im.progress.render_progress_bar(
        current_level, xp, progress_percentage,
        positions={
            'left': (670, 462),
            'center': (760, 461),
            'right': (851, 462)
        },
        font_size=18
    )
    
    await im.progress.render_progression(
        xp, xp_needed,
        position=(760, 433),
        font_size=18
    )
    await im.skin.paste_skin(
        uuid, position=(70, 115), size=(204, 374)
    )

    im.overlay_image(bg.load_image(image_path=f"bg/session/overlay.png"))
    im.save(f"{lib.DIR}assets/imgs/session.png")