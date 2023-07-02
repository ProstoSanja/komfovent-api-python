from .classes import *

import aiohttp

async def request(filename: str, creds: KomfoventCredentials, session: aiohttp.ClientSession) -> tuple[KomfoventConnectionResult, str]:
    try:
        async with session.post(creds.host() + filename, data= {'1': creds.username, '2': creds.password}) as resp:
            return await validate_komfovent_response(resp)
    except:
        return (KomfoventConnectionResult.NOT_FOUND, None)

async def validate_komfovent_response(resp: aiohttp.ClientResponse,) -> tuple[KomfoventConnectionResult, str]:
    text = await resp.text()
    if resp.status != 200:
        return (KomfoventConnectionResult.NOT_FOUND, None)
    if resp.headers.get('Server') != 'C6':
        return (KomfoventConnectionResult.NOT_FOUND, None)
    if "value=\"login\"" in text.replace(" ", "").lower():
        return (KomfoventConnectionResult.UNAUTHORISED, None)
    return (KomfoventConnectionResult.SUCCESS, text)