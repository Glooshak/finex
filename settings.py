from pydantic import BaseSettings


class Settings(BaseSettings):

    ALLOWED_CURRENCIES: list[str] = ['rub', 'usd']
    CLIENT_USER_AGENT: str = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) ' \
                             'Gecko/20100101 Firefox/47.0'


def settings_factory() -> Settings:
    return Settings()


settings = settings_factory()
