from uuid import UUID
from pydantic import BaseModel, computed_field
from typing import List


class CreateRoleRequestModel(BaseModel):
    name: str
    template_ids: List[str]
    organisation_id: UUID

    @computed_field
    @property
    def code(self) -> str:
        return self.name.lower().replace(" ", "_")


class GetRolesResponseModel(BaseModel):
    id: UUID
    name: str
    code: str
    template_ids: List[UUID]
    organisation_id: UUID

    model_config = {"from_attributes": True}
