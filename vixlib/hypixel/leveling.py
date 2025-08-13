class Leveling:
    def __init__(self, xp: int = None):
        self.xp = xp


    @property
    def level(self) -> float:
        prestige = 100 * (self.xp // 487000)
        xp_remainder = self.xp % 487000
        xp_map = (0, 500, 1500, 3500, 7000)

        for index, value in enumerate(xp_map):
            if xp_remainder < value:
                factor = xp_map[index - 1]
                return prestige + (index - 1) + ((xp_remainder - factor) / (value - factor))
        return prestige + 4 + (xp_remainder - 7000) / 5000


    @staticmethod
    def xp_needed_for_next_level(level: int) -> int:
        levels_since_prestige = int(level % 100)
        xp_map = {0: 500, 1: 1000, 2: 2000, 3: 3500}
        return xp_map.get(levels_since_prestige, 5000)


    @property
    def current_xp_towards_next_level(self) -> int:
        target_xp = self.xp_needed_for_next_level(int(self.level))
        decimal_part = self.level - int(self.level)
        progress_xp = decimal_part * target_xp
        return int(progress_xp)


    @property
    def progress_percentage(self) -> float:
        current_xp = self.current_xp_towards_next_level
        target_xp = self.xp_needed_for_next_level(int(self.level))
        return (current_xp / target_xp) * 100