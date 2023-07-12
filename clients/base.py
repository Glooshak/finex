from typing import Any
from enum import Enum

from pydantic import BaseModel


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
