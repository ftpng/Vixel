import asyncio
import time
from os import getenv
from collections import defaultdict, deque
from typing import Dict, Deque
from aiohttp import ClientSession, ContentTypeError
from aiohttp.client_exceptions import ClientConnectorError
from json import JSONDecodeError
from http.client import RemoteDisconnected
from requests.exceptions import ReadTimeout, ConnectTimeout

import vixlib as lib

_api_usage: Dict[str, Deque[float]] = defaultdict(deque)
_leaderboard_cache_paths = {}


def get_least_used_key(keys):
    now = time.time()
    best_key = None
    best_count = float("inf")

    for key in keys:
        if not key:
            continue

        while _api_usage[key] and now - _api_usage[key][0] > 60:
            _api_usage[key].popleft()

        count = len(_api_usage[key])
        if count < best_count:
            best_key = key
            best_count = count

    if not best_key:
        raise RuntimeError("No valid API keys available")

    _api_usage[best_key].append(now)
    return best_key


async def fetch_polsu_bedwars_leaderboard(
    mode: str,
    type_: str,
    top: int = 100,
    cache: bool = True,
    retries: int = 3,
    retry_delay: int = 5,
) -> dict:
    api_keys = [
        getenv("API_KEY_POLSU"),
        getenv("API_KEY_POLSU_2"),
        getenv("API_KEY_POLSU_3"),
    ]

    api_key = get_least_used_key(api_keys)

    url = "https://api.polsu.xyz/polsu/leaderboard/bedwars"
    headers = {
        "API-Key": api_key,
        "User-Agent": "Vixel Stats Bot Version 1"
    }
    params = {
        "mode": mode,
        "type": type_,
        "top": top
    }

    if cache:
        if mode not in _leaderboard_cache_paths:
            cache_path = f"{lib.DIR}vixlib/cache/leaderboards/leaderboard_cache_{mode}.sqlite"
            _leaderboard_cache_paths[mode] = cache_path
        cache_path = _leaderboard_cache_paths[mode]
    else:
        cache_path = None

    async def fetch(url: str):
        for attempt in range(retries + 1):
            try:
                if not cache or cache_path is None:
                    async with ClientSession() as session:
                        resp = await session.get(url, headers=headers, params=params, timeout=5)
                        data: dict = await resp.json()
                else:
                    from aiohttp_client_cache import CachedSession, SQLiteBackend
                    backend = SQLiteBackend(cache_name=cache_path, expire_after=300)
                    async with CachedSession(cache=backend) as session:
                        resp = await session.get(url, headers=headers, params=params, timeout=5)
                        data: dict = await resp.json()

                if "error" in data:
                    raise RuntimeError(f"Polsu API error: {data['error']}")

                return data

            except (
                ReadTimeout, ConnectTimeout, TimeoutError, asyncio.TimeoutError,
                JSONDecodeError, RemoteDisconnected, ContentTypeError, ClientConnectorError
            ) as exc:
                if attempt < retries:
                    await asyncio.sleep(retry_delay)
                else:
                    raise RuntimeError("Maximum number of retries exceeded.") from exc

        raise RuntimeError("Failed to fetch Polsu data.")

    leaderboard_data = await fetch(url)
    return leaderboard_data


async def fetch_polsu_player_ping(
    uuid: str,
    cache: bool = True,
    retries: int = 3,
    retry_delay: int = 5
) -> dict:
    api_keys = [
        getenv("API_KEY_POLSU"),
        getenv("API_KEY_POLSU_2"),
        getenv("API_KEY_POLSU_3"),
    ]

    api_key = get_least_used_key(api_keys)

    url = "https://api.polsu.xyz/polsu/ping"
    headers = {
        "API-Key": api_key,
        "User-Agent": "Vixel Stats Bot Version 1"
    }
    params = {
        "uuid": uuid
    }

    if cache:
        cache_path = f"{lib.DIR}vixlib/cache/ping/ping_cache.sqlite"
    else:
        cache_path = None

    async def fetch(url: str):
        for attempt in range(retries + 1):
            try:
                if not cache or cache_path is None:
                    async with ClientSession() as session:
                        resp = await session.get(url, headers=headers, params=params, timeout=5)
                        data: dict = await resp.json()
                else:
                    from aiohttp_client_cache import CachedSession, SQLiteBackend
                    backend = SQLiteBackend(cache_name=cache_path, expire_after=300)
                    async with CachedSession(cache=backend) as session:
                        resp = await session.get(url, headers=headers, params=params, timeout=5)
                        data: dict = await resp.json()

                if "error" in data:
                    raise RuntimeError(f"Polsu API error: {data['error']}")

                return data

            except (
                ReadTimeout, ConnectTimeout, TimeoutError, asyncio.TimeoutError,
                JSONDecodeError, RemoteDisconnected, ContentTypeError, ClientConnectorError
            ) as exc:
                if attempt < retries:
                    await asyncio.sleep(retry_delay)
                else:
                    raise RuntimeError("Maximum number of retries exceeded.") from exc

        raise RuntimeError("Failed to fetch Polsu ping data.")

    ping_data = await fetch(url)
    return ping_data


async def fetch_polsu_bedwars_formatted_name(
    uuid: str,
    cache: bool = True,
    retries: int = 3,
    retry_delay: int = 5
) -> dict:

    api_keys = [
        getenv("API_KEY_POLSU"),
        getenv("API_KEY_POLSU_2"),
        getenv("API_KEY_POLSU_3"),
    ]

    api_key = get_least_used_key(api_keys)

    url = "https://api.polsu.xyz/polsu/bedwars/formatted"
    headers = {
        "API-Key": api_key,
        "User-Agent": "Vixel Stats Bot Version 1"
    }
    params = {
        "uuid": uuid
    }

    if cache:
        cache_path = f"{lib.DIR}vixlib/cache/formatted/formatted_cache.sqlite"
    else:
        cache_path = None

    async def fetch(url: str):
        for attempt in range(retries + 1):
            try:
                if not cache or cache_path is None:
                    async with ClientSession() as session:
                        resp = await session.get(url, headers=headers, params=params, timeout=5)
                        data: dict = await resp.json()
                else:
                    from aiohttp_client_cache import CachedSession, SQLiteBackend
                    backend = SQLiteBackend(cache_name=cache_path, expire_after=300)
                    async with CachedSession(cache=backend) as session:
                        resp = await session.get(url, headers=headers, params=params, timeout=5)
                        data: dict = await resp.json()

                if "error" in data:
                    raise RuntimeError(f"Polsu API error: {data['error']}")

                return data

            except (
                ReadTimeout, ConnectTimeout, TimeoutError, asyncio.TimeoutError,
                JSONDecodeError, RemoteDisconnected, ContentTypeError, ClientConnectorError
            ) as exc:
                if attempt < retries:
                    await asyncio.sleep(retry_delay)
                else:
                    raise RuntimeError("Maximum number of retries exceeded.") from exc

        raise RuntimeError("Failed to fetch Polsu formatted name data.")

    formatted_name_data = await fetch(url)
    return formatted_name_data