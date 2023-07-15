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


class CurrencyResponse(BaseModel):
    date: date
    rates: dict[CURRENCIES_NAME, CurrencyInfo]


class FondInfo(BaseModel):
    ticket: str
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
