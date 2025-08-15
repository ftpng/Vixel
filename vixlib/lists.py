from discord.app_commands import Choice

MODES = [
    Choice(name="Overall", value="Overall"),
    Choice(name="Solos", value="Solos"),
    Choice(name="Doubles", value="Doubles"),
    Choice(name="Threes", value="Threes"),
    Choice(name="Fours", value="Fours"),
    Choice(name="4v4", value="4v4"),
]