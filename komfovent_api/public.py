from .classes import *
from .networking import check_connection_with_session

import aiohttp

async def check_connection(host: str, username: str, password: str) -> KomfoventConnectionResult:
    async with aiohttp.ClientSession() as session:
        return await check_connection_with_session(host, username, password, session)