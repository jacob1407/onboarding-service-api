from pydantic import BaseModel
from uuid import UUID


class CreateTemplateRequestModel(BaseModel):
    name: str
    display_name: str
    organisation_id: UUID


class GetTemplateReturnModel(BaseModel):
    id: UUID
    name: str
    display_name: str
    organisation_id: UUID

    class Config:
        orm_mode = True
