"""
Set up SQLite-based API caches with different expiration times.
"""

from aiohttp_client_cache import SQLiteBackend
from vixlib import DIR


CACHE_PATH: str = f"{DIR}vixlib/api/cache/"


MOJANG_CACHE = SQLiteBackend(
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

