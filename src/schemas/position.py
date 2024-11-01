from pydantic import BaseModel

from src.schemas.base import BaseCreateResponse, BaseResponse


class PositionSchema(BaseModel):
    id: int | None
    name: str


class PositionCreateResponse(BaseCreateResponse):
    playload: PositionSchema


class PositionListResponse(BaseResponse):
    playload: list[PositionSchema]


class PositionResponse(BaseResponse):
    playload: PositionSchema
