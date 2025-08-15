from typing import Literal


PROGRESS_BAR_MAX = 10

BEDWARS_MODES_MAP = {
    "overall": "",
    "solos": "eight_one_",
    "doubles": "eight_two_",
    "threes": "four_three_",
    "fours": "four_four_",
    "4v4": "two_four_"
}


def get_player_dict(hypixel_data: dict) -> dict:
    return hypixel_data.get('player') or {}


def ratio(dividend: int | float, divisor: int | float) -> int | float:
    return round(dividend / (divisor or 1), 2)


def get_most_mode(
    bedwars_data: dict,
    stat_key: str
) -> Literal["Solos", "Doubles", "Threes", "Fours", "4v4", "N/A"]:
    modes_dict: dict[str, int] = {
        'Solos': bedwars_data.get(f'eight_one_{stat_key}', 0),
        'Doubles': bedwars_data.get(f'eight_two_{stat_key}', 0),
        'Threes':  bedwars_data.get(f'four_three_{stat_key}', 0),
        'Fours': bedwars_data.get(f'four_four_{stat_key}', 0),
        '4v4': bedwars_data.get(f'two_four_{stat_key}', 0)
    }
    if max(modes_dict.values()) == 0:
        return "N/A"
    return str(max(modes_dict, key=modes_dict.get))


def get_most_played_mode(bedwars_data: dict):
    return get_most_mode(bedwars_data, 'games_played_bedwars')