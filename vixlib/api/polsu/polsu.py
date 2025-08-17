import asyncio
from os import getenv
from json import JSONDecodeError
from http.client import RemoteDisconnected

from requests import ReadTimeout, ConnectTimeout
from aiohttp import ClientSession, ContentTypeError, ClientConnectorError
from aiohttp_client_cache import CachedSession

from ..cache import PING_CACHE, FORMATTED_NAME_CACHE, LEADERBOARD_CACHES
from ..api_key import get_api_key
from .errors import PolsuInvalidResponseError, PolsuRateLimitedError

import vixlib as lib


ping_session = None
formatted_session = None
leaderboard_sessions = {}


async def init_sessions():
    global ping_session, formatted_session, leaderboard_sessions
    ping_session = CachedSession(cache=PING_CACHE)
    formatted_session = CachedSession(cache=FORMATTED_NAME_CACHE)
    leaderboard_sessions = {
        mode: CachedSession(cache=backend)
        for mode, backend in LEADERBOARD_CACHES.items()
    }

async def close_all_sessions():
    if ping_session:
        await ping_session.close()
    if formatted_session:
        await formatted_session.close()
    for session in leaderboard_sessions.values():
        await session.close()


async def fetch_polsu_data(
    endpoint: str,
    *,
    uuid: str = None,
    mode: str = None,
    type_: str = None,
    top: int = 100,
    cache: bool = True,
    retries: int = 3,
    retry_delay: int = 5
) -> dict:

    api_keys = [
        getenv("API_KEY_POLSU"),
        getenv("API_KEY_POLSU_2"),
        getenv("API_KEY_POLSU_3"),
    ]
    api_key = get_api_key(api_keys)

    if endpoint == "leaderboard":
        if not (mode and type_):
            raise ValueError("mode and type_ are required for leaderboard endpoint")
        url = "https://api.polsu.xyz/polsu/leaderboard/bedwars"
        params = {"mode": mode, "type": type_, "top": top}
        session = leaderboard_sessions[mode] if cache else None

    elif endpoint == "ping":
        if not uuid:
            raise ValueError("uuid is required for ping endpoint")
        url = "https://api.polsu.xyz/polsu/ping"
        params = {"uuid": uuid}
        session = ping_session if cache else None

    elif endpoint == "formatted":
        if not uuid:
            raise ValueError("uuid is required for formatted endpoint")
        url = "https://api.polsu.xyz/polsu/bedwars/formatted"
        params = {"uuid": uuid}
        session = formatted_session if cache else None

    else:
        raise ValueError("Invalid endpoint. Must be 'leaderboard', 'ping', or 'formatted'.")

    headers = {
        "API-Key": api_key,
        "User-Agent": "Vixel Stats Bot Version 1"
    }

    async def fetch():
        for attempt in range(retries + 1):
            try:
                if cache:
                    resp = await session.get(url, headers=headers, params=params, timeout=5)
                    data: dict = await resp.json()
                else:
                    async with ClientSession() as tmp_session:
                        async with tmp_session.get(url, headers=headers, params=params, timeout=5) as resp:
                            data: dict = await resp.json()

                if "error" in data:
                    if "rate limit" in data["error"] or data.get("throttle"):
                        raise PolsuRateLimitedError(data["error"])
                    raise PolsuInvalidResponseError(data["error"])

                return data

            except (
                ReadTimeout, ConnectTimeout, TimeoutError, asyncio.TimeoutError,
                JSONDecodeError, RemoteDisconnected, ContentTypeError, ClientConnectorError
            ) as exc:
                if attempt < retries:
                    await asyncio.sleep(retry_delay)
                else:
                    raise PolsuInvalidResponseError(
                        "Maximum number of retries exceeded."
                    ) from exc

        raise PolsuInvalidResponseError("Failed to fetch Polsu data.")

    return await fetch()
