from enum import Enum

class ColorMappings:
    black = (0, 0, 0)
    dark_blue = (0, 0, 170)
    dark_green = (0, 170, 0)
    dark_aqua = (0, 170, 170)
    dark_red = (170, 0, 0)
    dark_purple = (170, 0, 170)
    gold = (255, 170, 0)
    gray = (170, 170, 170)
    dark_gray = (85, 85, 85)
    blue = (85, 85, 255)
    green = (85, 255, 85)
    aqua = (85, 255, 255)
    red = (255, 85, 85)
    light_purple = (255, 85, 255)
    yellow = (255, 255, 85)
    white = (255, 255, 255)

    str_to_color_code = {
        'black': '&0',
        'dark_blue': '&1',
        'dark_green': '&2',
        'dark_aqua': '&3',
        'dark_red': '&4',
        'dark_purple': '&5',
        'gold': '&6',
        'gray': '&7',
        'dark_gray': '&8',
        'blue': '&9',
        'green': '&a',
        'aqua': '&b',
        'red': '&c',
        'light_purple': '&d',
        'yellow': '&e',
        'white': '&f'
    }

    color_codes: dict[str, tuple[int, int, int]] = {
        '&0': black,
        '&1': dark_blue,
        '&2': dark_green,
        '&3': dark_aqua,
        '&4': dark_red,
        '&5': dark_purple,
        '&6': gold,
        '&7': gray,
        '&8': dark_gray,
        '&9': blue,
        '&a': green,
        '&b': aqua,
        '&c': red,
        '&d': light_purple,
        '&e': yellow,
        '&f': white
    }


class PrestigeColorMaps:
    c = ColorMappings.str_to_color_code

    prestige_map = {
        10000: c['red'],
        900: c['dark_purple'],
        800: c['blue'],
        700: c['light_purple'],
        600: c['dark_red'],
        500: c['dark_aqua'],
        400: c['dark_green'],
        300: c['aqua'],
        200: c['gold'],
        100: c['white'],
        0: c['gray'],
    }

    prestige_map_2 = {
        5000: (c['dark_red'], c['dark_red'], c['dark_purple'], c['blue'], c['blue'], c['dark_blue'], c['black']),
        4900: (c['dark_green'], c['green'], c['white'], c['white'], c['green'], c['green'], c['dark_green']),
        4800: (c['dark_purple'], c['dark_purple'], c['red'], c['gold'], c['yellow'], c['aqua'], c['dark_aqua']),
        4700: (c['white'], c['dark_red'], c['red'], c['red'], c['blue'], c['dark_blue'], c['blue']),
        4600: (c['dark_aqua'], c['aqua'], c['yellow'], c['yellow'], c['gold'], c['light_purple'], c['dark_purple']),
        4500: (c['white'], c['white'], c['aqua'], c['aqua'], c['dark_aqua'], c['dark_aqua'], c['dark_aqua']),
        4400: (c['dark_green'], c['dark_green'], c['green'], c['yellow'], c['gold'], c['dark_purple'], c['light_purple']),
        4300: (c['black'], c['dark_purple'], c['dark_gray'], c['dark_gray'], c['dark_purple'], c['dark_purple'], c['black']),
        4200: (c['dark_blue'], c['blue'], c['dark_aqua'], c['aqua'], c['white'], c['gray'], c['gray']),
        4100: (c['yellow'], c['yellow'], c['gold'], c['red'], c['light_purple'], c['light_purple'], c['dark_purple']),
        4000: (c['dark_purple'], c['dark_purple'], c['red'], c['red'], c['gold'], c['gold'], c['yellow']),
        3900: (c['red'], c['red'], c['green'], c['green'], c['dark_aqua'], c['blue'], c['blue']),
        3800: (c['dark_blue'], c['dark_blue'], c['blue'], c['dark_purple'], c['dark_purple'], c['light_purple'], c['dark_blue']),
        3700: (c['dark_red'], c['dark_red'], c['red'], c['red'], c['aqua'], c['dark_aqua'], c['dark_aqua']),
        3600: (c['green'], c['green'], c['green'], c['aqua'], c['blue'], c['blue'], c['dark_blue']),
        3500: (c['red'], c['red'], c['dark_red'], c['dark_red'], c['dark_green'], c['green'], c['green']),
        3400: (c['dark_green'], c['green'], c['light_purple'], c['light_purple'], c['dark_purple'], c['dark_purple'], c['green']),
        3300: (c['blue'], c['blue'], c['blue'], c['light_purple'], c['red'], c['red'], c['dark_red']),
        3200: (c['red'], c['dark_red'], c['gray'], c['gray'], c['dark_red'], c['red'], c['red']),
        3100: (c['blue'], c['blue'], c['dark_aqua'], c['dark_aqua'], c['gold'], c['gold'], c['yellow']),
        3000: (c['yellow'], c['yellow'], c['gold'], c['gold'], c['red'], c['red'], c['dark_red']),
        2900: (c['aqua'], c['aqua'], c['dark_aqua'], c['dark_aqua'], c['blue'], c['blue'], c['blue']),
        2800: (c['green'], c['green'], c['dark_green'], c['dark_green'], c['gold'], c['gold'], c['yellow']),
        2700: (c['yellow'], c['yellow'], c['white'], c['white'], c['dark_gray'], c['dark_gray'], c['dark_gray']),
        2600: (c['dark_red'], c['dark_red'], c['red'], c['red'], c['light_purple'], c['light_purple'], c['dark_purple']),
        2500: (c['white'], c['white'], c['green'], c['green'], c['dark_green'], c['dark_green'], c['dark_green']),
        2400: (c['aqua'], c['aqua'], c['white'], c['white'], c['gray'], c['gray'], c['dark_gray']),
        2300: (c['dark_purple'], c['dark_purple'], c['light_purple'], c['light_purple'], c['gold'], c['yellow'], c['yellow']),
        2200: (c['gold'], c['gold'], c['white'], c['white'], c['aqua'], c['dark_aqua'], c['dark_aqua']),
        2100: (c['white'], c['white'], c['yellow'], c['yellow'], c['gold'], c['gold'], c['gold']),
        2000: (c['dark_gray'], c['gray'], c['white'], c['white'], c['gray'], c['gray'], c['dark_gray']),
        1900: (c['gray'], c['dark_purple'], c['dark_purple'], c['dark_purple'], c['dark_purple'], c['dark_gray'], c['gray']),
        1800: (c['gray'], c['blue'], c['blue'], c['blue'], c['blue'], c['dark_blue'], c['gray']),
        1700: (c['gray'], c['light_purple'], c['light_purple'], c['light_purple'], c['light_purple'], c['dark_purple'], c['gray']),
        1600: (c['gray'], c['red'], c['red'], c['red'], c['red'], c['dark_red'], c['gray']),
        1500: (c['gray'], c['dark_aqua'], c['dark_aqua'], c['dark_aqua'], c['dark_aqua'], c['blue'], c['gray']),
        1400: (c['gray'], c['green'], c['green'], c['green'], c['green'], c['dark_green'], c['gray']),
        1300: (c['gray'], c['aqua'], c['aqua'], c['aqua'], c['aqua'], c['dark_aqua'], c['gray']),
        1200: (c['gray'], c['yellow'], c['yellow'], c['yellow'], c['yellow'], c['gold'], c['gray']),
        1100: (c['gray'], c['white'], c['white'], c['white'], c['white'], c['gray'], c['gray']),
        1000: (c['red'], c['gold'], c['yellow'], c['green'], c['aqua'], c['light_purple'], c['dark_purple']),
    }


class PrestigeColorEnum(Enum):
    SINGLE = 1
    MULTI = 2


class PrestigeColors:
    def __init__(self, prestige: int):
        self.prestige = prestige

        if prestige in PrestigeColorMaps.prestige_map_2:
            self.type = PrestigeColorEnum.MULTI
            self.color = PrestigeColorMaps.prestige_map_2[prestige]
        else:
            self.type = PrestigeColorEnum.SINGLE
            self.color = PrestigeColorMaps.prestige_map.get(prestige, ColorMappings.str_to_color_code['gray'])


class Prestige:
    bedwars_star_symbol_map = {
        3100: '✥',
        2100: '⚝',
        1100: '✪',
        0: '✫'
    }

    def __init__(self, level: int) -> None:
        self._level = level
        capped_prestige = min(self.prestige, 5000)
        self.colors = PrestigeColors(capped_prestige)
        self.__star_symbol = None
        self.__formatted_level_str = None

    @property
    def prestige(self) -> int:
        level_rounded = (self._level // 100) * 100
        max_prestige = max(PrestigeColorMaps.prestige_map.keys())
        return min(level_rounded, max_prestige)

    @property
    def star_symbol(self) -> str:
        if self.__star_symbol is None:
            for threshold in sorted(self.bedwars_star_symbol_map.keys(), reverse=True):
                if self._level >= threshold:
                    self.__star_symbol = self.bedwars_star_symbol_map[threshold]
                    break
            else:
                self.__star_symbol = self.bedwars_star_symbol_map.get(0)
        return self.__star_symbol

    @property
    def formatted_level(self) -> str:
        if self.__formatted_level_str is None:
            prestige_colors = self.colors
            level_str = f'[{self._level}{self.star_symbol}]'

            if prestige_colors.type == PrestigeColorEnum.MULTI:
                colors = prestige_colors.color
                repeated_colors = (colors * ((len(level_str) // len(colors)) + 1))[:len(level_str)]
                self.__formatted_level_str = ''.join(
                    f'{color}{char}' for color, char in zip(repeated_colors, level_str)
                )
            else:
                self.__formatted_level_str = f'{prestige_colors.color}{level_str}'

        return self.__formatted_level_str
    

    @property
    def plain_formatted_level(self) -> str:
        return f'[{self._level}{self.star_symbol}]'