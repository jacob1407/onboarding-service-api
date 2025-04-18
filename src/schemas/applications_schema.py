from pydantic import BaseModel
from uuid import UUID
from typing import Optional


class CreateApplicationRequestModel(BaseModel):
    name: str
    organisation_id: UUID
    description: Optional[str] = None


class GetApplicationResponseModel(BaseModel):
    id: UUID
    name: str
    display_name: str
    organisation_id: UUID
    description: Optional[str] = None

    model_config = {"from_attributes": True}
