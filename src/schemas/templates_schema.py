from pydantic import BaseModel, computed_field
from uuid import UUID


class TemplateBaseModel(BaseModel):
    name: str
    application_ids: list[UUID]
    organisation_id: UUID


class CreateTemplateRequestModel(TemplateBaseModel):

    @computed_field
    @property
    def code(self) -> str:
        return self.name.lower().replace(" ", "_")


class TemplateResponseModel(TemplateBaseModel):
    id: UUID
    code: str
    organisation_id: UUID

    model_config = {"from_attributes": True}


class UpdateTemplateRequestModel(TemplateBaseModel):
    @computed_field
    @property
    def code(self) -> str | None:
        if self.name:
            return self.name.lower().replace(" ", "_")
        return None
