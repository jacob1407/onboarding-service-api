from pydantic import BaseModel
from uuid import UUID


class CreateTemplateRequestModel(BaseModel):
    name: str
    organisation_id: UUID
    application_ids: list[UUID]


class GetTemplateReturnModel(BaseModel):
    id: UUID
    name: str
    display_name: str
    organisation_id: UUID
    application_ids: list[UUID]

    model_config = {"from_attributes": True}
