from .classes import *
from .networking import check_connection_with_session

import aiohttp

async def check_connection(host: str, username: str, password: str) -> KomfoventConnectionResult:
    try:
        creds = KomfoventCredentials(host, username, password)
    except:
        return KomfoventConnectionResult.INVALID_INPUT
    async with aiohttp.ClientSession() as session:
        return await check_connection_with_session(creds, session)