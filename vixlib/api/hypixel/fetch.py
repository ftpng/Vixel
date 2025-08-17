import asyncio
from os import getenv
from json import JSONDecodeError
from http.client import RemoteDisconnected

from requests import ReadTimeout, ConnectTimeout
from aiohttp import ClientSession, ContentTypeError
from aiohttp_client_cache import CachedSession

from .errors import HypixelInvalidResponseError, HypixelRateLimitedError
from ..cache import STATS_CACHE

stats_session: CachedSession | None = None


async def init_hypixel_session():
    global stats_session
    stats_session = CachedSession(cache=STATS_CACHE)


async def close_hypixel_session():
    if stats_session:
        await stats_session.close()


async def __make_hypixel_request(session: ClientSession, url: str) -> dict:
    api_key = getenv('API_KEY_HYPIXEL')
    options = {
        'url': url,
        'headers': {"API-Key": api_key},
        'timeout': 5
    }
    return await (await session.get(**options)).json()


async def __fetch_hypixel_data(
    url: str,
    cache: bool = True,
    retries: int = 3,
    retry_delay: int = 5
) -> dict:
    for attempt in range(retries + 1):
        try:
            if not cache:
                async with ClientSession() as session:
                    return await __make_hypixel_request(session, url)

            resp = await stats_session.get(url, headers={"API-Key": getenv("API_KEY_HYPIXEL")}, timeout=5)
            return await resp.json()

        except (ReadTimeout, ConnectTimeout, TimeoutError, asyncio.TimeoutError,
                JSONDecodeError, RemoteDisconnected, ContentTypeError) as exc:
            if attempt < retries:
                print(f"Hypixel request failed. Retrying in {retry_delay} seconds...")
                await asyncio.sleep(retry_delay)
            else:
                raise HypixelInvalidResponseError(
                    "Maximum number of retries exceeded."
                ) from exc


async def fetch_hypixel_player_data(
    uuid: str,
    cache: bool = True,
    retries: int = 3,
    retry_delay: int = 5,
    attempts: int = 5,
    attempt_delay: int = 20,
    include_guild: bool = False
) -> dict:
    player_url = f"https://api.hypixel.net/player?uuid={uuid}"

    for attempt in range(attempts + 1):
        hypixel_data = await __fetch_hypixel_data(
            player_url, cache, retries, retry_delay
        )

        if not hypixel_data.get('success') and hypixel_data.get('throttle'):
            if attempt < attempts:
                print(
                    "We are being rate limited by hypixel. "
                    f"Retrying in {attempt_delay} seconds..."
                )
                await asyncio.sleep(attempt_delay)
            else:
                raise HypixelRateLimitedError('Maximum number of retries exceeded.')
        elif hypixel_data.get('success'):
            if include_guild:
                guild_url = f"https://api.hypixel.net/guild?player={uuid}"
                guild_data = await __fetch_hypixel_data(
                    guild_url, cache, retries, retry_delay
                )
                if guild_data.get("guild"):
                    hypixel_data["guild"] = guild_data["guild"]
            return hypixel_data

    return hypixel_data