from uuid import UUID
from pydantic import BaseModel
from typing import Optional, List


class CreateRoleRequestModel(BaseModel):
    name: str
    display_name: str
    template_ids: Optional[List[str]] = None
    organisation_id: UUID


class GetRolesResponseModel(CreateRoleRequestModel):
    id: UUID
    name: str
    display_name: str
    template_ids: Optional[List[str]] = None
    organisation_id: UUID

    model_config = {"from_attributes": True}
