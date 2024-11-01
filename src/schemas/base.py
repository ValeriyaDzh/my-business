from pydantic import BaseModel
from starlette.status import HTTP_200_OK, HTTP_201_CREATED


class Message(BaseModel):
    message: str


class BaseResponse(BaseModel):
    status: int = HTTP_200_OK
    error: bool = False


class BaseCreateResponse(BaseModel):
    status: int = HTTP_201_CREATED
    error: bool = False


class Confirm(BaseModel):
    flag: bool


class BaseConfirmResponse(BaseResponse):
    playload: Confirm
