from pydantic import BaseModel

from .base import (
    BaseApi,
    BaseFinexApiHeaders,
)
from .schemas import FondsResponse


class GetV1FondsApiQueryParams(BaseModel):
    exclude_indicatives: bool


class GetV1FondsApi(BaseApi):
    success_statuses = (200,)
    method = 'get'
    url = '/v1/fonds/nav'
    response = FondsResponse
    header = BaseFinexApiHeaders
    query_params = GetV1FondsApiQueryParams  # type: ignore
