from .classes import *
from .networking import request

import aiohttp
import lxml.html as LX

async def check_settings(creds: KomfoventCredentials, session: aiohttp.ClientSession) -> tuple[KomfoventConnectionResult, KomfoventSettinsResponse]:
    status, response = await request("/st.html", creds, session)
    if (status != KomfoventConnectionResult.SUCCESS):
        return (status, None)
    return (status, parse_settings(response))

def parse_settings(data: str) -> KomfoventSettinsResponse:
    root = LX.fromstring(data)
    name = root.xpath("//input[@name='204']")[0].value.strip()
    model = root.find_class("hide_cfg")[0].xpath("input")[0].value.strip()
    version = root.get_element_by_id("mmf1").value.strip()
    serial_number = root.get_element_by_id("c6sn").value.strip()
    return KomfoventSettinsResponse(name, model, version, serial_number)