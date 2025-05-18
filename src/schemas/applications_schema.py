from pydantic import BaseModel, computed_field
from uuid import UUID
from typing import Optional

from ..schemas.contact_schema import GetContactResponseModel


class CreateApplicationRequestModel(BaseModel):
    name: str
    description: Optional[str] = None
    contact_ids: list[UUID]

    @computed_field
    @property
    def code(self) -> str:
        return self.name.lower().replace(" ", "_")


class GetApplicationResponseModel(BaseModel):
    id: UUID
    name: str
    code: str
    description: Optional[str] = None
    contacts: list[GetContactResponseModel]

    model_config = {"from_attributes": True}


class GetApplicationsResponseModel(BaseModel):
    id: UUID
    name: str
    code: str
    description: Optional[str] = None

    model_config = {"from_attributes": True}
