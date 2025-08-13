class SessionStats:
    def __init__(self, session_data: dict) -> None:
        self.session_data = session_data

    def _get_session_stats_mode(self, prefix: str) -> dict:
        def get_stat(key):
            return self.session_data.get(f"{prefix}{key}_bedwars", 0)

        wins = get_stat("wins")
        losses = get_stat("losses")
        wlr = round(wins / losses, 2) if losses > 0 else wins

        finals = get_stat("final_kills")
        final_deaths = get_stat("final_deaths")
        fkdr = round(finals / final_deaths, 2) if final_deaths > 0 else finals

        kills = get_stat("kills")
        deaths = get_stat("deaths")
        kdr = round(kills / deaths, 2) if deaths > 0 else kills

        beds_broken = get_stat("beds_broken")
        beds_lost = get_stat("beds_lost")
        bblr = round(beds_broken / beds_lost, 2) if beds_lost > 0 else beds_broken

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
            "bblr": bblr
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
        return self._get_session_stats_mode(prefix)
    
    def calc_stats_diff(self, current_stats: dict) -> dict:
        modes = {
            "Overall": "",
            "Solos": "eight_one_",
            "Doubles": "eight_two_",
            "Threes": "four_three_",
            "Fours": "four_four_",
            "4v4": "two_four_",
        }

        diff = {}

        diff["uuid"] = self.session_data.get("uuid")
        diff["created_at"] = self.session_data.get("created_at")
        diff["experience"] = current_stats.get("Experience", 0)

        base_keys = [
            "wins_bedwars",
            "losses_bedwars",
            "final_kills_bedwars",
            "final_deaths_bedwars",
            "kills_bedwars",
            "deaths_bedwars",
            "beds_broken_bedwars",
            "beds_lost_bedwars",
            "winstreak",
            "games_played_bedwars",
        ]

        for mode, prefix in modes.items():
            for base_key in base_keys:
                if mode == "Overall":
                    key = base_key
                    current_key = base_key
                else:
                    key = f"{prefix}{base_key}"
                    current_key = f"{prefix}{base_key}"

                db_value = self.session_data.get(key, 0) or 0
                current_value = current_stats.get(current_key, 0) or 0

                diff_value = current_value - db_value
                if diff_value < 0:
                    diff_value = 0  

                diff[key] = diff_value

        return diff        