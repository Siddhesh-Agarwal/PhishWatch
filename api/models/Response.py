from typing import Literal, TypedDict

from pydantic import AnyUrl, BaseModel


class CheckListDict(TypedDict):
    reason: str
    intensity: Literal["high", "medium", "low"]


class Response(BaseModel):
    url: AnyUrl
    isPhishing: bool
    reasons: list[CheckListDict] = []


class ResponseDict(TypedDict):
    url: str
    isPhishing: bool
    reasons: list[str] | None
