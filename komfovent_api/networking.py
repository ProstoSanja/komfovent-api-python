from .classes import *

import aiohttp

async def check_connection_with_session(host: str, username: str, password: str, session: aiohttp.ClientSession) -> KomfoventConnectionResult:
    async with session.get(host) as resp:
        print(resp.status)
        print(await resp.text())
