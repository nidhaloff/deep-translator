from typing import Optional

import aiohttp

from deep_translator.exceptions import RequestError, TooManyRequests


async def async_get_request(
    session: aiohttp.ClientSession,
    url: str,
    params: Optional[dict] = None,
    proxies: Optional[dict] = None,
):
    async with session.get(url=url, params=params) as response:
        if response.status == 429:
            raise TooManyRequests()

        if response.status != 200:
            raise RequestError()

        return await response.text()
