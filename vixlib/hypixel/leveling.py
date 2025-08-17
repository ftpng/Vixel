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
        xp: int | None = None,
        level: int | None = None
    ) -> None:
        assert (xp, level).count(None) == 1, "Either level or xp must be provided."

        self.__xp = xp
        self.__level = level
        self.__progression = None

    @staticmethod
    def __calc_level(xp: int) -> float:
        prestige = 100 * (xp // 487000)
        xp_remainder = xp % 487000
        xp_map = (0, 500, 1500, 3500, 7000)

        for index, value in enumerate(xp_map):
            if xp_remainder < value:
                factor = xp_map[index - 1]
                return prestige + (index - 1) + ((xp_remainder - factor) / (value - factor))
        return prestige + 4 + (xp_remainder - 7000) / 5000

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
    def xp_needed_for_next_level(level: int) -> int:
        """XP required to reach the next level from given integer level."""
        levels_since_prestige = int(level % 100)
        xp_map = {0: 500, 1: 1000, 2: 2000, 3: 3500}
        return xp_map.get(levels_since_prestige, 5000)

    @staticmethod
    def __calc_progression(level: float) -> LevelProgressionTuple:
        target_xp = Leveling.xp_needed_for_next_level(int(level))
        decimal_part = level - int(level)
        progress_xp = round(decimal_part * target_xp)
        progress_percent = (progress_xp / target_xp) * 100 if target_xp else 0.0

        return LevelProgressionTuple(progress_xp, target_xp, progress_percent)

    @property
    def progression(self) -> LevelProgressionTuple:
        if self.__progression is None:
            self.__progression = self.__calc_progression(self.level)
        return self.__progression