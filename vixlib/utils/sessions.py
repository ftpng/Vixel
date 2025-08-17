from datetime import datetime

from vixlib import ensure_cursor, Cursor, VALID_COLUMNS
from vixlib.hypixel import BedwarsStats


class Session:
    def __init__(self, uuid: str) -> None:
        self.uuid = uuid

    @ensure_cursor
    def start_session(self, hypixel_data: dict, *, cursor: Cursor = None) -> None:
        modes = {
            "Overall": "",
            "Solos": "eight_one_",
            "Doubles": "eight_two_",
            "Threes": "four_three_",
            "Fours": "four_four_",
            "4v4": "two_four_",
        }

        fields = [
            "wins",
            "losses",
            "final_kills",
            "final_deaths",
            "kills",
            "deaths",
            "beds_broken",
            "beds_lost",
        ]

        stats_dict = {
            "uuid": self.uuid,
            "created_at": datetime.now(),
        }

        overall = BedwarsStats(hypixel_data, "Overall")
        stats_dict["experience"] = overall.experience

        for mode, prefix in modes.items():
            stats = BedwarsStats(hypixel_data, mode)

            for key in fields:
                value = getattr(stats, key, None)
                if value is None:
                    continue

                col_name = f"{key}_bedwars" if mode == "Overall" else f"{prefix}{key}_bedwars"

                if col_name in VALID_COLUMNS:
                    stats_dict[col_name] = value

        filtered_dict = {k: v for k, v in stats_dict.items() if k in VALID_COLUMNS}

        columns = ", ".join(filtered_dict.keys())
        placeholders = ", ".join(["%s"] * len(filtered_dict))
        update_assignments = ", ".join(
            f"{col} = VALUES({col})" for col in filtered_dict.keys() if col != "uuid"
        )

        sql = f"""
            INSERT INTO sessions ({columns}) VALUES ({placeholders})
            ON DUPLICATE KEY UPDATE
            {update_assignments}
        """

        cursor.execute(sql, list(filtered_dict.values()))

    @ensure_cursor
    def get_session(self, *, cursor: Cursor = None) -> dict:
        cursor.execute("SELECT * FROM sessions WHERE uuid=%s", (self.uuid,))
        row = cursor.fetchone()
        if row is None:
            return None

        columns = [desc[0] for desc in cursor.description]
        return dict(zip(columns, row))

    @ensure_cursor
    def get_session_creation_date(self, *, cursor: Cursor = None):
        cursor.execute("SELECT created_at FROM sessions WHERE uuid=%s", (self.uuid,))
        result = cursor.fetchone()
        return result[0] if result else None

    @ensure_cursor
    def get_session_experience(self, *, cursor: Cursor = None):
        cursor.execute("SELECT experience FROM sessions WHERE uuid=%s", (self.uuid,))
        result = cursor.fetchone()
        return result[0] if result else None