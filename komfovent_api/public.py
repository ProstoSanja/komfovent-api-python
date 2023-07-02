from .classes import *
from .api import check_settings

import aiohttp

async def check_connection(host: str, username: str, password: str) -> tuple[KomfoventConnectionResult, str]:
    try:
        creds = KomfoventCredentials(host, username, password)
    except:
        return KomfoventConnectionResult.INVALID_INPUT
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(5.0)) as session:
        return await check_settings(creds, session)