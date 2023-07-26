from .base import BaseApi, BaseFinexApiHeaders
from .schemas import CurrencyResponse


class GetV1CurrenciesApi(BaseApi):
    success_statuses = (200,)
    method = 'get'
    url = '/v1/rates/currency/'
    response = CurrencyResponse
    header = BaseFinexApiHeaders
