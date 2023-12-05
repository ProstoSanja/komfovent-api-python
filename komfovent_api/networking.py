from .classes import *

import aiohttp
import logging

async def request(filename: str, creds: KomfoventCredentials) -> tuple[KomfoventConnectionResult, str]:
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(5.0)) as session:
            async with session.post(creds.host() + filename, data= {'1': creds.username, '2': creds.password}) as resp:
                return await validate_komfovent_response(resp)
    except Exception as error:
        return (KomfoventConnectionResult.NOT_FOUND, error)

async def validate_komfovent_response(resp: aiohttp.ClientResponse,) -> tuple[KomfoventConnectionResult, str]:
    text = await resp.text()
    if resp.status != 200:
        return (KomfoventConnectionResult.NOT_FOUND, f"Response status code: {resp.status}")
    if resp.headers.get('Server') != 'C6':
        return (KomfoventConnectionResult.NOT_FOUND, f"Headers: {resp.headers}")
    if "value=\"login\"" in text.replace(" ", "").lower():
        return (KomfoventConnectionResult.UNAUTHORISED, None)
    return (KomfoventConnectionResult.SUCCESS, text)

async def update(creds: KomfoventCredentials, command: KomfoventCommand, value) -> None:
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(5.0)) as session:
            async with session.post(creds.host() + "/ajax.xml", data=f"{command.value}={value}"):
                return
    except:
        return