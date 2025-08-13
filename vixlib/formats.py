from datetime import datetime
from typing import Union, Dict, Any
from dateutil.relativedelta import relativedelta

import vixlib as lib
from mcfetch import Player


def started_on(date_input) -> str:
    if isinstance(date_input, datetime):
        past = date_input
    else:
        past = datetime.strptime(str(date_input), "%Y-%m-%d %H:%M:%S")

    now = datetime.now()
    delta = relativedelta(now, past)

    if delta.years:
        ago = f"{delta.years} year{'s' if delta.years > 1 else ''} ago"
    elif delta.months:
        ago = f"{delta.months} month{'s' if delta.months > 1 else ''} ago"
    elif delta.days >= 7:
        weeks = delta.days // 7
        ago = f"{weeks} week{'s' if weeks > 1 else ''} ago"
    elif delta.days:
        ago = f"{delta.days} day{'s' if delta.days > 1 else ''} ago"
    elif delta.hours:
        ago = f"{delta.hours} hr{'s' if delta.hours > 1 else ''} ago"
    elif delta.minutes:
        ago = f"{delta.minutes} min{'s' if delta.minutes > 1 else ''} ago"
    else:
        ago = f"{delta.seconds} sec{'s' if delta.seconds > 1 else ''} ago"

    date_formatted = past.strftime("%d/%m/%Y")
    return f"{date_formatted} ({ago})"


RATIO_STATS = {"wlr", "kdr", "fkdr", "bblr"}


def format_footer_value(
    key: str, 
    val: Union[int, float, None], 
    lb_info: Dict[str, Any]
) -> str:
    
    label = lb_info['display_name']
    if key in RATIO_STATS:
        label = key.upper()
    try:
        if val is None:
            return f"{label}: N/A"
        if key in RATIO_STATS:
            return f"{label}: {float(val):.2f}"
        else:
            return f"{label}: {int(float(val)):,}"
    except Exception:
        return f"{label}: {val}"
    

def format_value(
    key: str,
    val: Union[int, float, None],
) -> str:

    RATIO_STATS = {"FKDR", "WLR", "BBLR", "KDR"}

    try:
        if val is None:
            return "N/A"
        if key in RATIO_STATS:
            return str(val)
        else:
            return f"{int(float(val)):,}"
        
    except Exception:
        return str(val)
    

def strip_minecraft_formatting(s: str) -> str:
    if not s:
        return ""
    return s.replace("§", "&")



async def get_leaderboard_page(
    data: dict,
    player: str,
) -> tuple[int | None, int | None]:

    uuid = Player(player=player, requests_obj=lib.CACHE).uuid
    if not uuid:
        return None, None

    undashed_uuid = uuid.replace('-', '')

    leaderboard = data.get("data", {}).get("leaderboard", [])
    index = next(
        (i for i, p in enumerate(leaderboard) if str(p.get('uuid', '')).replace('-', '') == undashed_uuid),
        None
    )

    if index is None:
        return None, None
    
    page = index // 10 + 1
    pos = index % 10 + 1

    return page, pos


def format_lb_name(name: str) -> str:
    result = ""
    skip_next = False
    for char in name:
        if skip_next:
            skip_next = False
            continue
        if char == '§':
            skip_next = True
            continue
        result += char
    return result