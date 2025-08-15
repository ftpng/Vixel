from aiohttp_client_cache import SQLiteBackend
from requests_cache import CachedSession
from vixlib import DIR


CACHE_PATH: str = f"{DIR}vixlib/api/cache/"

MOJANG_CACHE = CachedSession(
    cache_name=f"{CACHE_PATH}mojang_cache.sqlite",
    expire_after=60
)

STATS_CACHE = SQLiteBackend(
    cache_name=f"{CACHE_PATH}stats_cache.sqlite", 
    expire_after=300    
)

SKIN_CACHE = SQLiteBackend(
    cache_name=f"{CACHE_PATH}skin_cache.sqlite", 
    expire_after=900    
)

PING_CACHE = SQLiteBackend(
    cache_name=f"{CACHE_PATH}ping_cache.sqlite", 
    expire_after=300    
)

FORMATTED_NAME_CACHE = SQLiteBackend(
    cache_name=f"{CACHE_PATH}formatted_name_cache.sqlite", 
    expire_after=300    
)

LEADERBOARD_CACHE_SOLO = SQLiteBackend(
    cache_name=f"{CACHE_PATH}/leaderboards/leaderboard_cache_solo.sqlite",
    expire_after=300
)

LEADERBOARD_CACHE_DOUBLES = SQLiteBackend(
    cache_name=f"{CACHE_PATH}/leaderboards/leaderboard_cache_doubles.sqlite",
    expire_after=300
)

LEADERBOARD_CACHE_THREES = SQLiteBackend(
    cache_name=f"{CACHE_PATH}/leaderboards/leaderboard_cache_threes.sqlite",
    expire_after=300
)

LEADERBOARD_CACHE_FOURS = SQLiteBackend(
    cache_name=f"{CACHE_PATH}/leaderboards/leaderboard_cache_fours.sqlite",
    expire_after=300
)

LEADERBOARD_CACHE_OVERALL = SQLiteBackend(
    cache_name=f"{CACHE_PATH}/leaderboards/leaderboard_cache_overall.sqlite",
    expire_after=300
)

LEADERBOARD_CACHES = {
    "solo": LEADERBOARD_CACHE_SOLO,
    "doubles": LEADERBOARD_CACHE_DOUBLES,
    "threes": LEADERBOARD_CACHE_THREES,
    "fours": LEADERBOARD_CACHE_FOURS,
    "overall": LEADERBOARD_CACHE_OVERALL
}