from enum import Enum
from typing import Any, Self
from functools import cached_property

from pydantic import BaseModel, parse_raw_as, parse_obj_as

from settings import settings


class ContentType(Enum):
    JSON = 'application/json'
    X_WWW_FORM_URLENCODED = 'application/x-www-form-urlencoded'
    FORM_DATA = None
    TEXT = 'text/plain'


class BaseApi:

    body: BaseModel | None = None
    body_type: ContentType = ContentType.JSON
    accept: ContentType = ContentType.JSON
    query_params: BaseModel | None = None
    url_params: BaseModel | None = None
    header_params: BaseModel | None = None
    security: BaseModel | None = None

    has_response: bool = True
    response: Any
    success_statuses: tuple[int, ...] = (200, 201, 203)

    base_url: str
    url: str
    method: str

    def __init__(
            self,
            base_url: str,
    ) -> None:

        self.base_url = base_url

    def _parse_model(
            self,
            annot_name,
            cached_key,
            model: BaseModel | None = None,
            **kwargs,
    ) -> None:

        if model is not None:
            setattr(self, annot_name, model)
        else:
            setattr(
                self,
                annot_name,
                parse_obj_as(
                    self.__annotations__[annot_name],
                    kwargs,
                )
            )
        if cached_key in self.__dict__:
            del self.__dict__[cached_key]

    @cached_property
    def headers(self) -> dict[str, Any]:
        headers = {
            'content-type': self.body_type.value,
            'accept': self.accept.value,
            'user-agent': settings.CLIENT_USER_AGENT,
        }

        if self.header_params is not None:
            _headers = self.header_params.dict(exclude_none=True, by_alias=True)
            for key, val in _headers.items():
                headers[key.lower()] = val
            if self.auth:
                for key, val in self.auth.items():
                    headers[key.lower()] = val

        return headers

    def add_header(self, key: str, value: str | list[str]) -> Self:

        self.headers[key.lower()] = value
        return self

    def add_query_params(self, **kwargs) -> Self:

        self._parse_model(
            annot_name='query_params',
            cached_key='params',
            **kwargs,
        )

        return self

    def add_header_params(self, **kwargs) -> Self:
        self._parse_model(annot_name='header_params', cached_key='headers', **kwargs)
        return self

    def add_security(self, **kwargs):
        self._parse_model(annot_name='security', cached_key='auth', **kwargs)
        for key, val in self.auth.items():
            self.add_header(key, val)
        return self

    @cached_property
    def full_url(self) -> str:
        _url = f'{self.base_url}{self.url}'
        if self.url_params is None:
            return _url
        return _url.format(**self.url_params.dict())

    @cached_property
    def params(self):

        if not self.query_params:
            return None

        return self.query_params.dict(exclude_none=True, by_alias=True)

    @cached_property
    def auth(self):

        if not self.security:
            return None

        return self.security.dict(exclude_none=True, by_alias=True)

    def parse_response(self, resp: str | bytes) -> BaseModel | None:

        if self.has_response:
            return parse_raw_as(self.__annotations__['response'], resp)
        return None
