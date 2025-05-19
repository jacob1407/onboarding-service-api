from pydantic import BaseModel, EmailStr
from uuid import UUID
from typing import Optional


class CreateContactRequestModel(BaseModel):
    first_name: str
    last_name: str
    email: str
    external_id: Optional[str] = None


class GetContactResponseModel(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email: str

    model_config = {"from_attributes": True}
