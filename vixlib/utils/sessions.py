from datetime import datetime

from vixlib import ensure_cursor, Cursor
from vixlib.hypixel import BedwarsStats


class Session:
    def __init__(self, uuid: str) -> None:
        self.uuid = uuid

    @ensure_cursor
    def start_session(
        self, hypixel_data: dict, *, cursor: Cursor = None
    ) -> None:
        modes = {
            "Overall": "",
            "Solos": "eight_one_",
            "Doubles": "eight_two_",
            "Threes": "four_three_",
            "Fours": "four_four_",
            "4v4": "two_four_",
        }

        fields_to_store = [
            "wins",
            "losses",
            "final_kills",
            "final_deaths",
            "kills",
            "deaths",
            "beds_broken",
            "beds_lost",
            "games_played",
            "items_purchased",
            "tools_purchased",
            "resources_collected",
            "iron_collected",
            "gold_collected",
            "diamonds_collected",
            "emeralds_collected",
            "coins",
        ]

        stats_dict = {
            "uuid": self.uuid,
            "created_at": datetime.now(),
        }

        overall = BedwarsStats(hypixel_data, "Overall")
        stats_dict["experience"] = overall.experience

        for mode, prefix in modes.items():
            stats = BedwarsStats(hypixel_data, mode)

            mode_values = {k: getattr(stats, k, None) for k in fields_to_store}

            for key, value in mode_values.items():
                if value is None:
                    continue

                col_name = f"{key}_bedwars" if mode == "Overall" else f"{prefix}{key}_bedwars"
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