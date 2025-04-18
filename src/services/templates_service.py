import re
from sqlalchemy.orm import Session
from uuid import UUID

from .utils import to_snake_case

from ..schemas.templates_schema import (
    CreateTemplateRequestModel,
    GetTemplateReturnModel,
)
from ..data_access.template_dao import TemplateDAO
from ..models.template_model import TemplateModel


class TemplateService:
    def __init__(self, db: Session):
        self.dao = TemplateDAO(db)

    def create_template(
        self, template_data: CreateTemplateRequestModel
    ) -> GetTemplateReturnModel:
        display_name = to_snake_case(template_data.name)
        template = self.dao.create(
            template_data.name, display_name, template_data.organisation_id
        )
        return GetTemplateReturnModel.model_validate(template)

    def get_templates_by_org(self, org_id: UUID) -> list[GetTemplateReturnModel]:
        templates = self.dao.get_by_org(org_id)
        return [GetTemplateReturnModel.model_validate(t) for t in templates]

    def update_template(
        self, template_id: UUID, data: CreateTemplateRequestModel
    ) -> GetTemplateReturnModel:
        display_name = to_snake_case(data.name)
        template = self.dao.update(
            template_id, data.name, display_name, data.organisation_id
        )
        return GetTemplateReturnModel.model_validate(template)

    def delete_template(self, template_id: UUID) -> None:
        self.dao.delete(template_id)
