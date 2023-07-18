import typer
from rich import print
from rich.console import Console

from async_typer import AsyncTyper
from calculator import Calculator, Currency, StatisticTable
from clients import PortfolioClient
from clients.api import CurrencyResponse
from settings import settings

app = AsyncTyper()
console = Console()


def validate_currencies(
    value: str,
) -> str:
    allowed_currencies = [cur.value for cur in Currency]
    if value not in allowed_currencies:
        raise typer.BadParameter(
            f'Only {"; ".join(allowed_currencies)} are allowed'
        )
    return value


@app.async_command()
async def assets(
    currency: str = typer.Option(
        'rub',
        callback=validate_currencies,
        help='Currency of assets',
    )
) -> None:
    """
    Showing your FinEx assets in different currencies.
    You are able to choose currencies with option --currency.
    By default --currency==rub.
    Available currencies: rub, usd.
    """

    _: StatisticTable = await Calculator(
        PortfolioClient(settings.FINEX_API_BASE_URL),
        currency=Currency(currency),
    ).get_table()


@app.async_command()
async def currency_rates() -> None:
    """
    Show currencies echange rated
    """
    cur_array = await PortfolioClient(
        settings.FINEX_API_BASE_URL
    ).get_currencies()
    cur_array: CurrencyResponse  # type: ignore
    print(cur_array.currencies_element.dict())  # type: ignore


@app.command()
def configs() -> None:
    """
    Show cli settings
    """
    print(settings.dict())


if __name__ == '__main__':
    app()
