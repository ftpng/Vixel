from typing import Literal
from aiohttp import ClientTimeout
from aiohttp_client_cache import CachedSession, SQLiteBackend

from vixlib.api.cache import SKIN_CACHE


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
        async with CachedSession(cache=SKIN_CACHE) as session:
            res = await session.get(url, headers=headers, timeout=timeout)
            if res.status == 200:
                return await res.read()
            else:
                async with CachedSession(cache=SKIN_CACHE) as fallback_session:
                    fallback_res = await fallback_session.get(
                        DEFAULT_STEVE_SKIN_URL, headers=headers, timeout=timeout
                    )
                    return await fallback_res.read()

    except Exception:
        async with CachedSession(cache=SKIN_CACHE) as fallback_session:
            fallback_res = await fallback_session.get(
                DEFAULT_STEVE_SKIN_URL, headers=headers, timeout=timeout
            )
            return await fallback_res.read()