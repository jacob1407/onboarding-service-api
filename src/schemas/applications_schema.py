from pydantic import BaseModel, computed_field
from uuid import UUID
from typing import Optional

from ..schemas.user_schema import GetUserResponseModel


class CreateApplicationRequestModel(BaseModel):
    name: str
    description: Optional[str] = None
    contact_ids: list[UUID]


class GetApplicationResponseModel(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None
    contacts: list[GetUserResponseModel]

    model_config = {"from_attributes": True}


class GetApplicationsResponseModel(BaseModel):
    id: UUID
    name: str
    description: str | None = None

    model_config = {"from_attributes": True}
