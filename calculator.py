from asyncio import gather
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

from clients import PortfolioClient


class Currency(Enum):
    RUB = 'rub'
    USD = 'usd'

    @property
    def capitilezed_ticket(self) -> str:
        return self.value.upper()


class TableRow(BaseModel):
    row: list[str]


class StatisticTable(BaseModel):
    heads: list[str] = Field(['Fond Name', 'Fond Price', 'Quantity', 'Total'])
    final_row: Optional[list[str]] = Field(['All founds', '', '', ''])
    body: list[TableRow]


class Calculator:
    def __init__(
        self,
        portfolio_client: PortfolioClient,
        currency: Currency = Currency.RUB,
    ) -> None:
        self._cur_type = currency
        self._portfolio_client = portfolio_client
        self._cur: Optional[BaseModel] = None
        self._fonds: Optional[BaseModel] = None

    def _exclude_fonds(self) -> None:
        pass

    def _create_table_body(self) -> None:
        pass

    def _align_fonds_by_currency(self) -> None:
        pass

    async def get_table(self) -> StatisticTable:
        self._fonds, self._cur = await gather(
            self._portfolio_client.get_fonds(),
            self._portfolio_client.get_currencies(),
        )
        return  # type: ignore
