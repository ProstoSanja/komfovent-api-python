from .classes import *
from .networking import request

import aiohttp
import lxml.html as LX

# helpers

def get_credentials(host: str, username: str, password: str) -> tuple[KomfoventConnectionResult, KomfoventCredentials]:
    try:
        return (KomfoventConnectionResult.SUCCESS, KomfoventCredentials(host, username, password))
    except:
        return (KomfoventConnectionResult.INVALID_INPUT, None)

def __string_to_float(input: str) -> float:
    return float(''.join(c for c in input if c.isdigit() or c == '.'))

# check_settings

async def get_settings(creds: KomfoventCredentials) -> tuple[KomfoventConnectionResult, KomfoventSettins]:
    status, response = await request("/st.html", creds)
    if (status != KomfoventConnectionResult.SUCCESS):
        return (status, None)
    return (status, __parse_settings(response))

def __parse_settings(data: str) -> KomfoventSettins:
    root = LX.fromstring(data)
    name = root.xpath("//input[@name='204']")[0].value.strip()
    model = root.find_class("hide_cfg")[0].xpath("input")[0].value.strip()
    version = root.get_element_by_id("mmf1").value.strip()
    serial_number = root.get_element_by_id("c6sn").value.strip()
    return KomfoventSettins(name, model, version, serial_number)

# get_unit_status

async def get_unit_status(creds: KomfoventCredentials) -> tuple[KomfoventConnectionResult, KomfoventUnit]:
    status, response = await request("/i.asp", creds)
    if (status != KomfoventConnectionResult.SUCCESS):
        return (status, None)
    return (status, __parse_unit_status(response))

def __parse_unit_status(data: str) -> KomfoventUnit:
    root = LX.fromstring(data.encode())
    return KomfoventUnit(
        mode = root.xpath("omo")[0].text.strip().upper(),
        fan_speed = int(root.xpath("sp")[0].text.strip()),
        temp_target = __string_to_float(root.xpath("st")[0].text),
        temp_supply = __string_to_float(root.xpath("ai0")[0].text),
        temp_extract = __string_to_float(root.xpath("ai1")[0].text),
        temp_outside = __string_to_float(root.xpath("ai2")[0].text),
    )
