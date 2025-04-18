from pydantic import BaseModel
from uuid import UUID


class CreateApplicationRequestModel(BaseModel):
    name: str
    organisation_id: UUID
    description: str


class GetApplicationResponseModel(BaseModel):
    id: UUID
    name: str
    display_name: str
    description: str
    organisation_id: UUID

    model_config = {"from_attributes": True}
