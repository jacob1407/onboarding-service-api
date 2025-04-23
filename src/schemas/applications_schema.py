from pydantic import BaseModel, computed_field
from uuid import UUID
from typing import Optional


class CreateApplicationRequestModel(BaseModel):
    name: str
    organisation_id: UUID
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
    organisation_id: UUID
    description: Optional[str] = None

    model_config = {"from_attributes": True}
