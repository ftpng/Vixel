import asyncio
import logging
from typing import Literal
from os import getenv
from json import JSONDecodeError
from http.client import RemoteDisconnected

from requests import ReadTimeout, ConnectTimeout
from aiohttp import ClientSession, ContentTypeError, ClientTimeout
from aiohttp_client_cache import CachedSession, SQLiteBackend

from .constants import DIR
from .errors import HypixelInvalidResponseError, HypixelRateLimitedError

logger = logging.getLogger(__name__)

STATS_CACHE_PATH = f"{DIR}vixlib/cache/stats_cache.sqlite"
SKIN_CACHE_PATH = f"{DIR}vixlib/cache/skin_cache.sqlite"


async def _fetch_hypixel_data(
    uuid: str,
    cache: bool = True,
    retries: int = 3,
    retry_delay: int = 5,
) -> dict:
    api_key = getenv("API_KEY_HYPIXEL")
    if not api_key:
        raise RuntimeError("Missing API_KEY_HYPIXEL environment variable")

    async def fetch(url: str):
        for attempt in range(retries + 1):
            try:
                if not cache:
                    async with ClientSession(timeout=ClientTimeout(total=5)) as session:
                        resp = await session.get(url, headers={"API-Key": api_key})
                        data: dict = await resp.json()
                else:
                    backend = SQLiteBackend(cache_name=STATS_CACHE_PATH, expire_after=300)
                    async with CachedSession(cache=backend, timeout=ClientTimeout(total=5)) as session:
                        resp = await session.get(url, headers={"API-Key": api_key})
                        data: dict = await resp.json()

                if not data.get("success") and data.get("throttle"):
                    raise HypixelRateLimitedError()

                if data.get("success"):
                    return data
                else:
                    raise HypixelInvalidResponseError(
                        f"Hypixel API error: {data.get('cause', 'Unknown')}"
                    )

            except (
                ReadTimeout, ConnectTimeout, TimeoutError, asyncio.TimeoutError,
                JSONDecodeError, RemoteDisconnected, ContentTypeError,
            ) as exc:
                if attempt < retries:
                    await asyncio.sleep(retry_delay)
                else:
                    raise HypixelInvalidResponseError(
                        "Maximum number of retries exceeded."
                    ) from exc

        raise HypixelInvalidResponseError("Failed to fetch Hypixel data.")

    player_url = f"https://api.hypixel.net/player?uuid={uuid}"
    player_data = await fetch(player_url)

    guild_url = f"https://api.hypixel.net/guild?player={uuid}"
    guild_data = await fetch(guild_url)

    if "guild" in guild_data and guild_data["guild"]:
        player_data["guild"] = guild_data["guild"]

    return player_data


async def fetch_hypixel_data(
    uuid: str,
    cache: bool = True,
    retries: int = 3,
    retry_delay: int = 5,
    attempts: int = 5,
    attempt_delay: int = 20,
) -> dict:
    for attempt in range(attempts + 1):
        try:
            data = await _fetch_hypixel_data(uuid, cache, retries, retry_delay)
        except HypixelRateLimitedError:
            if attempt < attempts:
                print(f"Hypixel API rate limited. Retrying in {attempt_delay} seconds... (Attempt {attempt + 1}/{attempts})")
                await asyncio.sleep(attempt_delay)
                continue
            else:
                raise HypixelRateLimitedError("Maximum number of rate limit retries exceeded.")
        else:
            return data

    return data



SkinStyle = Literal[
    'face', 'front', 'frontfull', 'head',
    'bust', 'full', 'skin', 'processedskin'
]

DEFAULT_STEVE_SKIN_URL = (
    "https://textures.minecraft.net/texture/"
    "a4665d6a9c07b7b3ecf3b9f4b1c6bff0e43a9a3b65e5b4b94a3a4567d9a12345"
)

async def fetch_skin_model(
    uuid: str,
    style: SkinStyle = "full"
) -> bytes:
    base_url = "https://visage.surgeplay.com"
    headers = {
        "User-Agent": "Vixel Stats Bot Version 1"
    }
    timeout = ClientTimeout(total=5)

    url = f"{base_url}/{style}/512/{uuid}"

    try:
        backend = SQLiteBackend(cache_name=SKIN_CACHE_PATH, expire_after=900)
        async with CachedSession(cache=backend) as session:
            res = await session.get(url, headers=headers, timeout=timeout)
            if res.status == 200:
                return await res.read()
            else:
                backend_fallback = SQLiteBackend(cache_name=SKIN_CACHE_PATH, expire_after=900)
                async with CachedSession(cache=backend_fallback) as fallback_session:
                    fallback_res = await fallback_session.get(
                        DEFAULT_STEVE_SKIN_URL, headers=headers, timeout=timeout
                    )
                    return await fallback_res.read()

    except Exception:
        backend_fallback = SQLiteBackend(cache_name=SKIN_CACHE_PATH, expire_after=900)
        async with CachedSession(cache=backend_fallback) as fallback_session:
            fallback_res = await fallback_session.get(
                DEFAULT_STEVE_SKIN_URL, headers=headers, timeout=timeout
            )
            return await fallback_res.read()