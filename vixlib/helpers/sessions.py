from datetime import datetime
from vixlib import ensure_cursor, Cursor

from vixlib.hypixel import BedwarsStats
import vixlib as lib


class Session:
    def __init__(self, uuid: str) -> None:
        self.uuid = uuid

    @ensure_cursor
    def start_session(self, bedwars_data: dict, *, cursor: Cursor = None) -> None:
        bedwars_stats = BedwarsStats(bedwars_data)

        modes = {
            "Overall": "",
            "Solos": "eight_one_",
            "Doubles": "eight_two_",
            "Threes": "four_three_",
            "Fours": "four_four_",
            "4v4": "two_four_",
        }
        stats_dict = {
            "uuid": self.uuid,
            "created_at": datetime.now(),
            "experience": bedwars_stats.get_experience,
        }

        for mode, prefix in modes.items():
            mode_stats = bedwars_stats.get_stats_by_mode(mode)
            for key, value in mode_stats.items():
                if key in {"wlr", "fkdr", "kdr", "bblr", "winstreak", "total_games"}:
                    continue
                if mode == "Overall":
                    col_name = f"{key}_bedwars"
                else:
                    col_name = f"{prefix}{key}_bedwars"
                
                if col_name in lib.VALID_COLUMNS:
                    stats_dict[col_name] = value

        columns = ", ".join(stats_dict.keys())
        placeholders = ", ".join(["%s"] * len(stats_dict))

        update_assignments = ", ".join(
            f"{col} = VALUES({col})" for col in stats_dict.keys() if col != "uuid"
        )

        sql = f"""
            INSERT INTO sessions ({columns}) VALUES ({placeholders})
            ON DUPLICATE KEY UPDATE
            {update_assignments}
        """

        cursor.execute(sql, list(stats_dict.values()))


    @ensure_cursor
    def get_session(self, *, cursor: Cursor = None) -> dict:
        cursor.execute("SELECT * FROM sessions WHERE uuid=%s", (self.uuid,))
        row = cursor.fetchone()
        if row is None:
            return None
        
        columns = [desc[0] for desc in cursor.description]
        return dict(zip(columns, row))
    

    @ensure_cursor
    def get_session_creation_date(self, *, cursor: Cursor = None) -> datetime | None:
        cursor.execute(
            "SELECT created_at FROM sessions WHERE uuid=%s", (self.uuid,)
        )
        result = cursor.fetchone()
        return result[0] if result else None


    @ensure_cursor
    def get_session_experience(self, *, cursor: Cursor = None) -> int | None:
        cursor.execute(
            "SELECT experience FROM sessions WHERE uuid=%s", (self.uuid,)
        )
        result = cursor.fetchone()
        return result[0] if result else None   
    


