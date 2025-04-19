from pydantic import BaseModel, EmailStr
from uuid import UUID
from typing import Optional


class CreateContactRequestModel(BaseModel):
    first_name: str
    last_name: str
    email: str
    external_id: Optional[str] = None
    organisation_id: UUID


class GetContactResponseModel(CreateContactRequestModel):
    id: UUID

    model_config = {"from_attributes": True}
