from typing import Any

from pydantic import BaseSettings, root_validator


class Settings(BaseSettings):
    CLIENT_USER_AGENT: str = (
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) '
        'Gecko/20100101 Firefox/47.0'
    )
    FINEX_API_HOST: str = 'api.finex-etf.ru'
    FINEX_API_BASE_URL: str = 'https://api.finex-etf.ru'
    # Fonds
    FONDS: dict[str, int] | None = None
    FXBC: int = 0
    FXCN: int = 0
    FXDE: int = 0
    FXDM: int = 0
    FXEM: int = 0
    FXES: int = 0
    FXFA: int = 0
    FXGD: int = 0
    FXIM: int = 0
    FXIP: int = 0
    FXIT: int = 0
    FXKZ: int = 0
    FXMM: int = 0
    FXRD: int = 0
    FXRE: int = 0
    FXRL: int = 0
    FXRU: int = 0
    FXRW: int = 0
    FXTB: int = 0
    FXTP: int = 0
    FXUS: int = 0
    FXWO: int = 0

    @root_validator
    def fill_fonds(cls, values: dict[str, Any]) -> Any:
        fonds: dict[str, int] = {}
        for key, value in values.items():
            if not key.startswith('FX'):
                continue

            if value == 0:
                continue

            fonds[key] = value

        values['FONDS'] = fonds
        return values

    class Config:
        env_file = '.env'


def settings_factory() -> Settings:
    return Settings()


settings = settings_factory()
