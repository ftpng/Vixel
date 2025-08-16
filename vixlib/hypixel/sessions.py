from .bedwars import BedwarsStats
from .leveling import Leveling
from .utils import BEDWARS_MODES_MAP

class SessionStats:
    def __init__(
        self, 
        hypixel_data: dict, 
        session_data: dict, 
        gamemode: str = 'Overall'
    ) -> None:
        
        self._gamemode = gamemode

        self._session_data = session_data or {}
        self._current = BedwarsStats(hypixel_data, gamemode)
        
        self._prefix = BEDWARS_MODES_MAP.get(self._gamemode, "")

        self.wins = self._get_diff("wins")
        self.losses = self._get_diff("losses")
        self.wlr = self._get_ratio(self.wins, self.losses)

        self.final_kills = self._get_diff("final_kills")
        self.final_deaths = self._get_diff("final_deaths")
        self.fkdr = self._get_ratio(self.final_kills, self.final_deaths)

        self.kills = self._get_diff("kills")
        self.deaths = self._get_diff("deaths")
        self.kdr = self._get_ratio(self.kills, self.deaths)

        self.beds_broken = self._get_diff("beds_broken")
        self.beds_lost = self._get_diff("beds_lost")
        self.bblr = self._get_ratio(self.beds_broken, self.beds_lost)

        current_xp = getattr(self._current, "experience", 0)
        self.experience = self._session_data.get("experience", 0)
        
        self.experience_diff = current_xp - self.experience

        self.leveling = Leveling(xp=self.experience)
        self.level = self.leveling.level

    def _get_ratio(self, val_1: int, val_2: int) -> float:
        return round(float(val_1) / (val_2 or 1), 2)

    def _get_session_stat(self, key: str, default=0) -> int:
        col_name = f"{key}_bedwars" if self._gamemode == "Overall" else f"{self._prefix}{key}_bedwars"
        return self._session_data.get(col_name, default)

    def _get_diff(self, key: str) -> int:
        current_value = getattr(self._current, key, 0)
        session_value = self._get_session_stat(key, 0)
        return current_value - session_value