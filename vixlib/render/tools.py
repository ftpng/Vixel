import re

from .colors import PrestigeColorMaps


def split_string(
    input_string: str,
    split_chars: tuple | list
) -> list[tuple[str, str]]:
    pattern = '|'.join(map(re.escape, split_chars))

    match_posses = re.finditer(f"(.*?)(?:{pattern}|$)", input_string)
    matches = [match.group(1) for i, match in enumerate(match_posses) if i != 0]
    matches.remove("")

    if not matches:
        return [(input_string, '')]

    values = re.findall(pattern, input_string)

    if not input_string.startswith(tuple(split_chars)):
        values.insert(0, '')

    return zip(matches, values)