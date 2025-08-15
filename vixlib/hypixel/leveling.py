from typing import NamedTuple


def decimal_of(number: float) -> int:
    return int(str(number).split(".")[-1])


class LevelProgressionTuple(NamedTuple):
    progress: int
    target: int
    progress_percent: float


class Leveling:
    def __init__(
        self,
        xp: int | None=None,
        level: int | None=None
    ) -> None:
        assert (xp, level).count(None) == 1, "Either level or xp must be provided."

        self.__xp = xp
        self.__level = level
        self.__progression = None

    @staticmethod
    def __calc_level(xp: int) -> float:  
        level: int = 100 * (xp // 487000)  
        xp %= 487000  
        xp_map = (0, 500, 1500, 3500, 7000)

        for index, value in enumerate(xp_map):
            if xp < value:
                factor = xp_map[index-1]
                return level + ((xp - factor) / (value - factor)) + (index - 1)
        return level + (xp - 7000) / 5000 + 4

    @property
    def level(self) -> float:
        if self.__level is None:
            self.__level = self.__calc_level(self.xp)
        return self.__level

    @property
    def level_int(self) -> int:
        return int(self.level)

    @staticmethod
    def __calc_xp(level: float):
        prestige, level = divmod(level, 100)
        xp = prestige * 487000
        xp_map = (0, 500, 1500, 3500, 7000)

        if level < 4:
            index = int(level)
            factor = xp_map[index]
            return int(xp + factor + (level - index) * (xp_map[index + 1] - factor))

        return int(xp + 7000 + (level - 4) * 5000)

    @property
    def xp(self) -> int:
        if self.__xp is None:
            self.__xp = self.__calc_xp(self.level)
        return self.__xp

    @staticmethod
    def __calc_progression(level: float) -> LevelProgressionTuple:
        lvls_since_pres = level % 100

        level_xp_map: dict = {0: 500, 1: 1000, 2: 2000, 3: 3500}
        lvl_target_xp: int = level_xp_map.get(int(lvls_since_pres), 5000)

        lvl_progress_xp = float(f'.{decimal_of(level)}') * lvl_target_xp
        lvl_progress_percentage = lvl_progress_xp / lvl_target_xp * 100

        return LevelProgressionTuple(
            int(lvl_progress_xp), int(lvl_target_xp), lvl_progress_percentage)

    @property
    def progression(self) -> LevelProgressionTuple:
        if self.__progression is None:
            self.__progression = self.__calc_progression(self.level)
        return self.__progression