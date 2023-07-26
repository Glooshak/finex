from asyncio import gather
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

from clients import PortfolioClient
from settings import UserTickers


class Currency(Enum):
    RUB = 'rub'
    USD = 'usd'
    EUR = 'eur'

    @property
    def capitilezed_ticket(self) -> str:
        return self.value.upper()


class TableRow(BaseModel):
    fond_name: str
    currency: str
    fond_price: float
    quantity: int
    total: float


class StatisticTable(BaseModel):
    heads: list[str] = Field(
        ['Fond Name', 'Currency', 'Fond Price', 'Quantity', 'Total']
    )
    body: list[TableRow] | None = None
    final_row: list[str | float] = Field(['All fonds', '', '', '', ''])

    def summarize_totals(self) -> float:
        if self.body is None:
            return 0.0
        return round(sum([row.total for row in self.body]), 2)


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

    def _create_rows(
        self,
        user_tickers: UserTickers,
    ) -> list[TableRow]:
        rows = []
        for ticker, _amount in user_tickers.items():
            fond = getattr(self._fonds, ticker)
            cur_info = getattr(
                self._cur.currencies_element.rates,  # type: ignore
                fond.currency,
            )
            fond_price = fond.value * getattr(
                cur_info, self._cur_type.capitilezed_ticket
            )
            quantity = user_tickers[fond.ticker]
            rows.append(
                TableRow(
                    fond_name=fond.ticker,
                    currency=self._cur_type.capitilezed_ticket,
                    fond_price=round(fond_price, 2),
                    quantity=quantity,
                    total=round(quantity * fond_price, 2),
                )
            )

        return rows

    async def get_table(
        self,
        tickers: UserTickers,
    ) -> StatisticTable:
        if not tickers:
            return StatisticTable()

        self._fonds, self._cur = await gather(
            self._portfolio_client.get_fonds(),
            self._portfolio_client.get_currencies(),
        )
        body = self._create_rows(tickers)
        st_table = StatisticTable(body=body)
        st_table.final_row[-1] = st_table.summarize_totals()
        st_table.final_row[1] = self._cur_type.capitilezed_ticket

        return st_table
