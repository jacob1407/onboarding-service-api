from uuid import UUID
from pydantic import BaseModel
from typing import List


class CreateRoleRequestModel(BaseModel):
    name: str
    template_ids: List[str]
    organisation_id: UUID


class GetRolesResponseModel(BaseModel):
    id: UUID
    name: str
    display_name: str
    template_ids: List[str]
    organisation_id: UUID

    model_config = {"from_attributes": True}
