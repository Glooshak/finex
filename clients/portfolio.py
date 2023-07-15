from pydantic import BaseModel

from .api import (
    GetV1CurrenciesApi,
    GetV1FondsApi,
)
from .request import make_http_request


class PortfolioClient:

    def __init__(
            self,
            finex_api_base_url: str,
    ) -> None:
        self._finex_api_base_url: str = finex_api_base_url

    async def get_currencies(self) -> BaseModel | None:

        api = GetV1CurrenciesApi(
            self._finex_api_base_url
        )

        return await make_http_request(api)

    async def get_fonds(self) -> BaseModel | None:

        api = GetV1FondsApi(
            self._finex_api_base_url
        ).add_query_params(exclude_indicatives=True)

        return await make_http_request(api)
