from uuid import UUID
from pydantic import BaseModel, computed_field
from typing import List

from ..schemas.applications_schema import (
    GetApplicationsResponseModel,
)


class CreateRoleRequestModel(BaseModel):
    name: str
    application_ids: List[UUID]
    description: str | None = None

    @computed_field
    @property
    def code(self) -> str:
        return self.name.lower().replace(" ", "_")


class GetRolesResponseModel(BaseModel):
    id: UUID
    name: str
    description: str | None

    model_config = {"from_attributes": True}


class GetRoleResponseModel(BaseModel):
    id: UUID
    name: str
    description: str | None
    applications: List[GetApplicationsResponseModel]

    model_config = {"from_attributes": True}
