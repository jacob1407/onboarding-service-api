from uuid import UUID
from typing import List
from pydantic import BaseModel


class CreateOrganisationRequestModel(BaseModel):
    name: str
    contact_emails: List[str]


class GetOrganisationResponseModel(CreateOrganisationRequestModel):
    id: UUID

    class Config:
        orm_mode = True
