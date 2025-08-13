class BedwarsStats:
    def __init__(self, bedwars_data: dict) -> None:
        self.bedwars_data = bedwars_data

    def _get_bedwars_stats_mode(self, prefix: str) -> dict:
        def get_stat(key):
            return self.bedwars_data.get(f"{prefix}{key}", 0)

        wins = get_stat("wins_bedwars")
        losses = get_stat("losses_bedwars")
        wlr = round(wins / losses, 2) if losses > 0 else wins

        finals = get_stat("final_kills_bedwars")
        final_deaths = get_stat("final_deaths_bedwars")
        fkdr = round(finals / final_deaths, 2) if final_deaths > 0 else finals

        kills = get_stat("kills_bedwars")
        deaths = get_stat("deaths_bedwars")
        kdr = round(kills / deaths, 2) if deaths > 0 else kills

        beds_broken = get_stat("beds_broken_bedwars")
        beds_lost = get_stat("beds_lost_bedwars")
        bblr = round(beds_broken / beds_lost, 2) if beds_lost > 0 else beds_broken

        winstreak = get_stat("winstreak")
        total_games = get_stat("games_played_bedwars")

        return {
            "wins": wins,
            "losses": losses,
            "wlr": wlr,
            "final_kills": finals,
            "final_deaths": final_deaths,
            "fkdr": fkdr,
            "kills": kills,
            "deaths": deaths,
            "kdr": kdr,
            "beds_broken": beds_broken,
            "beds_lost": beds_lost,
            "bblr": bblr,
            "winstreak": winstreak,
            "total_games": total_games
        }

    def get_stats_by_mode(self, mode: str) -> dict:
        modes = {
            "Overall": "",
            "Solos": "eight_one_",
            "Doubles": "eight_two_",
            "Threes": "four_three_",
            "Fours": "four_four_",
            "4v4": "two_four_",
        }
        prefix = modes.get(mode)

        return self._get_bedwars_stats_mode(prefix)
    

    @property
    def most_played(self):
        modes = {
            "Solos": self.bedwars_data.get("eight_one_games_played_bedwars", 0),
            "Doubles": self.bedwars_data.get("eight_two_games_played_bedwars", 0),
            "Threes": self.bedwars_data.get("four_three_games_played_bedwars", 0),
            "Fours": self.bedwars_data.get("four_four_games_played_bedwars", 0),
            "4v4": self.bedwars_data.get("two_four_games_played_bedwars", 0),
        }

        most_played_mode = max(modes, key=modes.get)
        return most_played_mode
    

    @property
    def get_experience(self):
        experience = self.bedwars_data.get("Experience", 0)

        return experience


