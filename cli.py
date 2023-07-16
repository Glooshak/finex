import typer
from rich import print

from settings import settings


app = typer.Typer()


def validate_currencies(value: str) -> str:
    allowed_currencies = settings.ALLOWED_CURRENCIES
    if value not in allowed_currencies:
        raise typer.BadParameter(f'Only {"; ".join(allowed_currencies)} are allowed')
    return value


@app.command()
def assets(
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
    typer.echo(currency)


@app.command()
def configs() -> None:
    """
    Show cli settings
    """
    print(settings.dict())


if __name__ == '__main__':
    app()
