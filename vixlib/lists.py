from discord.app_commands import Choice

MODES = [
    Choice(name="Overall", value="Overall"),
    Choice(name="Solos", value="Solos"),
    Choice(name="Doubles", value="Doubles"),
    Choice(name="Threes", value="Threes"),
    Choice(name="Fours", value="Fours"),
    Choice(name="4v4", value="4v4"),
]

TYPES_LEADERBOARD = [
    Choice(name="Stars", value="stars"),
    Choice(name="Winstreak", value="winstreak"),
    Choice(name="Total Games", value="games_played"),
    Choice(name="Wins", value="wins"),
    Choice(name="Losses", value="losses"),
    Choice(name="WLR", value="wlr"),
    Choice(name="Final Kills", value="final_kills"),
    Choice(name="Final Deaths", value="final_deaths"),
    Choice(name="FKDR", value="fkdr"),
    Choice(name="Kills", value="kills"),
    Choice(name="Deaths", value="deaths"),
    Choice(name="KDR", value="kdr"),
    Choice(name="Beds Broken", value="beds_broken"),
    Choice(name="Beds Lost", value="beds_lost"),
    Choice(name="BBLR", value="bblr"),
]

PAGE_RANGES = {
    1: (1, 10),
    2: (11, 20),
    3: (21, 30),
    4: (31, 40),
    5: (41, 50),
    6: (51, 60),
    7: (61, 70),
    8: (71, 80),
    9: (81, 90),
    10: (91, 100)
}