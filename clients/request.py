from copy import deepcopy

import aiohttp
from pydantic import BaseModel

from vars import HTTPResponseCodeVar

from .api.base import BaseApi


class RequestError(Exception):
    pass


async def make_http_request(
    api: BaseApi,
    read_body_on_error: int = 1024,
) -> BaseModel | None:
    _request_kwargs = {
        'method': api.method,
        'url': api.full_url,
        'headers': deepcopy(api.headers),
        'params': api.params,
        'timeout': aiohttp.ClientTimeout(total=api.request_timeout),
    }

    async with aiohttp.ClientSession() as client:
        resp: aiohttp.ClientResponse

        async with client.request(**_request_kwargs) as resp:
            HTTPResponseCodeVar.set(resp.status)
            if resp.status not in api.success_statuses:
                txt = await resp.content.read(read_body_on_error)
                raise RequestError(
                    f'Request fail {api.__class__}, {txt=},'
                    f' status_code={resp.status}'
                )

            if not api.has_response:
                return None

            txt = await resp.read()

            return api.parse_response(txt)
