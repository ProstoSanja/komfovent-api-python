from .classes import *

import aiohttp

async def check_connection_with_session(creds: KomfoventCredentials, session: aiohttp.ClientSession) -> KomfoventConnectionResult:
    async with session.post(creds.host(), data= {'1': creds.username, '2': creds.password}) as resp:
        print(resp.status)
        print(await resp.text())
