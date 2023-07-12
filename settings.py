from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    allowed_currencies: list[str] = ['rub', 'usd']


def settings_factory() -> Settings:
    return Settings()


settings = settings_factory()
