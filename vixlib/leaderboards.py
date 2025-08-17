import vixlib as lib

BEDWARS_LEADERBOARDS = {
    "overall": {
        "winstreak": {
            "path": f"{lib.DIR}data/overall/bedwars_winstreak.json",
            "channel_id": lib.OVERALL_WINSTREAK_CHANNEL,
            "display_name": "Winstreak"
        },
        "games_played": {
            "path": f"{lib.DIR}data/overall/bedwars_games.json",
            "channel_id": lib.OVERALL_STATS_CHANNEL,
            "display_name": "Games Played"
        },
        "wins": {
            "path": f"{lib.DIR}data/overall/bedwars_wins.json",
            "channel_id": lib.OVERALL_STATS_CHANNEL,
            "display_name": "Wins"
        },
        "losses": {
            "path": f"{lib.DIR}data/overall/bedwars_losses.json",
            "channel_id": lib.OVERALL_STATS_CHANNEL,
            "display_name": "Losses"
        },
        "wlr": {
            "path": f"{lib.DIR}data/overall/bedwars_wlr.json",
            "channel_id": lib.OVERALL_WLR_CHANNEL,
            "display_name": "WLR"
        },
        "kills": {
            "path": f"{lib.DIR}data/overall/bedwars_kills.json",
            "channel_id": lib.OVERALL_STATS_CHANNEL,
            "display_name": "Kills"
        },
        "deaths": {
            "path": f"{lib.DIR}data/overall/bedwars_deaths.json",
            "channel_id": lib.OVERALL_STATS_CHANNEL,
            "display_name": "Deaths"
        },
        "kdr": {
            "path": f"{lib.DIR}data/overall/bedwars_kdr.json",
            "channel_id": lib.OVERALL_KDR_CHANNEL,
            "display_name": "KDR"
        },
        "final_kills": {
            "path": f"{lib.DIR}data/overall/bedwars_final_kills.json",
            "channel_id": lib.OVERALL_STATS_CHANNEL,
            "display_name": "Final Kills"
        },
        "final_deaths": {
            "path": f"{lib.DIR}data/overall/bedwars_final_deaths.json",
            "channel_id": lib.OVERALL_STATS_CHANNEL,
            "display_name": "Final Deaths"
        },
        "fkdr": {
            "path": f"{lib.DIR}data/overall/bedwars_fkdr.json",
            "channel_id": lib.OVERALL_FKDR_CHANNEL,
            "display_name": "FKDR"
        },
        "beds_broken": {
            "path": f"{lib.DIR}data/overall/bedwars_beds_broken.json",
            "channel_id": lib.OVERALL_STATS_CHANNEL,
            "display_name": "Beds Broken"
        },
        "beds_lost": {
            "path": f"{lib.DIR}data/overall/bedwars_beds_lost.json",
            "channel_id": lib.OVERALL_STATS_CHANNEL,
            "display_name": "Beds Lost"
        },
        "bblr": {
            "path": f"{lib.DIR}data/overall/bedwars_bblr.json",
            "channel_id": lib.OVERALL_BBLR_CHANNEL,
            "display_name": "BBLR"
        },
        "stars": {
            "path": f"{lib.DIR}data/overall/bedwars_stars.json",
            "channel_id": lib.OVERALL_STARS_CHANNEL,
            "display_name": "Stars"
        }
    },
    "solos": {
        "winstreak": {
            "path": f"{lib.DIR}data/solos/bedwars_winstreak.json",
            "channel_id": lib.SOLOS_WINSTREAK_CHANNEL,
            "display_name": "Winstreak"
        },
        "games_played": {
            "path": f"{lib.DIR}data/solos/bedwars_games.json",
            "channel_id": lib.SOLOS_STATS_CHANNEL,
            "display_name": "Games Played"
        },
        "wins": {
            "path": f"{lib.DIR}data/solos/bedwars_wins.json",
            "channel_id": lib.SOLOS_STATS_CHANNEL,
            "display_name": "Wins"
        },
        "losses": {
            "path": f"{lib.DIR}data/solos/bedwars_losses.json",
            "channel_id": lib.SOLOS_STATS_CHANNEL,
            "display_name": "Losses"
        },
        "wlr": {
            "path": f"{lib.DIR}data/solos/bedwars_wlr.json",
            "channel_id": lib.SOLOS_WLR_CHANNEL,
            "display_name": "WLR"
        },
        "kills": {
            "path": f"{lib.DIR}data/solos/bedwars_kills.json",
            "channel_id": lib.SOLOS_STATS_CHANNEL,
            "display_name": "Kills"
        },
        "deaths": {
            "path": f"{lib.DIR}data/solos/bedwars_deaths.json",
            "channel_id": lib.SOLOS_STATS_CHANNEL,
            "display_name": "Deaths"
        },
        "kdr": {
            "path": f"{lib.DIR}data/solos/bedwars_kdr.json",
            "channel_id": lib.SOLOS_KDR_CHANNEL,
            "display_name": "KDR"
        },
        "final_kills": {
            "path": f"{lib.DIR}data/solos/bedwars_final_kills.json",
            "channel_id": lib.SOLOS_STATS_CHANNEL,
            "display_name": "Final Kills"
        },
        "final_deaths": {
            "path": f"{lib.DIR}data/solos/bedwars_final_deaths.json",
            "channel_id": lib.SOLOS_STATS_CHANNEL,
            "display_name": "Final Deaths"
        },
        "fkdr": {
            "path": f"{lib.DIR}data/solos/bedwars_fkdr.json",
            "channel_id": lib.SOLOS_FKDR_CHANNEL,
            "display_name": "FKDR"
        },
        "beds_broken": {
            "path": f"{lib.DIR}data/solos/bedwars_beds_broken.json",
            "channel_id": lib.SOLOS_STATS_CHANNEL,
            "display_name": "Beds Broken"
        },
        "beds_lost": {
            "path": f"{lib.DIR}data/solos/bedwars_beds_lost.json",
            "channel_id": lib.SOLOS_STATS_CHANNEL,
            "display_name": "Beds Lost"
        },
        "bblr": {
            "path": f"{lib.DIR}data/solos/bedwars_bblr.json",
            "channel_id": lib.SOLOS_BBLR_CHANNEL,
            "display_name": "BBLR"
        }
    },
    "doubles": {
        "winstreak": {
            "path": f"{lib.DIR}data/doubles/bedwars_winstreak.json",
            "channel_id": lib.DOUBLES_WINSTREAK_CHANNEL,
            "display_name": "Winstreak"
        },
        "games_played": {
            "path": f"{lib.DIR}data/doubles/bedwars_games.json",
            "channel_id": lib.DOUBLES_STATS_CHANNEL,
            "display_name": "Games Played"
        },
        "wins": {
            "path": f"{lib.DIR}data/doubles/bedwars_wins.json",
            "channel_id": lib.DOUBLES_STATS_CHANNEL,
            "display_name": "Wins"
        },
        "losses": {
            "path": f"{lib.DIR}data/doubles/bedwars_losses.json",
            "channel_id": lib.DOUBLES_STATS_CHANNEL,
            "display_name": "Losses"
        },
        "wlr": {
            "path": f"{lib.DIR}data/doubles/bedwars_wlr.json",
            "channel_id": lib.DOUBLES_WLR_CHANNEL,
            "display_name": "WLR"
        },
        "kills": {
            "path": f"{lib.DIR}data/doubles/bedwars_kills.json",
            "channel_id": lib.DOUBLES_STATS_CHANNEL,
            "display_name": "Kills"
        },
        "deaths": {
            "path": f"{lib.DIR}data/doubles/bedwars_deaths.json",
            "channel_id": lib.DOUBLES_STATS_CHANNEL,
            "display_name": "Deaths"
        },
        "kdr": {
            "path": f"{lib.DIR}data/doubles/bedwars_kdr.json",
            "channel_id": lib.DOUBLES_KDR_CHANNEL,
            "display_name": "KDR"
        },
        "final_kills": {
            "path": f"{lib.DIR}data/doubles/bedwars_final_kills.json",
            "channel_id": lib.DOUBLES_STATS_CHANNEL,
            "display_name": "Final Kills"
        },
        "final_deaths": {
            "path": f"{lib.DIR}data/doubles/bedwars_final_deaths.json",
            "channel_id": lib.DOUBLES_STATS_CHANNEL,
            "display_name": "Final Deaths"
        },
        "fkdr": {
            "path": f"{lib.DIR}data/doubles/bedwars_fkdr.json",
            "channel_id": lib.DOUBLES_FKDR_CHANNEL,
            "display_name": "FKDR"
        },
        "beds_broken": {
            "path": f"{lib.DIR}data/doubles/bedwars_beds_broken.json",
            "channel_id": lib.DOUBLES_STATS_CHANNEL,
            "display_name": "Beds Broken"
        },
        "beds_lost": {
            "path": f"{lib.DIR}data/doubles/bedwars_beds_lost.json",
            "channel_id": lib.DOUBLES_STATS_CHANNEL,
            "display_name": "Beds Lost"
        },
        "bblr": {
            "path": f"{lib.DIR}data/doubles/bedwars_bblr.json",
            "channel_id": lib.DOUBLES_BBLR_CHANNEL,
            "display_name": "BBLR"
        }
    },
    "threes": {
        "winstreak": {
            "path": f"{lib.DIR}data/threes/bedwars_winstreak.json",
            "channel_id": lib.THREES_WINSTREAK_CHANNEL,
            "display_name": "Winstreak"
        },
        "games_played": {
            "path": f"{lib.DIR}data/threes/bedwars_games.json",
            "channel_id": lib.THREES_STATS_CHANNEL,
            "display_name": "Games Played"
        },
        "wins": {
            "path": f"{lib.DIR}data/threes/bedwars_wins.json",
            "channel_id": lib.THREES_STATS_CHANNEL,
            "display_name": "Wins"
        },
        "losses": {
            "path": f"{lib.DIR}data/threes/bedwars_losses.json",
            "channel_id": lib.THREES_STATS_CHANNEL,
            "display_name": "Losses"
        },
        "wlr": {
            "path": f"{lib.DIR}data/threes/bedwars_wlr.json",
            "channel_id": lib.THREES_WLR_CHANNEL,
            "display_name": "WLR"
        },
        "kills": {
            "path": f"{lib.DIR}data/threes/bedwars_kills.json",
            "channel_id": lib.THREES_STATS_CHANNEL,
            "display_name": "Kills"
        },
        "deaths": {
            "path": f"{lib.DIR}data/threes/bedwars_deaths.json",
            "channel_id": lib.THREES_STATS_CHANNEL,
            "display_name": "Deaths"
        },
        "kdr": {
            "path": f"{lib.DIR}data/threes/bedwars_kdr.json",
            "channel_id": lib.THREES_KDR_CHANNEL,
            "display_name": "KDR"
        },
        "final_kills": {
            "path": f"{lib.DIR}data/threes/bedwars_final_kills.json",
            "channel_id": lib.THREES_STATS_CHANNEL,
            "display_name": "Final Kills"
        },
        "final_deaths": {
            "path": f"{lib.DIR}data/threes/bedwars_final_deaths.json",
            "channel_id": lib.THREES_STATS_CHANNEL,
            "display_name": "Final Deaths"
        },
        "fkdr": {
            "path": f"{lib.DIR}data/threes/bedwars_fkdr.json",
            "channel_id": lib.THREES_FKDR_CHANNEL,
            "display_name": "FKDR"
        },
        "beds_broken": {
            "path": f"{lib.DIR}data/threes/bedwars_beds_broken.json",
            "channel_id": lib.THREES_STATS_CHANNEL,
            "display_name": "Beds Broken"
        },
        "beds_lost": {
            "path": f"{lib.DIR}data/threes/bedwars_beds_lost.json",
            "channel_id": lib.THREES_STATS_CHANNEL,
            "display_name": "Beds Lost"
        },
        "bblr": {
            "path": f"{lib.DIR}data/threes/bedwars_bblr.json",
            "channel_id": lib.THREES_BBLR_CHANNEL,
            "display_name": "BBLR"
        }
    },
    "fours": {
        "winstreak": {
            "path": f"{lib.DIR}data/fours/bedwars_winstreak.json",
            "channel_id": lib.FOURS_WINSTREAK_CHANNEL,
            "display_name": "Winstreak"
        },
        "games_played": {
            "path": f"{lib.DIR}data/fours/bedwars_games.json",
            "channel_id": lib.FOURS_STATS_CHANNEL,
            "display_name": "Games Played"
        },
        "wins": {
            "path": f"{lib.DIR}data/fours/bedwars_wins.json",
            "channel_id": lib.FOURS_STATS_CHANNEL,
            "display_name": "Wins"
        },
        "losses": {
            "path": f"{lib.DIR}data/fours/bedwars_losses.json",
            "channel_id": lib.FOURS_STATS_CHANNEL,
            "display_name": "Losses"
        },
        "wlr": {
            "path": f"{lib.DIR}data/fours/bedwars_wlr.json",
            "channel_id": lib.FOURS_WLR_CHANNEL,
            "display_name": "WLR"
        },
        "kills": {
            "path": f"{lib.DIR}data/fours/bedwars_kills.json",
            "channel_id": lib.FOURS_STATS_CHANNEL,
            "display_name": "Kills"
        },
        "deaths": {
            "path": f"{lib.DIR}data/fours/bedwars_deaths.json",
            "channel_id": lib.FOURS_STATS_CHANNEL,
            "display_name": "Deaths"
        },
        "kdr": {
            "path": f"{lib.DIR}data/fours/bedwars_kdr.json",
            "channel_id": lib.FOURS_KDR_CHANNEL,
            "display_name": "KDR"
        },
        "final_kills": {
            "path": f"{lib.DIR}data/fours/bedwars_final_kills.json",
            "channel_id": lib.FOURS_STATS_CHANNEL,
            "display_name": "Final Kills"
        },
        "final_deaths": {
            "path": f"{lib.DIR}data/fours/bedwars_final_deaths.json",
            "channel_id": lib.FOURS_STATS_CHANNEL,
            "display_name": "Final Deaths"
        },
        "fkdr": {
            "path": f"{lib.DIR}data/fours/bedwars_fkdr.json",
            "channel_id": lib.FOURS_FKDR_CHANNEL,
            "display_name": "FKDR"
        },
        "beds_broken": {
            "path": f"{lib.DIR}data/fours/bedwars_beds_broken.json",
            "channel_id": lib.FOURS_STATS_CHANNEL,
            "display_name": "Beds Broken"
        },
        "beds_lost": {
            "path": f"{lib.DIR}data/fours/bedwars_beds_lost.json",
            "channel_id": lib.FOURS_STATS_CHANNEL,
            "display_name": "Beds Lost"
        },
        "bblr": {
            "path": f"{lib.DIR}data/fours/bedwars_bblr.json",
            "channel_id": lib.FOURS_BBLR_CHANNEL,
            "display_name": "BBLR"
        }
    },
    "4v4": {
        "winstreak": {
            "path": f"{lib.DIR}data/4v4/bedwars_winstreak.json",
            "channel_id": lib.FOUR_VS_FOUR_WINSTREAK_CHANNEL,
            "display_name": "Winstreak"
        },
        "games_played": {
            "path": f"{lib.DIR}data/4v4/bedwars_games.json",
            "channel_id": lib.FOUR_VS_FOUR_STATS_CHANNEL,
            "display_name": "Games Played"
        },
        "wins": {
            "path": f"{lib.DIR}data/4v4/bedwars_wins.json",
            "channel_id": lib.FOUR_VS_FOUR_STATS_CHANNEL,
            "display_name": "Wins"
        },
        "losses": {
            "path": f"{lib.DIR}data/4v4/bedwars_losses.json",
            "channel_id": lib.FOUR_VS_FOUR_STATS_CHANNEL,
            "display_name": "Losses"
        },
        "wlr": {
            "path": f"{lib.DIR}data/4v4/bedwars_wlr.json",
            "channel_id": lib.FOUR_VS_FOUR_WLR_CHANNEL,
            "display_name": "WLR"
        },
        "kills": {
            "path": f"{lib.DIR}data/4v4/bedwars_kills.json",
            "channel_id": lib.FOUR_VS_FOUR_STATS_CHANNEL,
            "display_name": "Kills"
        },
        "deaths": {
            "path": f"{lib.DIR}data/4v4/bedwars_deaths.json",
            "channel_id": lib.FOUR_VS_FOUR_STATS_CHANNEL,
            "display_name": "Deaths"
        },
        "kdr": {
            "path": f"{lib.DIR}data/4v4/bedwars_kdr.json",
            "channel_id": lib.FOUR_VS_FOUR_KDR_CHANNEL,
            "display_name": "KDR"
        },
        "final_kills": {
            "path": f"{lib.DIR}data/4v4/bedwars_final_kills.json",
            "channel_id": lib.FOUR_VS_FOUR_STATS_CHANNEL,
            "display_name": "Final Kills"
        },
        "final_deaths": {
            "path": f"{lib.DIR}data/4v4/bedwars_final_deaths.json",
            "channel_id": lib.FOUR_VS_FOUR_STATS_CHANNEL,
            "display_name": "Final Deaths"
        },
        "fkdr": {
            "path": f"{lib.DIR}data/4v4/bedwars_fkdr.json",
            "channel_id": lib.FOUR_VS_FOUR_FKDR_CHANNEL,
            "display_name": "FKDR"
        },
        "beds_broken": {
            "path": f"{lib.DIR}data/4v4/bedwars_beds_broken.json",
            "channel_id": lib.FOUR_VS_FOUR_STATS_CHANNEL,
            "display_name": "Beds Broken"
        },
        "beds_lost": {
            "path": f"{lib.DIR}data/4v4/bedwars_beds_lost.json",
            "channel_id": lib.FOUR_VS_FOUR_STATS_CHANNEL,
            "display_name": "Beds Lost"
        },
        "bblr": {
            "path": f"{lib.DIR}data/4v4/bedwars_bblr.json",
            "channel_id": lib.FOUR_VS_FOUR_BBLR_CHANNEL,
            "display_name": "BBLR"
        }
    }
}