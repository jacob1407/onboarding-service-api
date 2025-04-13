from uuid import UUID
from pydantic import BaseModel
from typing import Optional, List


class CreateRoleRequestModel(BaseModel):
    name: str
    display_name: str
    template_ids: Optional[List[str]] = None


class GetRolesResponseModel(CreateRoleRequestModel):
    id: UUID

    class Config:
        orm_mode = True
