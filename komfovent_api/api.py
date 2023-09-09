from .classes import *
from .networking import request, update

import lxml.html as LX

# helpers

def get_credentials(host: str, username: str, password: str) -> tuple[KomfoventConnectionResult, KomfoventCredentials]:
    try:
        return (KomfoventConnectionResult.SUCCESS, KomfoventCredentials(host, username, password))
    except:
        return (KomfoventConnectionResult.INVALID_INPUT, None)

def __string_to_float(input: str) -> float:
    formatted = ''.join(c for c in input if c.isdigit() or c == '.')
    if (len(formatted) > formatted.count('.')):
        return float(formatted)
    return 0.0
def __string_to_int(input: str) -> float:
    return int(''.join(c for c in input if c.isdigit()))

# check_settings

async def get_settings(creds: KomfoventCredentials) -> tuple[KomfoventConnectionResult, KomfoventSettings]:
    status, response = await request("/st.html", creds)
    if (status != KomfoventConnectionResult.SUCCESS):
        return (status, None)
    return (status, __parse_settings(response))

def __parse_settings(data: str) -> KomfoventSettings:
    root = LX.fromstring(data)
    name = root.xpath("//input[@name='204']")[0].value.strip()
    model = root.find_class("hide_cfg")[0].xpath("input")[0].value.strip()
    version = root.get_element_by_id("mmf1").value.strip()
    serial_number = root.get_element_by_id("c6sn").value.strip()
    return KomfoventSettings(name, model, version, serial_number)

# get_unit_status

async def get_unit_status(creds: KomfoventCredentials) -> tuple[KomfoventConnectionResult, KomfoventUnit]:
    status, response = await request("/i.asp", creds)
    if (status != KomfoventConnectionResult.SUCCESS):
        return (status, None)
    return (status, __parse_unit_status(response))

def __parse_unit_mode(root: any) -> KomfoventModes:
    if (root.xpath("omo")[0].text.strip().upper() == "OFF"):
        return KomfoventModes.OFF
    if (__string_to_int(root.xpath("vf")[0].text) >> 23 & 1):
        return KomfoventModes.AUTO
    # TODO: detect if heating is enabled in mode settings
    return KomfoventModes.COOL

def __parse_unit_status(data: str) -> KomfoventUnit:
    root = LX.fromstring(data.encode())
    return KomfoventUnit(
        preset = root.xpath("omo")[0].text.strip().upper(),
        mode = __parse_unit_mode(root),
        fan_speed = int(root.xpath("sp")[0].text.strip()),
        temp_target = __string_to_float(root.xpath("st")[0].text),
        temp_supply = __string_to_float(root.xpath("ai0")[0].text),
        temp_extract = __string_to_float(root.xpath("ai1")[0].text),
        temp_outside = __string_to_float(root.xpath("ai2")[0].text),
    )

async def set_preset(creds: KomfoventCredentials, preset: KomfoventPresets) -> KomfoventConnectionResult:
    auth_status, _ = await get_settings(creds)
    if (auth_status != KomfoventConnectionResult.SUCCESS):
        return auth_status
    await update(creds, KomfoventCommand.SET_PRESET, preset.value)
    return KomfoventConnectionResult.SUCCESS

async def set_mode(creds: KomfoventCredentials, mode: KomfoventModes) -> KomfoventConnectionResult:
    status, state = await get_unit_status(creds)
    if (status != KomfoventConnectionResult.SUCCESS):
        return status
    if (state.mode == mode):
        return KomfoventConnectionResult.SUCCESS
    if (mode == KomfoventModes.OFF):
        await update(creds, KomfoventCommand.ON_OFF, 0)
    elif (mode == KomfoventModes.AUTO):
        await update(creds, KomfoventCommand.SET_AUTO, 2)
    else:
        # disable all special modes
        if (state.mode == KomfoventModes.OFF):
            await update(creds, KomfoventCommand.ON_OFF, 0)
        elif (state.mode == KomfoventModes.AUTO):
            await update(creds, KomfoventCommand.SET_AUTO, 2)
    return await set_mode(creds, mode)