from datetime import date
from typing import Literal

from pydantic import BaseModel

CURRENCIES_NAME = Literal[
    'EUR',
    'GBP',
    'KZT',
    'RUB',
    'USD',
]


class CurrencyInfo(BaseModel):
    EUR: float
    GBP: float
    KZT: float
    RUB: float
    USD: float

    def convert_to_eur(self) -> float:
        return self.EUR

    def convert_to_gbp(self) -> float:
        return self.GBP

    def convert_to_kzt(self) -> float:
        return self.KZT

    def convert_to_rub(self) -> float:
        return self.RUB

    def convert_to_usd(self) -> float:
        return self.USD


class CurrenciesInfo(BaseModel):
    EUR: CurrencyInfo
    GBP: CurrencyInfo
    KZT: CurrencyInfo
    RUB: CurrencyInfo
    USD: CurrencyInfo


class CurrencyResponseItem(BaseModel):
    date: date
    rates: CurrenciesInfo


class CurrencyResponse(BaseModel):
    __root__: list[CurrencyResponseItem]

    @property
    def currencies_element(self) -> CurrencyResponseItem:
        elements_array = self.__root__

        if len(elements_array) > 1:
            return elements_array[0]

        [cur_element] = elements_array

        return cur_element


class FondInfo(BaseModel):
    ticker: str
    date: date
    currency: str
    value: float


class FondsResponse(BaseModel):
    FXBC: FondInfo
    FXEM: FondInfo
    FXRE: FondInfo
    FXRD: FondInfo
    FXES: FondInfo
    FXIP: FondInfo
    FXTP: FondInfo
    FXFA: FondInfo
    FXDM: FondInfo
    FXGD: FondInfo
    FXWO: FondInfo
    FXRW: FondInfo
    FXTB: FondInfo
    FXMM: FondInfo
    FXRL: FondInfo
    FXIM: FondInfo
    FXIT: FondInfo
    FXUS: FondInfo
    FXRU: FondInfo
    FXDE: FondInfo
    FXCN: FondInfo
    FXKZ: FondInfo
