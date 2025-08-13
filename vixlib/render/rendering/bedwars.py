from vixlib.render import BackgroundImageLoader, ImageRender, DisplayName, Prestige
from vixlib.hypixel import BedwarsStats, Leveling

import vixlib as lib


async def render_bedwars_stats(uuid: str, mode: str) -> None:

    bg = BackgroundImageLoader(dir="bedwars")
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
    im.text.draw_many(
        [(f"({mode})", {"position": (170, 91)})],
        default_text_options={"shadow_offset": (2, 2), "align": "center", "font_size": 18},
    )

    """im.text.draw_many(
        [
            (f"{green}Wins", {"position": (413, 229)}),
            (f"{red}Losses", {"position": (640, 229)}),
            (f"{gold}WLR", {"position": (867, 229)}),
            (f"{green}Final Kills", {"position": (413, 299)}),
            (f"{red}Final Deaths", {"position": (640, 299)}),
            (f"{gold}FKDR", {"position": (867, 299)}),
            (f"{green}Kills", {"position": (413, 369)}),
            (f"{red}Deaths", {"position": (640, 369)}),
            (f"{gold}KDR", {"position": (867, 369)}),
            (f"{green}Beds Broken", {"position": (413, 439)}),
            (f"{red}Beds Lost", {"position": (640, 439)}),
            (f"{gold}BBLR", {"position": (867, 439)}),
        ],
        default_text_options={"shadow_offset": (2, 2), "align": "center", "font_size": 16},
    )
    im.text.draw_many(
        [
            (f"&fTotal games", {"position": (755, 115)}),
            (f"&fMost played", {"position": (755, 146)}),
            (f"&fWinstreak", {"position": (755, 177)}),
        ],
        default_text_options={"shadow_offset": (2, 2), "align": "left", "font_size": 14},
    )"""

    bedwars_data: dict = hypixel_player_data.get("stats", {}).get("Bedwars", {})
    stats = BedwarsStats(bedwars_data).get_stats_by_mode(mode)

    im.text.draw_many(
        [
            (f"&a{stats['wins']:,}", {"position": (413, 252)}),
            (f"&c{stats['losses']:,}", {"position": (640, 252)}),
            (f"&6{stats['wlr']}", {"position": (867, 252)}),

            (f"&a{stats['final_kills']:,}", {"position": (413, 322)}),
            (f"&c{stats['final_deaths']:,}", {"position": (640, 322)}),
            (f"&6{stats['fkdr']}", {"position": (867, 322)}),

            (f"&a{stats['kills']:,}", {"position": (413, 392)}),
            (f"&c{stats['deaths']:,}", {"position": (640, 392)}),
            (f"&6{stats['kdr']}", {"position": (867, 392)}),

            (f"&a{stats['beds_broken']:,}", {"position": (413, 462)}),
            (f"&c{stats['beds_lost']:,}", {"position": (640, 462)}),
            (f"&6{stats['bblr']}", {"position": (867, 462)}),
        ],
        default_text_options={"shadow_offset": (2, 2), "align": "center", "font_size": 20},
    )

    most_played = BedwarsStats(bedwars_data).most_played
    im.text.draw_many(
        [
            (f"&9{stats['total_games']:,}", {"position": (955, 116)}),
            (f"&9{stats['winstreak']:,}", {"position": (955, 178)}),
            (f"&9{most_played}", {"position": (955, 147)}),
        ],
        default_text_options={"shadow_offset": (2, 2), "align": "right", "font_size": 16},
    )

    ping: dict = await lib.fetch_polsu_player_ping(uuid)
    avg_ms: dict = ping.get("data", {}).get("stats", {})
    ms = avg_ms.get("avg", 0)

    im.text.draw_many(
        [
            (f"&d{round(ms)} &fms", {"position": (60, 465)}),
        ],
        default_text_options={"shadow_offset": (2, 2), "align": "left", "font_size": 16},
    )
    
    experience = bedwars_data.get("Experience", 0)
    progress_percentage = Leveling(experience).progress_percentage
    level = Leveling(experience).level

    xp = Leveling(experience).current_xp_towards_next_level
    xp_needed = Leveling(experience).xp_needed_for_next_level(level)

    await im.progress.render_progress_bar(
        level, xp, progress_percentage,
        positions={
            'left': (430, 173),
            'center': (520, 172),
            'right': (611, 173)
        },
        font_size=18
    )
    
    await im.progress.render_progression(
        xp, xp_needed,
        position=(520, 144),
        font_size=18
    )
    
    level = Prestige(int(level)).formatted_level
    await im.progress.render_prestige(
        level,
        position=(520, 117),
        font_size=18
    )

    await im.skin.paste_skin(
        uuid, position=(70, 115), size=(204, 374)
    )
    
    im.overlay_image(bg.load_image(image_path=f"bg/bedwars/overlay.png"))
    im.save(f"{lib.DIR}assets/imgs/bedwars.png")
